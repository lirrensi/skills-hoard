"""Artify - HTML artifact preview/serve CLI with live-reload.

Opens a local HTML file directly in the browser, or serves it on a random
local port with polling-based live-reload. Supports an optional --webview
flag that opens the served page in a chromeless native window using the
host browser's --app=URL mode. Also manages running instances (list/kill/
restart by port) and exposes a command/response snapshot endpoint that
lets the CLI read the current form state from a page the human is filling
out in a browser.

FILE: artify/cli/src/artify_cli/cli.py
PURPOSE: CLI tool for previewing, live-reloading, instance-managing, and snapshotting HTML artifacts locally during authoring.
OWNS: artify open/serve/list/kill/restart/snapshot commands, the local HTTP server used by serve (incl. command/response snapshot endpoints), the per-port instance registry under ~/.artify/instances, and app-mode browser detection for --webview.
EXPORTS: main (Click group), open, serve, list_cmd, kill, restart, snapshot
DOCS: docs/product.md (## Tool: artify), docs/arch.md (## Component: artify)
DEPENDS_ON: click, watchdog, psutil, rich
DOES_NOT: serve directories, support --port/--no-reload/--no-open/--await-response, network binding beyond 127.0.0.1
NOTES: Local dev tool. Binds HTTP to 127.0.0.1 only. Polling-based live-reload (500ms client, 150ms watchdog debounce). Idempotent reload script injection via INJECT_MARKER. Snapshot is command/response, single round-trip (no state push, no WebSocket). Server is multi-threaded (ThreadingMixIn) so the snapshot handler can block while the page still polls /__commands. ReloadState is a backward-compat alias for InstanceState.
"""

from __future__ import annotations

import builtins
import functools
import http.server
import json
import mimetypes
import os
import platform
import shutil
import socketserver
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

import click
import psutil
from rich.console import Console
from rich.table import Table

__version__ = "0.0.0"


INJECT_MARKER = "<!--ARTIFY_RELOAD-->"

RELOAD_JS = """(function(){
  // --- Live-reload polling (existing) ---
  var lastReload = null;
  setInterval(function(){
    fetch('/__reload_check').then(function(r){ return r.text(); }).then(function(t){
      if (lastReload !== null && t !== lastReload) { location.reload(); }
      lastReload = t;
    }).catch(function(){});
  }, 500);

  // --- Command polling (new) ---
  function collect() {
    if (typeof window.__artify_collect__ === 'function') {
      try { return window.__artify_collect__(); } catch(e) { return {__artify_collect_error: String(e)}; }
    }
    var data = {};
    var els = document.querySelectorAll('input, textarea, select');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.disabled) continue;
      var type = (el.type || '').toLowerCase();
      if (type === 'submit' || type === 'button' || type === 'reset' || type === 'image') continue;
      var key = el.name || el.id;
      if (!key) continue;
      if (type === 'checkbox') data[key] = el.checked;
      else if (type === 'radio') { if (el.checked) data[key] = el.value; }
      else if (el.tagName === 'SELECT' && el.multiple) {
        data[key] = Array.prototype.slice.call(el.selectedOptions).map(function(o){ return o.value; });
      } else {
        data[key] = el.value;
      }
    }
    return data;
  }
  function execute(cmd) {
    if (cmd.type === 'snapshot') {
      var data = collect();
      fetch('/__snapshot_result/' + encodeURIComponent(cmd.id), {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({fields: data})
      }).catch(function(){});
    }
    // Future: handle other command types here
  }
  setInterval(function(){
    fetch('/__commands').then(function(r){ return r.json(); }).then(function(cmds){
      if (Array.isArray(cmds)) cmds.forEach(execute);
    }).catch(function(){});
  }, 500);
})();"""


# --- Script injection ----------------------------------------------------


def inject_reload_script(html: str) -> str:
    """Append the live-reload script tag to HTML. Idempotent.

    Inserts the marker + script tag just before </body>, else before </html>,
    else at the end of the string. If the marker is already present, returns
    the input unchanged.
    """
    if INJECT_MARKER in html:
        return html

    inject = f'{INJECT_MARKER}<script src="/__reload.js"></script>'

    lower = html.lower()
    body_close = lower.rfind("</body>")
    if body_close != -1:
        return html[:body_close] + inject + html[body_close:]

    html_close = lower.rfind("</html>")
    if html_close != -1:
        return html[:html_close] + inject + html[html_close:]

    return html + inject


# --- App-mode browser detection ------------------------------------------


def find_app_browser() -> list[str] | None:
    """Locate a native browser that supports --app=URL mode.

    Returns the argv template (with a literal '{url}' slot to be filled in
    by open_in_webview) for the first supported browser found, or None.
    """
    system = platform.system()

    if system == "Windows":
        # Prefer Edge (always present on modern Windows), then Chrome.
        edge = shutil.which("msedge.exe")
        if edge:
            return [edge, "--app={url}"]
        chrome = shutil.which("chrome.exe")
        if chrome:
            return [chrome, "--app={url}"]
        return None

    if system == "Darwin":
        # `open` is always present; only return a launcher if Chrome is installed.
        if Path("/Applications/Google Chrome.app").exists():
            open_path = shutil.which("open")
            if open_path:
                return [open_path, "-na", "Google Chrome", "--args", "--app={url}"]
        return None

    # Linux: try common chromium-family binaries in order.
    for name in ("google-chrome", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return [path, "--app={url}"]

    return None


def open_in_webview(url: str) -> bool:
    """Launch the app-mode browser detached. Returns True on successful spawn."""
    launcher = find_app_browser()
    if launcher is None:
        return False

    cmd = [arg.format(url=url) for arg in launcher]
    try:
        kwargs: dict = {
            "stdin": subprocess.DEVNULL,
            "stdout": subprocess.DEVNULL,
            "stderr": subprocess.DEVNULL,
        }
        if sys.platform == "win32":
            # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
            kwargs["creationflags"] = 0x00000008 | 0x00000200
            kwargs["close_fds"] = True
        else:
            kwargs["start_new_session"] = True
        subprocess.Popen(cmd, **kwargs)
        return True
    except OSError:
        return False


# --- Instance registry ---------------------------------------------------

REGISTRY_DIR = Path.home() / ".artify" / "instances"


def is_pid_alive(pid: int) -> bool:
    """Return True if pid is a currently running process.

    Wraps psutil.pid_exists (already a core dep) and tolerates bogus values.
    """
    try:
        return psutil.pid_exists(int(pid))
    except (ValueError, TypeError):
        return False


def collect_serving_url(port: int) -> str:
    """Return the canonical URL for a running serve instance on port."""
    return f"http://127.0.0.1:{port}/"


def write_registry_entry(port: int, pid: int, file: Path) -> None:
    """Atomically write the per-port registry file under ~/.artify/instances/.

    The temp file is written to ``<port>.json.tmp`` and renamed onto
    ``<port>.json`` via os.replace so a concurrent reader never sees a
    half-written file. Best-effort: any OSError is swallowed silently
    because the registry is observability, not correctness.
    """
    try:
        REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        return
    entry = {
        "port": int(port),
        "pid": int(pid),
        "file": str(Path(file).resolve()),
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    target = REGISTRY_DIR / f"{port}.json"
    tmp = target.with_suffix(".json.tmp")
    try:
        # Use builtins.open explicitly because the module's `open` Click
        # command shadows the builtin in this namespace.
        with builtins.open(tmp, "w", encoding="utf-8") as fp:
            json.dump(entry, fp)
        os.replace(tmp, target)
    except OSError:
        # Best-effort cleanup of the temp file on failure.
        try:
            tmp.unlink()
        except OSError:
            pass


def remove_registry_entry(port: int) -> None:
    """Remove the registry entry for port. Silent on missing or unreadable."""
    target = REGISTRY_DIR / f"{port}.json"
    try:
        target.unlink()
    except FileNotFoundError:
        pass
    except OSError:
        pass


def read_registry() -> list[dict]:
    """Return all registry entries, sorted by port ascending.

    Each entry is augmented with ``alive`` (bool) computed via
    psutil.pid_exists on the stored PID. Stale (dead) entries are kept
    so the user can see and decide what to do with them; the CLI never
    auto-removes them.
    """
    if not REGISTRY_DIR.is_dir():
        return []
    out: list[dict] = []
    for path in REGISTRY_DIR.glob("*.json"):
        try:
            raw = path.read_text(encoding="utf-8")
            entry = json.loads(raw)
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(entry, dict):
            continue
        try:
            port = int(entry.get("port", 0))
            pid = int(entry.get("pid", 0))
        except (ValueError, TypeError):
            continue
        entry["port"] = port
        entry["pid"] = pid
        entry["alive"] = is_pid_alive(pid)
        out.append(entry)
    out.sort(key=lambda e: e.get("port", 0))
    return out


# --- HTTP server ---------------------------------------------------------


class InstanceState:
    """Per-instance server state: file mtime, command queue, snapshot registry.

    The mtime field keeps the existing live-reload semantics. The command
    queue carries requests from the CLI (``POST /__snapshot_request``) to
    the page (polling ``GET /__commands``). The snapshot registry carries
    the page's response (``POST /__snapshot_result/<id>``) back to the
    blocking CLI handler via a per-id ``threading.Event``.
    """

    def __init__(self, path: Path, snapshot_timeout: float = 30.0) -> None:
        self.path = path
        self.snapshot_timeout = float(snapshot_timeout)

        # Live-reload mtime (legacy ReloadState semantics).
        self._mtime_lock = threading.Lock()
        self._mtime: float = self._read_mtime()

        # Command queue: CLI -> page. Lock kept separate from mtime to
        # avoid contention between watchdog events and snapshot requests.
        self.commands_lock = threading.Lock()
        self.pending_commands: list[dict] = []

        # Snapshot wait/result registry: page -> CLI. ``snapshot_results``
        # holds ``None`` while a slot is allocated but no page response has
        # arrived yet, and the actual result dict once the page POSTs it.
        self.results_lock = threading.Lock()
        self.pending_snapshots: dict[str, threading.Event] = {}
        self.snapshot_results: dict[str, dict | None] = {}

    # --- mtime (legacy ReloadState API) --------------------------------

    def _read_mtime(self) -> float:
        try:
            return self.path.stat().st_mtime
        except OSError:
            return 0.0

    def get(self) -> float:
        with self._mtime_lock:
            return self._mtime

    def update_from_disk(self) -> None:
        mtime = self._read_mtime()
        with self._mtime_lock:
            self._mtime = mtime

    def bump(self) -> None:
        """Mark a change (called by watchdog on a debounced file-modified event).

        Note: this is a defense-in-depth placeholder. ``__reload_check``
        always calls ``update_from_disk()`` on every poll, which overwrites
        anything ``bump()`` writes, so in normal operation this path is
        dead. It is kept so a future push-based transport (e.g. WebSocket)
        can rely on it.
        """
        with self._mtime_lock:
            self._mtime = time.time()

    # --- command queue (CLI -> page) -----------------------------------

    def enqueue_command(self, cmd: dict) -> None:
        with self.commands_lock:
            self.pending_commands.append(cmd)

    def drain_commands(self) -> list[dict]:
        with self.commands_lock:
            cmds = self.pending_commands
            self.pending_commands = []
            return cmds

    # --- snapshot registry (page -> CLI) -------------------------------

    def register_snapshot(self, sid: str) -> threading.Event:
        """Allocate a new pending snapshot slot for ``sid`` and return its event."""
        event = threading.Event()
        with self.results_lock:
            self.pending_snapshots[sid] = event
            self.snapshot_results[sid] = None
        return event

    def set_snapshot_result(self, sid: str, data: dict) -> bool:
        """Record the page's response for ``sid`` and signal the waiter.

        Returns False if ``sid`` is unknown (caller should respond 404).
        """
        with self.results_lock:
            if sid not in self.pending_snapshots:
                return False
            self.snapshot_results[sid] = data
            event = self.pending_snapshots.get(sid)
        if event is not None:
            event.set()
        return True

    def wait_for_snapshot(self, sid: str, timeout: float | None = None) -> dict | None:
        """Block until the page's response arrives, or ``timeout`` elapses.

        Returns the result dict on success, or None on timeout / unknown id.
        Cleans up the registry slot either way.
        """
        if timeout is None:
            timeout = self.snapshot_timeout
        with self.results_lock:
            event = self.pending_snapshots.get(sid)
        if event is None:
            return None
        if not event.wait(timeout=timeout):
            # Timeout: drop the slot so a late response doesn't accumulate.
            with self.results_lock:
                self.pending_snapshots.pop(sid, None)
                self.snapshot_results.pop(sid, None)
            return None
        with self.results_lock:
            result = self.snapshot_results.get(sid)
            self.pending_snapshots.pop(sid, None)
            self.snapshot_results.pop(sid, None)
        return result


# Backward-compat alias: the existing v1 tests reference ReloadState.
ReloadState = InstanceState


class ArtifyHandler(http.server.BaseHTTPRequestHandler):
    """Serves the user's file (with reload script injected) and the protocol endpoints.

    GET endpoints
    -------------
    ``/`` / ``/index.html``        - the served file (HTML gets the script injected)
    ``/__reload.js``               - the polling + command JS
    ``/__reload_check``            - returns the current mtime as text
    ``/__commands``                - drain pending commands as a JSON array

    POST endpoints
    --------------
    ``/__snapshot_request``        - enqueue a snapshot command and block until the page
                                     responds (or ``InstanceState.snapshot_timeout`` elapses)
    ``/__snapshot_result/<id>``    - record the page's response for a pending snapshot
    """

    quiet = True

    def __init__(
        self,
        request,  # noqa: ANN001 — stdlib type
        client_address,  # noqa: ANN001
        server,  # noqa: ANN001
        *,
        state: InstanceState,
        file_path: Path,
    ) -> None:
        self.state = state
        self.file_path = file_path
        super().__init__(request, client_address, server)

    def do_GET(self) -> None:  # noqa: N802 — stdlib API
        if self.path in ("/", "/index.html"):
            self._serve_file()
        elif self.path == "/__reload.js":
            self._send_text(RELOAD_JS, "application/javascript; charset=utf-8")
        elif self.path == "/__reload_check":
            # Re-read the file mtime on every poll so the client reloads
            # promptly after a save, even if a watchdog event was missed.
            self.state.update_from_disk()
            self._send_text(str(self.state.get()), "text/plain; charset=utf-8")
        elif self.path == "/__commands":
            self._send_json(self.state.drain_commands())
        else:
            self.send_error(404, "Not Found")

    def do_POST(self) -> None:  # noqa: N802 — stdlib API
        prefix = "/__snapshot_result/"
        if self.path.startswith(prefix):
            self._handle_snapshot_result(self.path[len(prefix):])
            return
        if self.path == "/__snapshot_request":
            self._handle_snapshot_request()
            return
        self.send_error(404, "Not Found")

    def _handle_snapshot_request(self) -> None:
        """Enqueue a snapshot command and block in this thread until the page responds.

        Returns 200 with ``{"fields": {...}}`` on success, or 408 with
        ``{"error": "page did not respond"}`` on timeout. The server is
        multi-threaded (see ReusableTCPServer) so other connections — in
        particular the page's polling of /__commands — keep flowing while
        this handler is blocked.
        """
        sid = uuid.uuid4().hex
        self.state.enqueue_command({"type": "snapshot", "id": sid})
        self.state.register_snapshot(sid)
        result = self.state.wait_for_snapshot(sid, timeout=self.state.snapshot_timeout)
        if result is None:
            self._send_json({"error": "page did not respond"}, status=408)
            return
        self._send_json(result, status=200)

    def _handle_snapshot_result(self, sid: str) -> None:
        """Record the page's response for snapshot ``sid`` and signal the waiter."""
        try:
            length = int(self.headers.get("Content-Length", "0") or "0")
        except ValueError:
            length = 0
        body_raw = self.rfile.read(length) if length > 0 else b""
        if body_raw:
            try:
                payload = json.loads(body_raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._send_json({"error": "invalid json body"}, status=400)
                return
        else:
            payload = {}
        if not isinstance(payload, dict):
            payload = {}
        fields = payload.get("fields", {})
        if not isinstance(fields, dict):
            fields = {}
        if not sid or not self.state.set_snapshot_result(sid, {"fields": fields}):
            self._send_json({"error": "unknown snapshot id"}, status=404)
            return
        self._send_json({"ok": True}, status=200)

    def _serve_file(self) -> None:
        try:
            raw = self.file_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            self.send_error(500, f"Failed to read file: {exc}")
            return

        if self.file_path.suffix.lower() in (".html", ".htm"):
            body = inject_reload_script(raw).encode("utf-8")
        else:
            body = raw.encode("utf-8")

        guessed, _ = mimetypes.guess_type(self.file_path)
        content_type = guessed or "text/plain"
        # Browsers without a charset will assume their own default (often
        # not UTF-8). Always tag the charset explicitly for text types.
        if content_type.startswith("text/") and "charset=" not in content_type:
            content_type = f"{content_type}; charset=utf-8"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, body: str, content_type: str) -> None:
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, payload: object, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002 — stdlib API
        if not self.quiet:
            super().log_message(format, *args)


class ReusableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """TCP server with SO_REUSEADDR, threaded per request.

    ThreadingMixIn is required by the snapshot design: ``POST
    /__snapshot_request`` blocks in its handler thread while it waits for
    the page's response, and the page must still be able to GET
    ``/__commands`` and POST ``/__snapshot_result/<id>`` on a different
    worker thread during that window. Without threading, those would
    queue behind the snapshot request and the protocol would deadlock.
    """

    allow_reuse_address = True
    daemon_threads = True


def start_server(
    path: Path,
    snapshot_timeout: float = 30.0,
) -> tuple[ReusableTCPServer, int, InstanceState]:
    """Build the local server bound to 127.0.0.1 on a random free port."""
    state = InstanceState(path, snapshot_timeout=snapshot_timeout)
    handler = functools.partial(ArtifyHandler, state=state, file_path=path)
    server = ReusableTCPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    return server, port, state


# --- Watchdog live-reload -----------------------------------------------


def watch_and_serve(path: Path, server: ReusableTCPServer, state: InstanceState) -> None:
    """Run watchdog in the background; main thread serves HTTP until interrupted.

    Watchdog bursts (temp-file + rename) are coalesced with a 150ms throttle.
    """
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    debounce_seconds = 0.15

    class _Handler(FileSystemEventHandler):
        def __init__(self) -> None:
            self._last_event: float = 0.0
            self._target = path.resolve()

        def on_modified(self, event) -> None:  # type: ignore[override]
            if event.is_directory:
                return
            now = time.monotonic()
            if now - self._last_event < debounce_seconds:
                # Burst from an editor's temp-file + rename pattern — ignore.
                return
            self._last_event = now

            try:
                event_path = Path(event.src_path).resolve()
            except OSError:
                return
            if event_path != self._target:
                return

            state.bump()

    observer = Observer()
    observer.schedule(_Handler(), str(path.parent), recursive=False)
    observer.daemon = True
    observer.start()
    try:
        server.serve_forever()
    finally:
        observer.stop()
        observer.join(timeout=2)


# --- Browser launch ------------------------------------------------------


def open_with_browser(url: str, webview: bool) -> None:
    """Open url in the default browser tab, or in an app-mode native window if webview is True."""
    if webview and open_in_webview(url):
        click.echo("Opened in app-mode browser.")
        return
    if webview:
        click.echo(
            "App-mode browser not found; falling back to default browser.",
            err=True,
        )
    webbrowser.open_new_tab(url)
    click.echo("Opened in default browser tab.")


# --- Cross-platform process termination helpers -------------------------


def _terminate_pid(pid: int, grace_seconds: float = 2.0) -> None:
    """Best-effort SIGTERM-then-SIGKILL for ``pid``. No-op if already dead.

    Raises ``psutil.AccessDenied`` if the OS refuses the operation; callers
    should surface that to the user.
    """
    if not is_pid_alive(pid):
        return
    proc = psutil.Process(pid)
    proc.terminate()
    deadline = time.monotonic() + grace_seconds
    while time.monotonic() < deadline and is_pid_alive(pid):
        time.sleep(0.05)
    if is_pid_alive(pid):
        psutil.Process(pid).kill()


def _read_registry_entry(port: int) -> dict | None:
    """Read and parse the registry entry for ``port``. Returns None on miss or corruption."""
    path = REGISTRY_DIR / f"{port}.json"
    try:
        # Use builtins.open explicitly because the module's `open` Click
        # command shadows the builtin in this namespace.
        with builtins.open(path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except FileNotFoundError:
        return None
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    return data


# --- Click commands ------------------------------------------------------


@click.group()
@click.version_option(__version__, prog_name="artify")
def main() -> None:
    """Open, serve, manage, and snapshot HTML artifacts."""


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def open(file: Path) -> None:  # noqa: A001 — Click command name shadows builtin; intentional
    """Open FILE in the default browser via file:// (offline, no server)."""
    url = f"file:///{file.resolve().as_posix()}"
    click.echo(f"Opening: {url}")
    if not webbrowser.open_new_tab(url):
        click.echo("Failed to open browser.", err=True)
        sys.exit(1)


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "--webview",
    is_flag=True,
    help="Open in a chromeless native window (browser --app mode) instead of a regular tab.",
)
def serve(file: Path, webview: bool) -> None:
    """Serve FILE on a random port with live-reload, open in browser."""
    server, port, state = start_server(file)
    write_registry_entry(port, os.getpid(), file)
    url = f"http://localhost:{port}/"
    click.echo(f"Serving: {file}  ->  {url}")
    click.echo("Press Ctrl+C to stop.")
    open_with_browser(url, webview)
    try:
        watch_and_serve(file, server, state)
    except KeyboardInterrupt:
        click.echo("\nStopping...")
    finally:
        server.shutdown()
        server.server_close()
        remove_registry_entry(port)


@main.command(name="list")
def list_cmd() -> None:
    """List running artify serve instances (PORT is the unique instance ID)."""
    entries = read_registry()
    if not entries:
        click.echo("No artify instances running.")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("PORT", justify="right")
    table.add_column("PID", justify="right")
    table.add_column("FILE")
    table.add_column("STATUS")
    table.add_column("STARTED")
    table.add_column("URL")

    for entry in entries:
        port = entry.get("port", 0)
        pid = entry.get("pid", 0)
        file_str = str(entry.get("file", ""))
        started = str(entry.get("started_at", ""))
        alive = bool(entry.get("alive", False))
        # Show last 60 chars of the file path so long Windows paths still fit.
        file_display = file_str
        if len(file_display) > 60:
            file_display = "..." + file_display[-57:]
        if alive:
            status = "running"
            url = collect_serving_url(port)
            style = None
        else:
            status = "dead"
            url = "-"
            style = "dim"
        table.add_row(
            str(port),
            str(pid),
            file_display,
            status,
            started,
            url,
            style=style,
        )

    Console().print(table)


@main.command()
@click.argument("port", type=click.IntRange(min=1, max=65535))
def kill(port: int) -> None:
    """Kill the artify serve instance on PORT and clean up its registry entry."""
    entry = _read_registry_entry(port)
    if entry is None:
        click.echo(f"No artify instance on port {port}", err=True)
        sys.exit(1)

    pid = int(entry.get("pid", 0))
    was_alive = is_pid_alive(pid)
    if was_alive:
        try:
            _terminate_pid(pid)
        except psutil.NoSuchProcess:
            was_alive = False
        except psutil.AccessDenied as exc:
            click.echo(f"Access denied killing pid {pid}: {exc}", err=True)
            sys.exit(1)
        # else: _terminate_pid succeeded — keep was_alive=True so the
        # success message below is printed. Don't re-check liveness here:
        # the process is, by definition, no longer alive after a successful
        # terminate, and re-checking would flip the flag and print the
        # misleading "already not running" message instead.

    remove_registry_entry(port)
    if was_alive:
        click.echo(f"Killed artify instance on port {port} (pid {pid})")
    else:
        click.echo(
            f"Instance on port {port} (pid {pid}) was already not running; cleaned up registry."
        )


@main.command()
@click.argument("port", type=click.IntRange(min=1, max=65535))
def restart(port: int) -> None:
    """Kill the artify instance on PORT and re-serve the same file on a new port."""
    entry = _read_registry_entry(port)
    if entry is None:
        click.echo(f"No artify instance on port {port}", err=True)
        sys.exit(1)

    file_str = str(entry.get("file", ""))
    if not file_str:
        click.echo(f"Registry entry for port {port} is missing the file path.", err=True)
        sys.exit(1)
    file_path = Path(file_str)
    if not file_path.is_file():
        click.echo(f"File no longer exists: {file_path}", err=True)
        sys.exit(1)

    # Kill the existing instance (best-effort) and clear its registry entry
    # so we don't leave a stale entry pointing at a now-dead port.
    pid = int(entry.get("pid", 0))
    if is_pid_alive(pid):
        try:
            _terminate_pid(pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    remove_registry_entry(port)

    # Spawn a detached `artify serve` for the same file. The new instance
    # picks a fresh free port and writes its own registry entry.
    cmd = [sys.executable, "-m", "artify_cli", "serve", str(file_path)]
    spawn_kwargs: dict = {}
    if sys.platform == "win32":
        # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP so the new process
        # survives this one's exit and doesn't share our console.
        spawn_kwargs["creationflags"] = 0x00000008 | 0x00000200
        spawn_kwargs["close_fds"] = True
    else:
        spawn_kwargs["start_new_session"] = True
        spawn_kwargs["stdin"] = subprocess.DEVNULL
        spawn_kwargs["stdout"] = subprocess.DEVNULL
        spawn_kwargs["stderr"] = subprocess.DEVNULL
    subprocess.Popen(cmd, **spawn_kwargs)

    # Give the new instance a beat to bind its port and write its registry
    # entry, so a follow-up `artify list` sees it without a race.
    time.sleep(0.3)
    click.echo(
        "Restarted. New instance on a different port — run 'artify list' to find it."
    )


@main.command()
@click.argument("port", type=click.IntRange(min=1, max=65535))
@click.option(
    "--timeout",
    type=click.FloatRange(min=1.0),
    default=30.0,
    show_default=True,
    help="Seconds to wait for the page to respond before giving up.",
)
def snapshot(port: int, timeout: float) -> None:
    """Trigger a snapshot on the artify serve instance on PORT and print the form state as JSON.

    Sends a snapshot command to the running instance, waits for the page to
    respond with all current form field values, then prints the JSON.
    Blocks until the page responds or the instance times out.
    """
    url = f"http://127.0.0.1:{port}/__snapshot_request"
    request = urllib.request.Request(url, method="POST", data=b"")
    try:
        # Use a small safety margin past `timeout` so the server's 408
        # response has time to come back after it expires its own wait.
        with urllib.request.urlopen(request, timeout=timeout + 5.0) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        if exc.code == 408:
            click.echo(f"Page did not respond within {timeout}s", err=True)
            sys.exit(1)
        click.echo(f"HTTP {exc.code} from artify on port {port}: {exc.reason}", err=True)
        sys.exit(1)
    except urllib.error.URLError as exc:
        # Connection refused, no route, DNS failure, etc. — for the user
        # the practical message is "no instance on that port".
        click.echo(f"No artify instance on port {port}", err=True)
        sys.exit(1)
    except (TimeoutError, OSError) as exc:
        # The server-side wait expired at the same moment as the socket
        # timeout; treat it the same as a 408 from the user's perspective.
        click.echo(f"Page did not respond within {timeout}s ({exc})", err=True)
        sys.exit(1)

    # 200 OK — print the payload verbatim. `fields` may be empty, that is fine.
    try:
        payload = json.loads(body) if body else {}
    except json.JSONDecodeError:
        click.echo(f"Artify on port {port} returned invalid JSON: {body!r}", err=True)
        sys.exit(1)
    click.echo(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
