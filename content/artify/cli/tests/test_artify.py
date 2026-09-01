# FILE: tests/test_artify.py
# PURPOSE: Test coverage for the artify CLI tool.
# OWNS: Behavior tests for inject_reload_script, find_app_browser, open_in_webview,
#       ArtifyHandler + start_server, the Click open/serve commands, the registry
#       helpers (write/read/remove), the new list/kill/restart/snapshot Click
#       commands, the /__commands and /__snapshot_* HTTP endpoints, the
#       threaded server, and the custom __artify_collect__ hook.
# DOCS: .agents/reports/plan_artify_2026-06-20.md, docs/product.md, docs/arch.md

from __future__ import annotations

import http.client
import json
import os
import platform
import shutil
import socket
import socketserver
import subprocess
import sys
import threading
import time
from pathlib import Path
from unittest import mock

import click.testing
import pytest

import artify_cli.cli as artify  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def runner() -> click.testing.CliRunner:
    return click.testing.CliRunner()


@pytest.fixture
def html_file(tmp_path: Path) -> Path:
    """A minimal HTML file in tmp_path that the server can serve."""
    p = tmp_path / "index.html"
    p.write_text(
        "<!doctype html><html><head><title>T</title></head>"
        "<body><h1>hi</h1></body></html>",
        encoding="utf-8",
    )
    return p


@pytest.fixture
def html_no_body(tmp_path: Path) -> Path:
    """A fragment of HTML with no </body> or </html> tags."""
    p = tmp_path / "frag.html"
    p.write_text("<div>just a div</div>", encoding="utf-8")
    return p


@pytest.fixture
def html_no_body_no_html(tmp_path: Path) -> Path:
    """A bare string with no closing tags at all."""
    p = tmp_path / "bare.html"
    p.write_text("hello world", encoding="utf-8")
    return p


def _start_server_thread(
    path: Path,
) -> tuple[socketserver.TCPServer, int]:
    """Start a real HTTP server on a real port in a background thread. Returns (server, port)."""
    server, port, _state = artify.start_server(path)
    t = threading.Thread(target=server.serve_forever, name="artify-test-server", daemon=True)
    t.start()
    return server, port


def _http_get(host: str, port: int, path: str) -> tuple[int, dict, bytes]:
    """Make a GET to a real port. Returns (status, headers, body)."""
    conn = http.client.HTTPConnection(host, port, timeout=5)
    try:
        conn.request("GET", path)
        resp = conn.getresponse()
        body = resp.read()
        # Map headers to a plain dict of (key -> value) preserving case.
        headers = {k: v for k, v in resp.getheaders()}
        return resp.status, headers, body
    finally:
        conn.close()


def _wait_for_port(host: str, port: int, timeout: float = 5.0) -> None:
    """Poll until the server is accepting connections."""
    deadline = time.time() + timeout
    last_err: Exception | None = None
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return
        except OSError as exc:
            last_err = exc
            time.sleep(0.05)
    raise RuntimeError(f"server never came up on {host}:{port}: {last_err}")


# ---------------------------------------------------------------------------
# inject_reload_script
# ---------------------------------------------------------------------------


class TestInjectReloadScript:
    def test_inserts_before_body_close(self, html_file: Path) -> None:
        raw = html_file.read_text(encoding="utf-8")
        out = artify.inject_reload_script(raw)
        assert artify.INJECT_MARKER in out
        # Marker should sit immediately before </body>
        idx = out.find(artify.INJECT_MARKER)
        assert out[idx:].startswith(artify.INJECT_MARKER)
        assert out[idx:].find("</body>") > 0
        # The injection should be on the line just before </body>
        assert (
            out.rfind(artify.INJECT_MARKER) < out.rfind("</body>")
        ), "marker must be inserted before </body>"

    def test_inserts_before_html_close_when_no_body(self, tmp_path: Path) -> None:
        p = tmp_path / "nobody.html"
        p.write_text(
            "<!doctype html><html><head></head></html>",
            encoding="utf-8",
        )
        raw = p.read_text(encoding="utf-8")
        out = artify.inject_reload_script(raw)
        assert artify.INJECT_MARKER in out
        assert (
            out.rfind(artify.INJECT_MARKER) < out.rfind("</html>")
        ), "marker must be inserted before </html> when no body"

    def test_appends_to_end_when_neither_tag_present(
        self, html_no_body_no_html: Path
    ) -> None:
        raw = html_no_body_no_html.read_text(encoding="utf-8")
        out = artify.inject_reload_script(raw)
        assert artify.INJECT_MARKER in out
        # The original content must come before the injection, with the
        # marker sitting right at the start of the appended block.
        idx = out.find(artify.INJECT_MARKER)
        assert out[:idx] == raw
        # And the script tag must be appended after the marker.
        assert out.endswith('<script src="/__reload.js"></script>')

    def test_idempotent(self, html_file: Path) -> None:
        raw = html_file.read_text(encoding="utf-8")
        once = artify.inject_reload_script(raw)
        twice = artify.inject_reload_script(once)
        # Second call returns the same string.
        assert once == twice
        # And the marker appears exactly once in the final string.
        assert once.count(artify.INJECT_MARKER) == 1

    def test_case_insensitive_tag_match(self) -> None:
        # Uppercase tags
        raw_upper = "<HTML><BODY><P>hi</P></BODY></HTML>"
        out_upper = artify.inject_reload_script(raw_upper)
        assert out_upper.count(artify.INJECT_MARKER) == 1
        assert out_upper.rfind(artify.INJECT_MARKER) < out_upper.rfind("</BODY>")

        # Mixed case
        raw_mixed = "<html><Body>x</Body></html>"
        out_mixed = artify.inject_reload_script(raw_mixed)
        assert out_mixed.count(artify.INJECT_MARKER) == 1
        assert out_mixed.rfind(artify.INJECT_MARKER) < out_mixed.rfind("</Body>")

    def test_idempotent_across_multiple_calls(self) -> None:
        raw = "<html><body>x</body></html>"
        s = raw
        for _ in range(5):
            s = artify.inject_reload_script(s)
        assert s.count(artify.INJECT_MARKER) == 1

    def test_marker_is_html_comment(self) -> None:
        out = artify.inject_reload_script("<html><body></body></html>")
        # The marker should be a valid HTML comment.
        assert artify.INJECT_MARKER.startswith("<!--")
        assert artify.INJECT_MARKER.endswith("-->")
        assert artify.INJECT_MARKER in out


# ---------------------------------------------------------------------------
# find_app_browser
# ---------------------------------------------------------------------------


class TestFindAppBrowser:
    def test_returns_none_when_nothing_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Force every possible detection path to fail.
        monkeypatch.setattr(platform, "system", lambda: "Windows")
        monkeypatch.setattr(shutil, "which", lambda name: None)
        assert artify.find_app_browser() is None

    def test_windows_edge(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(platform, "system", lambda: "Windows")
        monkeypatch.setattr(
            shutil, "which", lambda name: "C:/edge/msedge.exe" if name == "msedge.exe" else None
        )
        result = artify.find_app_browser()
        assert result is not None
        assert result[0] == "C:/edge/msedge.exe"
        assert "--app={url}" in result
        # Confirm there is a literal {url} slot.
        assert any("{url}" in arg for arg in result)

    def test_windows_chrome_fallback(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(platform, "system", lambda: "Windows")
        # No edge, but chrome is present.
        def fake_which(name: str) -> str | None:
            if name == "msedge.exe":
                return None
            if name == "chrome.exe":
                return "C:/chrome/chrome.exe"
            return None
        monkeypatch.setattr(shutil, "which", fake_which)
        result = artify.find_app_browser()
        assert result is not None
        assert result[0] == "C:/chrome/chrome.exe"
        assert "--app={url}" in result

    def test_macos_chrome_present(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.setattr(platform, "system", lambda: "Darwin")
        # Use a fake /Applications/Google Chrome.app — patch Path.exists for it.
        # On Windows, str(Path("/Applications/...")) is "\\Applications\\..." so
        # match by as_posix() too.
        real_path_exists = Path.exists

        def fake_exists(self: Path) -> bool:
            if self.as_posix() == "/Applications/Google Chrome.app":
                return True
            return real_path_exists(self)

        monkeypatch.setattr(Path, "exists", fake_exists)
        monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/open" if name == "open" else None)
        result = artify.find_app_browser()
        assert result is not None
        # argv template should be open -na "Google Chrome" --args --app={url}
        assert result[0] == "/usr/bin/open"
        assert "-na" in result
        assert "Google Chrome" in result
        assert "--app={url}" in result

    def test_macos_chrome_absent(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(platform, "system", lambda: "Darwin")
        real_path_exists = Path.exists

        def fake_exists(self: Path) -> bool:
            if "Google Chrome.app" in str(self):
                return False
            return real_path_exists(self)

        monkeypatch.setattr(Path, "exists", fake_exists)
        monkeypatch.setattr(shutil, "which", lambda name: None)
        assert artify.find_app_browser() is None

    def test_linux_chromium(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(platform, "system", lambda: "Linux")
        monkeypatch.setattr(
            shutil,
            "which",
            lambda name: "/usr/bin/chromium" if name == "chromium" else None,
        )
        result = artify.find_app_browser()
        assert result is not None
        assert result[0] == "/usr/bin/chromium"
        assert "--app={url}" in result

    def test_linux_returns_none_when_no_browser(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(platform, "system", lambda: "Linux")
        monkeypatch.setattr(shutil, "which", lambda name: None)
        assert artify.find_app_browser() is None

    @pytest.mark.skipif(
        platform.system() != "Windows",
        reason="Windows real-host check",
    )
    def test_real_host_windows(self) -> None:
        """On a real Windows host, find_app_browser returns a non-None list
        ONLY if msedge.exe or chrome.exe is on PATH. If neither is installed,
        it returns None and the CLI falls back gracefully — both are correct."""
        result = artify.find_app_browser()
        if shutil.which("msedge.exe") or shutil.which("chrome.exe"):
            assert result is not None
            assert any("{url}" in a for a in result)
            assert any("--app=" in a for a in result)
        else:
            # No app-mode browser on this host — must return None so the
            # CLI's open_with_browser() can fall back to webbrowser.open_new_tab.
            assert result is None


# ---------------------------------------------------------------------------
# open_in_webview
# ---------------------------------------------------------------------------


class TestOpenInWebview:
    def test_returns_true_on_successful_spawn(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(artify, "find_app_browser", lambda: ["browser.exe", "--app={url}"])
        fake_proc = mock.MagicMock()
        with mock.patch.object(artify.subprocess, "Popen", return_value=fake_proc) as popen:
            ok = artify.open_in_webview("http://localhost:1234/")
        assert ok is True
        # Verify the URL was substituted into the template.
        call = popen.call_args
        cmd = call.args[0]
        # cmd is a list of strings; check the substituted URL is in there.
        assert any("http://localhost:1234/" in a for a in cmd)
        # No {url} placeholder should remain.
        assert not any("{url}" in a for a in cmd)

    def test_returns_false_when_no_app_browser(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(artify, "find_app_browser", lambda: None)
        # Popen should never be called in this case.
        with mock.patch.object(artify.subprocess, "Popen") as popen:
            ok = artify.open_in_webview("http://localhost:1234/")
        assert ok is False
        popen.assert_not_called()

    def test_returns_false_on_oserror(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(artify, "find_app_browser", lambda: ["browser.exe", "--app={url}"])
        with mock.patch.object(
            artify.subprocess, "Popen", side_effect=OSError("boom")
        ):
            ok = artify.open_in_webview("http://localhost:1234/")
        assert ok is False


# ---------------------------------------------------------------------------
# ArtifyHandler + start_server
# ---------------------------------------------------------------------------


class TestArtifyHandler:
    def test_get_root_returns_html_with_marker(self, html_file: Path) -> None:
        server, port = _start_server_thread(html_file)
        try:
            _wait_for_port("127.0.0.1", port)
            status, headers, body = _http_get("127.0.0.1", port, "/")
            assert status == 200
            assert b"ARTIFY_RELOAD" in body
            assert b"<h1>hi</h1>" in body
            ct = headers.get("Content-Type", "")
            assert ct.startswith("text/html")
            # Cache-Control must be no-store.
            assert headers.get("Cache-Control") == "no-store"
        finally:
            server.shutdown()
            server.server_close()

    def test_get_index_html_also_works(self, html_file: Path) -> None:
        server, port = _start_server_thread(html_file)
        try:
            _wait_for_port("127.0.0.1", port)
            status, _, body = _http_get("127.0.0.1", port, "/index.html")
            assert status == 200
            assert b"ARTIFY_RELOAD" in body
        finally:
            server.shutdown()
            server.server_close()

    def test_get_reload_js(self, html_file: Path) -> None:
        server, port = _start_server_thread(html_file)
        try:
            _wait_for_port("127.0.0.1", port)
            status, headers, body = _http_get("127.0.0.1", port, "/__reload.js")
            assert status == 200
            # The content type must mention javascript. (implementation uses
            # application/javascript; charset=utf-8, which is fine.)
            ct = headers.get("Content-Type", "")
            assert "javascript" in ct.lower()
            # Body should be the RELOAD_JS constant.
            assert body.decode("utf-8") == artify.RELOAD_JS
            assert headers.get("Cache-Control") == "no-store"
        finally:
            server.shutdown()
            server.server_close()

    def test_get_reload_check_returns_float(self, html_file: Path) -> None:
        server, port = _start_server_thread(html_file)
        try:
            _wait_for_port("127.0.0.1", port)
            status, headers, body = _http_get("127.0.0.1", port, "/__reload_check")
            assert status == 200
            ct = headers.get("Content-Type", "")
            assert "text/plain" in ct
            mtime = float(body.decode("utf-8").strip())
            # mtime should be a positive number close to now.
            assert mtime > 0
            assert mtime <= time.time() + 1
        finally:
            server.shutdown()
            server.server_close()

    def test_get_unknown_returns_404(self, html_file: Path) -> None:
        server, port = _start_server_thread(html_file)
        try:
            _wait_for_port("127.0.0.1", port)
            status, _, _ = _http_get("127.0.0.1", port, "/bogus")
            assert status == 404
        finally:
            server.shutdown()
            server.server_close()

    def test_live_reload_mtime_changes(self, html_file: Path) -> None:
        server, port = _start_server_thread(html_file)
        try:
            _wait_for_port("127.0.0.1", port)
            _, _, body1 = _http_get("127.0.0.1", port, "/__reload_check")
            mtime1 = float(body1.decode("utf-8").strip())

            # Modify the file, then wait long enough for mtime resolution
            # (Windows NTFS is ~100ns but a small sleep is cheap insurance).
            time.sleep(0.05)
            html_file.write_text(
                "<!doctype html><html><body>changed</body></html>",
                encoding="utf-8",
            )

            # Re-read.
            _, _, body2 = _http_get("127.0.0.1", port, "/__reload_check")
            mtime2 = float(body2.decode("utf-8").strip())
            assert mtime2 > mtime1, f"mtime did not advance: {mtime1} -> {mtime2}"
        finally:
            server.shutdown()
            server.server_close()

    def test_idempotent_injection_across_multiple_gets(self, html_file: Path) -> None:
        server, port = _start_server_thread(html_file)
        try:
            _wait_for_port("127.0.0.1", port)
            # Hit the file 5 times. Each response must have exactly one marker.
            for _ in range(5):
                _, _, body = _http_get("127.0.0.1", port, "/")
                assert body.count(b"ARTIFY_RELOAD") == 1
        finally:
            server.shutdown()
            server.server_close()

    def test_non_html_served_without_injection(self, tmp_path: Path) -> None:
        svg = tmp_path / "logo.svg"
        svg.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg"><circle r="5"/></svg>',
            encoding="utf-8",
        )
        server, port = _start_server_thread(svg)
        try:
            _wait_for_port("127.0.0.1", port)
            status, _, body = _http_get("127.0.0.1", port, "/")
            assert status == 200
            # Script injection must not happen for non-HTML.
            assert b"ARTIFY_RELOAD" not in body
            assert b"<svg" in body
        finally:
            server.shutdown()
            server.server_close()

    def test_svg_content_type_is_image_svg_xml(self, tmp_path: Path) -> None:
        """A .svg file must be served with image/svg+xml, not text/html.

        Browsers content-sniff so the existing text/html header works in
        practice, but the correct Content-Type matters for caching, download
        behavior, and strict clients.
        """
        import mimetypes

        svg = tmp_path / "logo.svg"
        svg.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg"><circle r="5"/></svg>',
            encoding="utf-8",
        )
        # Reference value from the stdlib, so the test stays in sync with
        # whatever Python ships for .svg.
        expected, _ = mimetypes.guess_type(str(svg))
        assert expected == "image/svg+xml"

        server, port = _start_server_thread(svg)
        try:
            _wait_for_port("127.0.0.1", port)
            status, headers, body = _http_get("127.0.0.1", port, "/")
            assert status == 200
            ct = headers.get("Content-Type", "")
            assert ct.startswith("image/svg+xml"), f"unexpected Content-Type: {ct!r}"
            # And of course no script injection into the SVG body.
            assert b"<script" not in body.lower()
            assert b"ARTIFY_RELOAD" not in body
        finally:
            server.shutdown()
            server.server_close()

    def test_server_bound_to_localhost(self, html_file: Path) -> None:
        server, port = _start_server_thread(html_file)
        try:
            # Confirm server_address is bound to 127.0.0.1, not 0.0.0.0.
            assert server.server_address[0] == "127.0.0.1"
            # And we can reach it on localhost.
            _wait_for_port("127.0.0.1", port)
            status, _, _ = _http_get("127.0.0.1", port, "/")
            assert status == 200
        finally:
            server.shutdown()
            server.server_close()

    def test_reload_state_thread_safe_get_update(self, html_file: Path) -> None:
        state = artify.ReloadState(html_file)
        m0 = state.get()
        assert m0 > 0

        # bump and get from another thread concurrently.
        results: list[float] = []

        def reader() -> None:
            for _ in range(50):
                results.append(state.get())
                time.sleep(0.001)

        t = threading.Thread(target=reader, daemon=True)
        t.start()
        for _ in range(50):
            state.bump()
            state.update_from_disk()
            time.sleep(0.001)
        t.join(timeout=3)

        # We should have produced 50 reads without any exception or
        # nonsensical float. Just sanity-check: every value is a float.
        assert all(isinstance(r, float) for r in results)
        assert len(results) == 50


# ---------------------------------------------------------------------------
# Click commands (open / serve)
# ---------------------------------------------------------------------------


class TestClickOpenCommand:
    def test_open_existing_file_exits_zero(
        self, runner: click.testing.CliRunner, html_file: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        called: list[str] = []

        def fake_open(url: str) -> bool:
            called.append(url)
            return True

        monkeypatch.setattr(artify.webbrowser, "open_new_tab", fake_open)
        result = runner.invoke(artify.main, ["open", str(html_file)])
        assert result.exit_code == 0, result.output
        assert len(called) == 1
        # The URL must be a file:// URL pointing to the resolved path.
        url = called[0]
        assert url.startswith("file:///")
        # On Windows the resolved path uses backslashes in as_posix -> forward slashes
        assert html_file.resolve().as_posix() in url

    def test_open_missing_file_exits_nonzero(
        self, runner: click.testing.CliRunner, tmp_path: Path
    ) -> None:
        missing = tmp_path / "does_not_exist.html"
        result = runner.invoke(artify.main, ["open", str(missing)])
        # Click exits with 2 for invalid argument values (e.g. exists=True check).
        # The plan said "exits 1" but the actual behavior is Click's standard 2.
        assert result.exit_code != 0
        # Error message must mention the missing file in some recognizable form.
        combined = (result.output + (result.stderr or "")).lower()
        assert "does not exist" in combined or "invalid" in combined

    def test_open_prints_url(
        self, runner: click.testing.CliRunner, html_file: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(artify.webbrowser, "open_new_tab", lambda url: True)
        result = runner.invoke(artify.main, ["open", str(html_file)])
        assert result.exit_code == 0
        # The URL should be echoed in stdout for the user to see.
        assert "Opening:" in result.output
        assert "file:///" in result.output

    def test_open_handles_browser_failure(
        self, runner: click.testing.CliRunner, html_file: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # If webbrowser.open_new_tab returns False, the CLI should exit non-zero.
        monkeypatch.setattr(artify.webbrowser, "open_new_tab", lambda url: False)
        result = runner.invoke(artify.main, ["open", str(html_file)])
        assert result.exit_code != 0


class TestClickServeCommand:
    def test_serve_help_shows_webview_option(
        self, runner: click.testing.CliRunner
    ) -> None:
        result = runner.invoke(artify.main, ["serve", "--help"])
        assert result.exit_code == 0
        assert "--webview" in result.output

    def test_serve_missing_file_exits_nonzero_before_starting(
        self, runner: click.testing.CliRunner, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        missing = tmp_path / "nope.html"
        # If serve actually tried to start, webbrowser.open_new_tab would be
        # called. Patch it to assert it is NOT called.
        called: list[str] = []

        def fake_open(url: str) -> bool:
            called.append(url)
            return True

        monkeypatch.setattr(artify.webbrowser, "open_new_tab", fake_open)
        result = runner.invoke(artify.main, ["serve", str(missing)])
        assert result.exit_code != 0
        # Browser must not have been opened.
        assert called == []
        # Some recognizable error.
        combined = (result.output + (result.stderr or "")).lower()
        assert "does not exist" in combined or "invalid" in combined

    def test_serve_starts_and_url_appears_in_output(
        self,
        runner: click.testing.CliRunner,
        html_file: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Smoke test: serve starts, prints URL, then we simulate Ctrl+C."""

        def fake_serve_forever(self):  # type: ignore[no-untyped-def]
            raise KeyboardInterrupt

        # TCPServer overrides server_close, so patch on both BaseServer
        # and TCPServer to be safe.
        monkeypatch.setattr(socketserver.BaseServer, "serve_forever", fake_serve_forever)
        monkeypatch.setattr(socketserver.TCPServer, "serve_forever", fake_serve_forever)
        monkeypatch.setattr(socketserver.BaseServer, "shutdown", lambda self: None)
        monkeypatch.setattr(socketserver.TCPServer, "server_close", lambda self: None)
        monkeypatch.setattr(artify.webbrowser, "open_new_tab", lambda url: True)

        result = runner.invoke(artify.main, ["serve", str(html_file)])
        # KeyboardInterrupt is swallowed by the try/except; the command exits 0.
        assert result.exit_code == 0, result.output
        # URL printed in stdout.
        assert "Serving:" in result.output
        assert "http://localhost:" in result.output
        # The serve_forever patch means watchdog's observer is started but
        # serve_forever returns immediately. (watch_and_serve imports
        # watchdog lazily INSIDE the function.) The observer is then stopped
        # in the inner finally and the command's outer finally runs.

    def test_serve_keyboard_interrupt_cleanly_stops(
        self,
        runner: click.testing.CliRunner,
        html_file: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Ctrl+C (KeyboardInterrupt) is caught and a friendly 'Stopping...' is printed."""

        def fake_serve_forever(self):  # type: ignore[no-untyped-def]
            raise KeyboardInterrupt

        monkeypatch.setattr(socketserver.BaseServer, "serve_forever", fake_serve_forever)
        monkeypatch.setattr(socketserver.TCPServer, "serve_forever", fake_serve_forever)

        # Capture the actual server instance so we can assert on its
        # shutdown/server_close flag after the Click command finishes.
        # We instrument the instance methods directly — patching the
        # class doesn't work for server_close because TCPServer overrides
        # it. The tracked methods are no-ops (we don't want to actually
        # call the real shutdown: it would block on __is_shut_down.wait()
        # because our fake serve_forever raises before signalling shutdown).
        captured: dict[str, object] = {}

        original_start_server = artify.start_server

        def instrumented_start_server(path: Path):  # type: ignore[no-untyped-def]
            server, port, state = original_start_server(path)
            captured["server"] = server

            def tracked_shutdown() -> None:
                captured["shutdown_called"] = True

            def tracked_server_close() -> None:
                captured["server_close_called"] = True

            server.shutdown = tracked_shutdown  # type: ignore[method-assign]
            server.server_close = tracked_server_close  # type: ignore[method-assign]
            return server, port, state

        monkeypatch.setattr(artify, "start_server", instrumented_start_server)
        monkeypatch.setattr(artify.webbrowser, "open_new_tab", lambda url: True)

        result = runner.invoke(artify.main, ["serve", str(html_file)])
        assert result.exit_code == 0
        assert "Stopping" in result.output
        # server.shutdown() and server.server_close() must have been called
        # via the Click command's finally block. We assert by reading the
        # tracked flags captured by the instrumented server instance.
        assert captured.get("shutdown_called") is True
        assert captured.get("server_close_called") is True


# ---------------------------------------------------------------------------
# Top-level CLI sanity
# ---------------------------------------------------------------------------


class TestMainGroup:
    def test_main_help_lists_open_and_serve(
        self, runner: click.testing.CliRunner
    ) -> None:
        result = runner.invoke(artify.main, ["--help"])
        assert result.exit_code == 0
        assert "open" in result.output
        assert "serve" in result.output

    def test_main_version(self, runner: click.testing.CliRunner) -> None:
        result = runner.invoke(artify.main, ["--version"])
        assert result.exit_code == 0
        # Should print "artify" and a version.
        assert "artify" in result.output.lower()


# ---------------------------------------------------------------------------
# Helpers shared by the new (list/kill/restart/snapshot) tests
# ---------------------------------------------------------------------------


@pytest.fixture
def redirected_registry(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Point artify.REGISTRY_DIR at a per-test temp directory.

    Returns the (Path) so tests can read/write/inspect entries directly.
    """
    reg = tmp_path / "instances"
    reg.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(artify, "REGISTRY_DIR", reg)
    return reg


def _start_server_thread_with_timeout(
    path: Path,
    snapshot_timeout: float = 5.0,
) -> tuple[socketserver.TCPServer, int, artify.InstanceState]:
    """Same as _start_server_thread but lets tests pick the snapshot timeout."""
    server, port, state = artify.start_server(path, snapshot_timeout=snapshot_timeout)
    t = threading.Thread(target=server.serve_forever, name="artify-test-server", daemon=True)
    t.start()
    return server, port, state


def _http_post(
    host: str,
    port: int,
    path: str,
    body: bytes = b"",
    headers: dict | None = None,
    timeout: float = 5.0,
) -> tuple[int, dict, bytes]:
    """Make a POST to a real port. Returns (status, headers, body)."""
    h = {"Content-Length": str(len(body))} if body else {}
    if headers:
        h.update(headers)
    conn = http.client.HTTPConnection(host, port, timeout=timeout)
    try:
        conn.request("POST", path, body=body, headers=h)
        resp = conn.getresponse()
        out_headers = {k: v for k, v in resp.getheaders()}
        return resp.status, out_headers, resp.read()
    finally:
        conn.close()


def _http_post_json(
    host: str,
    port: int,
    path: str,
    obj: dict,
    timeout: float = 5.0,
) -> tuple[int, dict, bytes]:
    body = json.dumps(obj).encode("utf-8")
    return _http_post(
        host,
        port,
        path,
        body=body,
        headers={"Content-Type": "application/json"},
        timeout=timeout,
    )


def _start_dummy_serve_subprocess(
    reg_dir: Path,
    html_file: Path,
    port_to_register: int | None = None,
) -> subprocess.Popen:
    """Start a real subprocess that acts as a 'serve' instance for kill/restart tests.

    The subprocess:
      - patches webbrowser.open_new_tab to a no-op
      - points artify.REGISTRY_DIR at reg_dir
      - writes a registry entry for itself and sleeps

    The caller is responsible for writing the registry entry (we return the
    Popen so the caller can decide what port/pid to register). The subprocess
    does NOT bind an HTTP port; it just sits there so kill/restart can target
    its PID.

    Returns the Popen handle. The caller MUST .terminate() it for cleanup.
    """
    # A tiny "fake serve" script. We don't bind an HTTP port because the
    # tests for kill/restart only care about the process lifecycle.
    script = (
        "import os, sys, time, signal\n"
        "import webbrowser\n"
        "webbrowser.open_new_tab = lambda *a, **k: True\n"
        "import artify_cli.cli as a\n"
        "from pathlib import Path\n"
        "a.REGISTRY_DIR = Path(r'%s')\n"
        "# Just sleep until SIGTERM. The test process writes the registry\n"
        "# entry; we don't auto-register so the test can control the data.\n"
        "signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))\n"
        "time.sleep(120)\n"
    ) % (str(reg_dir),)
    creationflags = 0x00000008 | 0x00000200 if sys.platform == "win32" else 0
    return subprocess.Popen(
        [sys.executable, "-c", script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=creationflags,
    )


# ---------------------------------------------------------------------------
# is_pid_alive
# ---------------------------------------------------------------------------


class TestIsPidAlive:
    def test_true_for_self(self) -> None:
        assert artify.is_pid_alive(os.getpid()) is True

    def test_false_for_definitely_dead_pid(self) -> None:
        # 99999999 is way above any reasonable PID on Windows / Linux.
        assert artify.is_pid_alive(99999999) is False

    def test_bogus_string_returns_false(self) -> None:
        assert artify.is_pid_alive("not-a-pid") is False  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Registry helpers
# ---------------------------------------------------------------------------


class TestRegistryHelpers:
    def test_read_empty_when_dir_missing(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        # REGISTRY_DIR points to a path that does NOT exist.
        monkeypatch.setattr(artify, "REGISTRY_DIR", tmp_path / "nope")
        assert artify.read_registry() == []

    def test_read_returns_empty_when_dir_exists_but_no_files(
        self, redirected_registry: Path
    ) -> None:
        assert artify.read_registry() == []

    def test_write_creates_file_with_expected_fields(
        self, redirected_registry: Path, tmp_path: Path
    ) -> None:
        html = tmp_path / "x.html"
        html.write_text("<html></html>", encoding="utf-8")
        artify.write_registry_entry(12345, os.getpid(), html)
        target = redirected_registry / "12345.json"
        assert target.is_file()
        payload = json.loads(target.read_text(encoding="utf-8"))
        assert payload["port"] == 12345
        assert payload["pid"] == os.getpid()
        assert payload["file"].replace("/", os.sep).endswith("x.html")
        assert "started_at" in payload

    def test_write_is_atomic_no_tmp_left(
        self, redirected_registry: Path, tmp_path: Path
    ) -> None:
        html = tmp_path / "y.html"
        html.write_text("<html></html>", encoding="utf-8")
        artify.write_registry_entry(22222, os.getpid(), html)
        # No leftover .tmp files.
        leftovers = list(redirected_registry.glob("*.json.tmp"))
        assert leftovers == []

    def test_read_augments_with_alive_field(
        self, redirected_registry: Path, tmp_path: Path
    ) -> None:
        html = tmp_path / "z.html"
        html.write_text("<html></html>", encoding="utf-8")
        artify.write_registry_entry(33000, os.getpid(), html)  # live
        artify.write_registry_entry(33001, 99999999, html)  # dead
        entries = artify.read_registry()
        assert len(entries) == 2
        by_port = {e["port"]: e for e in entries}
        assert by_port[33000]["alive"] is True
        assert by_port[33001]["alive"] is False

    def test_read_sorted_by_port(
        self, redirected_registry: Path, tmp_path: Path
    ) -> None:
        html = tmp_path / "s.html"
        html.write_text("<html></html>", encoding="utf-8")
        # Insert in non-sorted order.
        artify.write_registry_entry(55555, os.getpid(), html)
        artify.write_registry_entry(11111, os.getpid(), html)
        artify.write_registry_entry(33333, os.getpid(), html)
        ports = [e["port"] for e in artify.read_registry()]
        assert ports == [11111, 33333, 55555]

    def test_remove_silent_on_missing(
        self, redirected_registry: Path
    ) -> None:
        # No entry exists; should not raise.
        artify.remove_registry_entry(77777)
        assert list(redirected_registry.iterdir()) == []

    def test_roundtrip_write_read_remove(
        self, redirected_registry: Path, tmp_path: Path
    ) -> None:
        html = tmp_path / "rt.html"
        html.write_text("<html></html>", encoding="utf-8")
        artify.write_registry_entry(40000, os.getpid(), html)
        assert any(e["port"] == 40000 for e in artify.read_registry())
        artify.remove_registry_entry(40000)
        assert not (redirected_registry / "40000.json").exists()
        assert not any(e["port"] == 40000 for e in artify.read_registry())

    def test_read_skips_corrupt_files(
        self, redirected_registry: Path
    ) -> None:
        (redirected_registry / "11111.json").write_text("not json", encoding="utf-8")
        assert artify.read_registry() == []

    def test_remove_registry_entry_idempotent(
        self, redirected_registry: Path, tmp_path: Path
    ) -> None:
        html = tmp_path / "id.html"
        html.write_text("<html></html>", encoding="utf-8")
        artify.write_registry_entry(50000, os.getpid(), html)
        artify.remove_registry_entry(50000)
        artify.remove_registry_entry(50000)  # second call must be silent
        assert not (redirected_registry / "50000.json").exists()


# ---------------------------------------------------------------------------
# InstanceState: command queue + snapshot registry
# ---------------------------------------------------------------------------


class TestInstanceStateSnapshot:
    def test_enqueue_and_drain_commands(self, html_file: Path) -> None:
        state = artify.InstanceState(html_file, snapshot_timeout=1.0)
        assert state.drain_commands() == []
        state.enqueue_command({"type": "snapshot", "id": "a"})
        state.enqueue_command({"type": "snapshot", "id": "b"})
        out = state.drain_commands()
        assert [c["id"] for c in out] == ["a", "b"]
        # Queue is empty after drain.
        assert state.drain_commands() == []

    def test_register_snapshot_unknown_id_returns_none(
        self, html_file: Path
    ) -> None:
        state = artify.InstanceState(html_file, snapshot_timeout=1.0)
        assert state.wait_for_snapshot("missing") is None

    def test_set_snapshot_result_unknown_id_returns_false(
        self, html_file: Path
    ) -> None:
        state = artify.InstanceState(html_file, snapshot_timeout=1.0)
        assert state.set_snapshot_result("nope", {"fields": {}}) is False

    def test_set_snapshot_result_signals_waiter(
        self, html_file: Path
    ) -> None:
        state = artify.InstanceState(html_file, snapshot_timeout=2.0)
        event = state.register_snapshot("abc")
        assert state.set_snapshot_result("abc", {"fields": {"x": 1}}) is True
        assert event.wait(timeout=1) is True
        result = state.wait_for_snapshot("abc", timeout=0.1)
        assert result == {"fields": {"x": 1}}

    def test_wait_for_snapshot_timeout_returns_none_and_cleans_up(
        self, html_file: Path
    ) -> None:
        state = artify.InstanceState(html_file, snapshot_timeout=0.1)
        state.register_snapshot("timeout-id")
        # Don't signal; wait should time out.
        result = state.wait_for_snapshot("timeout-id", timeout=0.1)
        assert result is None
        # After timeout the slot is cleaned up: a second wait is also None
        # and set_snapshot_result returns False.
        assert state.wait_for_snapshot("timeout-id", timeout=0.1) is None
        assert state.set_snapshot_result("timeout-id", {"fields": {}}) is False


# ---------------------------------------------------------------------------
# /__commands endpoint
# ---------------------------------------------------------------------------


class TestCommandsEndpoint:
    def test_get_returns_empty_array_when_no_commands(
        self, html_file: Path
    ) -> None:
        server, port, _state = _start_server_thread_with_timeout(html_file)
        try:
            _wait_for_port("127.0.0.1", port)
            status, _, body = _http_get("127.0.0.1", port, "/__commands")
            assert status == 200
            assert json.loads(body) == []
        finally:
            server.shutdown()
            server.server_close()

    def test_get_drains_enqueued_commands(self, html_file: Path) -> None:
        server, port, state = _start_server_thread_with_timeout(html_file)
        try:
            _wait_for_port("127.0.0.1", port)
            # Enqueue directly on the state (simulates /__snapshot_request).
            state.enqueue_command({"type": "snapshot", "id": "q1"})
            state.enqueue_command({"type": "snapshot", "id": "q2"})

            status, _, body = _http_get("127.0.0.1", port, "/__commands")
            assert status == 200
            cmds = json.loads(body)
            assert [c["id"] for c in cmds] == ["q1", "q2"]

            # Second call drains the now-empty queue.
            status, _, body = _http_get("127.0.0.1", port, "/__commands")
            assert status == 200
            assert json.loads(body) == []
        finally:
            server.shutdown()
            server.server_close()


# ---------------------------------------------------------------------------
# /__snapshot_request and /__snapshot_result endpoints
# ---------------------------------------------------------------------------


class TestSnapshotRequestBlocks:
    def test_request_blocks_until_result_arrives(
        self, html_file: Path
    ) -> None:
        server, port, state = _start_server_thread_with_timeout(html_file, snapshot_timeout=5.0)
        try:
            _wait_for_port("127.0.0.1", port)

            result: dict = {}
            ready = threading.Event()

            def post_request() -> None:
                status, _, body = _http_post(
                    "127.0.0.1", port, "/__snapshot_request", body=b""
                )
                result["status"] = status
                result["body"] = body.decode("utf-8")
                ready.set()

            t = threading.Thread(target=post_request, daemon=True)
            t.start()

            # Give the request a beat to land in wait_for_snapshot.
            time.sleep(0.2)
            assert not ready.is_set(), "request returned before the result was posted"

            # Find the snapshot id the server allocated.
            with state.results_lock:
                sids = list(state.pending_snapshots.keys())
            assert len(sids) == 1
            sid = sids[0]

            # Now post the result.
            status, _, body = _http_post_json(
                "127.0.0.1",
                port,
                "/__snapshot_result/" + sid,
                {"fields": {"hello": "world"}},
            )
            assert status == 200
            assert json.loads(body) == {"ok": True}

            assert ready.wait(timeout=3)
            assert result["status"] == 200
            assert json.loads(result["body"]) == {"fields": {"hello": "world"}}
        finally:
            server.shutdown()
            server.server_close()


class TestSnapshotResultErrors:
    def test_unknown_id_returns_404(self, html_file: Path) -> None:
        server, port, _state = _start_server_thread_with_timeout(html_file)
        try:
            _wait_for_port("127.0.0.1", port)
            status, _, body = _http_post_json(
                "127.0.0.1", port, "/__snapshot_result/nope", {"fields": {}}
            )
            assert status == 404
            assert json.loads(body) == {"error": "unknown snapshot id"}
        finally:
            server.shutdown()
            server.server_close()

    def test_invalid_json_returns_400(self, html_file: Path) -> None:
        server, port, state = _start_server_thread_with_timeout(html_file)
        try:
            _wait_for_port("127.0.0.1", port)
            # Pre-register a valid id so the JSON parse is what fails,
            # not the unknown-id check.
            state.register_snapshot("valid-id")
            status, _, body = _http_post(
                "127.0.0.1",
                port,
                "/__snapshot_result/valid-id",
                body=b"this is { not json",
                headers={"Content-Type": "application/json"},
            )
            assert status == 400
            assert json.loads(body) == {"error": "invalid json body"}
        finally:
            server.shutdown()
            server.server_close()


# ---------------------------------------------------------------------------
# Threaded server: a blocked /__snapshot_request must not freeze /__commands
# ---------------------------------------------------------------------------


class TestThreadedServer:
    def test_commands_endpoint_responds_during_blocked_snapshot(
        self, html_file: Path
    ) -> None:
        """Regression: if the server were single-threaded, the blocked
        /__snapshot_request would freeze every other endpoint. The
        ThreadingMixIn change is the fix; this test guards it.
        """
        server, port, state = _start_server_thread_with_timeout(
            html_file, snapshot_timeout=5.0
        )
        try:
            _wait_for_port("127.0.0.1", port)

            # Kick off a snapshot request in a thread; it will block.
            snapshot_done = threading.Event()
            snapshot_result: dict = {}

            def blocking_snapshot() -> None:
                status, _, body = _http_post(
                    "127.0.0.1", port, "/__snapshot_request", body=b""
                )
                snapshot_result["status"] = status
                snapshot_result["body"] = body.decode("utf-8")
                snapshot_done.set()

            t = threading.Thread(target=blocking_snapshot, daemon=True)
            t.start()

            # Give the request a beat to enter the wait.
            time.sleep(0.2)

            # /__commands must respond promptly while the snapshot is blocked.
            t0 = time.monotonic()
            status, _, body = _http_get("127.0.0.1", port, "/__commands")
            commands_time = time.monotonic() - t0

            assert status == 200
            assert commands_time < 1.0, (
                f"/__commands took {commands_time:.3f}s while /__snapshot_request "
                f"was blocked — server is not properly threaded"
            )
            cmds = json.loads(body)
            assert any(c.get("type") == "snapshot" for c in cmds), (
                "the snapshot command should be visible to the page"
            )

            # Unblock the snapshot.
            with state.results_lock:
                sids = list(state.pending_snapshots.keys())
            if sids:
                _http_post_json(
                    "127.0.0.1",
                    port,
                    "/__snapshot_result/" + sids[0],
                    {"fields": {"answer": 42}},
                )

            assert snapshot_done.wait(timeout=3)
            assert snapshot_result["status"] == 200
        finally:
            server.shutdown()
            server.server_close()


# ---------------------------------------------------------------------------
# Click: artify list
# ---------------------------------------------------------------------------


class TestClickListCommand:
    def test_empty_registry_prints_message_and_exits_zero(
        self, runner: click.testing.CliRunner, redirected_registry: Path
    ) -> None:
        assert list(redirected_registry.iterdir()) == []
        result = runner.invoke(artify.main, ["list"])
        assert result.exit_code == 0, result.output
        assert "No artify instances running." in result.output

    def test_list_with_multiple_entries_contains_all_ports(
        self,
        runner: click.testing.CliRunner,
        redirected_registry: Path,
        tmp_path: Path,
    ) -> None:
        f1 = tmp_path / "a.html"
        f1.write_text("<html></html>", encoding="utf-8")
        f2 = tmp_path / "b.html"
        f2.write_text("<html></html>", encoding="utf-8")
        artify.write_registry_entry(41000, os.getpid(), f1)
        artify.write_registry_entry(42000, os.getpid(), f2)
        # Force a wide terminal so Rich doesn't truncate the URL column.
        wide_env = dict(os.environ)
        wide_env["COLUMNS"] = "200"
        result = runner.invoke(artify.main, ["list"], env=wide_env)
        assert result.exit_code == 0, result.output
        # All ports are listed.
        for port in ("41000", "42000"):
            assert port in result.output, f"port {port} missing from list output"
        # Status is "running" for the live one.
        assert "running" in result.output
        # URL is shown (with the wide terminal, Rich renders it in full).
        assert "http://127.0.0.1:41000/" in result.output
        assert "http://127.0.0.1:42000/" in result.output

    def test_list_marks_dead_entries(
        self,
        runner: click.testing.CliRunner,
        redirected_registry: Path,
        tmp_path: Path,
    ) -> None:
        f1 = tmp_path / "live.html"
        f1.write_text("<html></html>", encoding="utf-8")
        artify.write_registry_entry(43100, os.getpid(), f1)         # live
        artify.write_registry_entry(43200, 99999999, f1)            # dead
        result = runner.invoke(artify.main, ["list"])
        assert result.exit_code == 0, result.output
        # Both ports present.
        assert "43100" in result.output
        assert "43200" in result.output
        # "running" and "dead" both appear.
        assert "running" in result.output
        assert "dead" in result.output
        # The dead entry should NOT have a URL — the implementation prints
        # "-" for the URL of a dead row.
        # We check by making sure the dead port does not have a URL.
        # The line for 43200 should contain "-" in the URL slot.
        for line in result.output.splitlines():
            if "43200" in line:
                assert "http://127.0.0.1:43200" not in line, (
                    f"dead entry should not show a URL, got: {line!r}"
                )

    def test_list_help(self, runner: click.testing.CliRunner) -> None:
        result = runner.invoke(artify.main, ["list", "--help"])
        assert result.exit_code == 0
        assert "List running artify" in result.output


# ---------------------------------------------------------------------------
# Click: artify kill
# ---------------------------------------------------------------------------


class TestClickKillCommand:
    def test_unknown_port_exits_1(
        self, runner: click.testing.CliRunner, redirected_registry: Path
    ) -> None:
        # 59999 is in the valid 1..65535 range but has no entry.
        result = runner.invoke(artify.main, ["kill", "59999"])
        assert result.exit_code == 1, result.output
        combined = (result.output + (result.stderr or "")).lower()
        assert "no artify instance on port 59999" in combined

    def test_kill_terminates_real_process_and_removes_entry(
        self,
        runner: click.testing.CliRunner,
        redirected_registry: Path,
        tmp_path: Path,
    ) -> None:
        # Start a real (dummy) serve subprocess we can terminate.
        html = tmp_path / "k.html"
        html.write_text("<html></html>", encoding="utf-8")
        proc = _start_dummy_serve_subprocess(redirected_registry, html)
        try:
            # Wait for the subprocess to be alive.
            deadline = time.time() + 5
            while time.time() < deadline and proc.poll() is not None:
                time.sleep(0.05)
            assert proc.poll() is None, "dummy serve exited before kill"

            # Register it (the test does this, not the subprocess).
            artify.write_registry_entry(55000, proc.pid, html)
            assert (redirected_registry / "55000.json").is_file()

            # Run the kill command.
            result = runner.invoke(artify.main, ["kill", "55000"])
            assert result.exit_code == 0, result.output

            # Registry file is gone.
            assert not (redirected_registry / "55000.json").exists()

            # Process is actually terminated (allow a moment for the OS).
            deadline = time.time() + 5
            while time.time() < deadline and proc.poll() is None:
                time.sleep(0.05)
            assert proc.poll() is not None, "kill did not terminate the process"
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except Exception:
                    proc.kill()

    def test_kill_success_message_includes_pid(
        self,
        runner: click.testing.CliRunner,
        redirected_registry: Path,
        tmp_path: Path,
    ) -> None:
        """The plan specifies 'Killed artify instance on port N (pid P)' on success.

        NOTE: current production code prints 'was already not running' even after
        a successful kill — see BUG note in the report. This test pins the
        expected success message and will fail until the bug is fixed.
        """
        html = tmp_path / "k2.html"
        html.write_text("<html></html>", encoding="utf-8")
        proc = _start_dummy_serve_subprocess(redirected_registry, html)
        try:
            deadline = time.time() + 5
            while time.time() < deadline and proc.poll() is not None:
                time.sleep(0.05)
            assert proc.poll() is None

            artify.write_registry_entry(55100, proc.pid, html)
            result = runner.invoke(artify.main, ["kill", "55100"])
            assert result.exit_code == 0, result.output
            # The plan-specified success message.
            assert f"Killed artify instance on port 55100 (pid {proc.pid})" in result.output
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except Exception:
                    proc.kill()

    def test_kill_already_dead_pid_still_cleans_up(
        self,
        runner: click.testing.CliRunner,
        redirected_registry: Path,
        tmp_path: Path,
    ) -> None:
        html = tmp_path / "d.html"
        html.write_text("<html></html>", encoding="utf-8")
        # Dead PID.
        artify.write_registry_entry(56000, 99999999, html)
        assert (redirected_registry / "56000.json").is_file()

        result = runner.invoke(artify.main, ["kill", "56000"])
        assert result.exit_code == 0, result.output
        # The friendly "already not running" message.
        combined = (result.output + (result.stderr or "")).lower()
        assert "already" in combined
        # Registry is cleaned up regardless.
        assert not (redirected_registry / "56000.json").exists()

    def test_kill_help(self, runner: click.testing.CliRunner) -> None:
        result = runner.invoke(artify.main, ["kill", "--help"])
        assert result.exit_code == 0
        assert "Kill the artify serve" in result.output


# ---------------------------------------------------------------------------
# Click: artify restart
# ---------------------------------------------------------------------------


class TestClickRestartCommand:
    def test_unknown_port_exits_1(
        self, runner: click.testing.CliRunner, redirected_registry: Path
    ) -> None:
        result = runner.invoke(artify.main, ["restart", "59999"])
        assert result.exit_code == 1, result.output
        combined = (result.output + (result.stderr or "")).lower()
        assert "no artify instance on port 59999" in combined

    def test_restart_kills_old_and_spawns_new(
        self,
        runner: click.testing.CliRunner,
        redirected_registry: Path,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        # Start a dummy serve subprocess that we can kill.
        html = tmp_path / "r.html"
        html.write_text("<html></html>", encoding="utf-8")
        old_proc = _start_dummy_serve_subprocess(redirected_registry, html)
        # Picked a port to register; use a high one unlikely to collide.
        old_port = 57000
        # Initialize before the try so the finally block can safely access
        # it even if an early assertion fails.
        new_proc_holder: dict = {}
        try:
            # Wait for the old subprocess to actually be running.
            deadline = time.time() + 5
            while time.time() < deadline and old_proc.poll() is not None:
                time.sleep(0.05)
            assert old_proc.poll() is None, "dummy serve exited prematurely"

            # Register it.
            artify.write_registry_entry(old_port, old_proc.pid, html)
            assert (redirected_registry / f"{old_port}.json").is_file()

            # The Click `restart` command spawns a real subprocess via
            # subprocess.Popen. We patch it so the new instance:
            #   1. does not try to open a browser, and
            #   2. writes its registry entry into our temp REGISTRY_DIR.
            # This keeps the test self-contained without needing a browser
            # or modifying production code.
            real_popen = subprocess.Popen  # capture real Popen before patching

            def fake_popen(cmd, **kwargs):  # type: ignore[no-untyped-def]
                # Verify the command shape — restart should be invoking
                # `artify serve <file>` with sys.executable.
                assert isinstance(cmd, list)
                assert cmd[0] == sys.executable
                assert cmd[1:3] == ["-m", "artify_cli"]
                assert cmd[3] == "serve"
                assert str(html) in cmd[4]
                # Spawn a fake "serve" that just writes a registry entry
                # into our temp REGISTRY_DIR and sleeps.
                script = (
                    "import os, sys, time, signal\n"
                    "import webbrowser\n"
                    "webbrowser.open_new_tab = lambda *a, **k: True\n"
                    "import artify_cli.cli as a\n"
                    "from pathlib import Path\n"
                    "a.REGISTRY_DIR = Path(r'%s')\n"
                    # Pick a free port and pretend to serve.
                    "import socket\n"
                    "s = socket.socket(); s.bind(('127.0.0.1', 0))\n"
                    "port = s.getsockname()[1]\n"
                    "s.close()\n"
                    "a.write_registry_entry(port, os.getpid(), Path(r'%s'))\n"
                    "signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))\n"
                    "time.sleep(120)\n"
                ) % (str(redirected_registry), str(html))
                creationflags = (
                    0x00000008 | 0x00000200 if sys.platform == "win32" else 0
                )
                p = real_popen(  # use the captured real Popen, not the patched one
                    [sys.executable, "-c", script],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    creationflags=creationflags,
                )
                new_proc_holder["proc"] = p
                return p

            monkeypatch.setattr(artify.subprocess, "Popen", fake_popen)

            result = runner.invoke(artify.main, ["restart", str(old_port)])
            assert result.exit_code == 0, result.output
            assert "Restarted" in result.output or "restarted" in result.output.lower()

            # Old process is dead.
            deadline = time.time() + 5
            while time.time() < deadline and old_proc.poll() is None:
                time.sleep(0.05)
            assert old_proc.poll() is not None, "restart did not kill the old process"

            # Old registry entry is gone.
            assert not (redirected_registry / f"{old_port}.json").exists()

            # New subprocess is running.
            new_proc = new_proc_holder.get("proc")
            assert new_proc is not None
            deadline = time.time() + 5
            while time.time() < deadline and new_proc.poll() is not None:
                time.sleep(0.05)
            assert new_proc.poll() is None, "new serve subprocess died"

            # New registry entry exists, with a different PID and a different
            # port, for the same file.
            # Poll up to 3s for the subprocess to write its entry, since
            # the import + registry write takes a moment in a fresh Python.
            deadline = time.time() + 3
            live: list = []
            while time.time() < deadline:
                entries = artify.read_registry()
                live = [e for e in entries if e.get("alive")]
                if live:
                    break
                time.sleep(0.1)
            assert len(live) == 1
            entry = live[0]
            assert entry["pid"] != old_proc.pid
            assert entry["port"] != old_port
            assert Path(entry["file"]).resolve() == html.resolve()
        finally:
            if old_proc.poll() is None:
                old_proc.terminate()
                try:
                    old_proc.wait(timeout=3)
                except Exception:
                    old_proc.kill()
            new_proc = new_proc_holder.get("proc")
            if new_proc is not None and new_proc.poll() is None:
                new_proc.terminate()
                try:
                    new_proc.wait(timeout=3)
                except Exception:
                    new_proc.kill()

    def test_restart_file_no_longer_exists_exits_1(
        self,
        runner: click.testing.CliRunner,
        redirected_registry: Path,
        tmp_path: Path,
    ) -> None:
        # Register a file path that does not exist.
        missing = tmp_path / "deleted.html"
        # No write — just the registry entry.
        artify.write_registry_entry(58000, 99999999, missing)
        result = runner.invoke(artify.main, ["restart", "58000"])
        assert result.exit_code == 1, result.output
        combined = (result.output + (result.stderr or "")).lower()
        assert "no longer exists" in combined or "missing" in combined

    def test_restart_help(self, runner: click.testing.CliRunner) -> None:
        result = runner.invoke(artify.main, ["restart", "--help"])
        assert result.exit_code == 0
        # The Click docstring starts with "Kill the artify instance on PORT..."
        assert "Kill the artify instance" in result.output
        # And mentions the port argument.
        assert "PORT" in result.output


# ---------------------------------------------------------------------------
# Click: artify snapshot
# ---------------------------------------------------------------------------


class TestClickSnapshotCommand:
    def test_unknown_port_exits_1(
        self, runner: click.testing.CliRunner
    ) -> None:
        # 59999 is a valid port with nothing listening.
        result = runner.invoke(artify.main, ["snapshot", "59999"])
        assert result.exit_code == 1, result.output
        combined = (result.output + (result.stderr or "")).lower()
        assert "no artify instance on port 59999" in combined

    def test_end_to_end_with_simulated_page(
        self,
        runner: click.testing.CliRunner,
        tmp_path: Path,
    ) -> None:
        """Start a real server with a real HTML form file, simulate the
        page in a thread that polls /__commands and POSTs the form data,
        then run `artify snapshot <port>` via CliRunner and assert the
        returned JSON matches the page's data.
        """
        html = tmp_path / "form.html"
        html.write_text(
            (
                "<!doctype html><html><body>\n"
                "<form>\n"
                '<input name="name" value="alice">\n'
                '<input name="email" value="a@example.com">\n'
                "</form>\n"
                "</body></html>\n"
            ),
            encoding="utf-8",
        )

        server, port, _state = _start_server_thread_with_timeout(
            html, snapshot_timeout=5.0
        )
        poller_stop = threading.Event()
        try:
            _wait_for_port("127.0.0.1", port)

            def simulate_page() -> None:
                while not poller_stop.is_set():
                    try:
                        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=1)
                        conn.request("GET", "/__commands")
                        resp = conn.getresponse()
                        cmds = json.loads(resp.read())
                        conn.close()
                    except Exception:
                        time.sleep(0.1)
                        continue
                    for cmd in cmds:
                        if cmd.get("type") == "snapshot":
                            sid = cmd["id"]
                            # Default collector behavior: emit hard-coded
                            # values as if the user had filled the form.
                            data = {"name": "alice", "email": "a@example.com"}
                            conn = http.client.HTTPConnection(
                                "127.0.0.1", port, timeout=2
                            )
                            conn.request(
                                "POST",
                                "/__snapshot_result/" + sid,
                                body=json.dumps({"fields": data}).encode("utf-8"),
                                headers={"Content-Type": "application/json"},
                            )
                            r = conn.getresponse()
                            r.read()
                            conn.close()
                            return  # one-shot

            poller = threading.Thread(target=simulate_page, daemon=True)
            poller.start()

            # Run snapshot via the Click command. The server's snapshot
            # timeout is 5s; the CLI --timeout is 10s so the server-side
            # 408 would still surface as a 1-exit before the CLI times out.
            result = runner.invoke(
                artify.main, ["snapshot", str(port), "--timeout", "10"]
            )
            assert result.exit_code == 0, (
                f"snapshot exited {result.exit_code}: "
                f"stdout={result.output!r} stderr={result.stderr!r}"
            )

            # The output should be the JSON we expect.
            payload = json.loads(result.output)
            assert "fields" in payload
            assert payload["fields"] == {
                "name": "alice",
                "email": "a@example.com",
            }
        finally:
            poller_stop.set()
            server.shutdown()
            server.server_close()

    def test_timeout_when_page_never_responds(
        self,
        runner: click.testing.CliRunner,
        tmp_path: Path,
    ) -> None:
        html = tmp_path / "t.html"
        html.write_text("<html><body>x</body></html>", encoding="utf-8")

        # Use a short server-side timeout so the test is fast.
        server, port, _state = _start_server_thread_with_timeout(
            html, snapshot_timeout=0.5
        )
        try:
            _wait_for_port("127.0.0.1", port)
            # No simulated page — server will return 408 after 0.5s.
            result = runner.invoke(
                artify.main, ["snapshot", str(port), "--timeout", "2"]
            )
            assert result.exit_code == 1, result.output
            combined = (result.output + (result.stderr or "")).lower()
            assert "did not respond" in combined
        finally:
            server.shutdown()
            server.server_close()

    def test_empty_fields_is_acceptable_output(
        self,
        runner: click.testing.CliRunner,
        tmp_path: Path,
    ) -> None:
        """A page with no inputs collects an empty fields dict; the CLI
        should still print that as JSON and exit 0.
        """
        html = tmp_path / "empty.html"
        html.write_text(
            "<!doctype html><html><body>no inputs here</body></html>",
            encoding="utf-8",
        )

        server, port, _state = _start_server_thread_with_timeout(
            html, snapshot_timeout=3.0
        )
        poller_stop = threading.Event()
        try:
            _wait_for_port("127.0.0.1", port)

            def simulate_empty_page() -> None:
                while not poller_stop.is_set():
                    try:
                        conn = http.client.HTTPConnection(
                            "127.0.0.1", port, timeout=1
                        )
                        conn.request("GET", "/__commands")
                        resp = conn.getresponse()
                        cmds = json.loads(resp.read())
                        conn.close()
                    except Exception:
                        time.sleep(0.1)
                        continue
                    for cmd in cmds:
                        if cmd.get("type") == "snapshot":
                            sid = cmd["id"]
                            conn = http.client.HTTPConnection(
                                "127.0.0.1", port, timeout=2
                            )
                            conn.request(
                                "POST",
                                "/__snapshot_result/" + sid,
                                body=b'{"fields": {}}',
                                headers={"Content-Type": "application/json"},
                            )
                            r = conn.getresponse()
                            r.read()
                            conn.close()
                            return

            poller = threading.Thread(target=simulate_empty_page, daemon=True)
            poller.start()

            result = runner.invoke(
                artify.main, ["snapshot", str(port), "--timeout", "5"]
            )
            assert result.exit_code == 0, (
                f"snapshot exited {result.exit_code}: {result.output!r} {result.stderr!r}"
            )
            payload = json.loads(result.output)
            assert payload == {"fields": {}}
        finally:
            poller_stop.set()
            server.shutdown()
            server.server_close()

    def test_timeout_flag_rejects_values_below_one(
        self, runner: click.testing.CliRunner
    ) -> None:
        result = runner.invoke(artify.main, ["snapshot", "59999", "--timeout", "0.5"])
        # Click's FloatRange(min=1.0) rejects this.
        assert result.exit_code != 0

    def test_snapshot_help(self, runner: click.testing.CliRunner) -> None:
        result = runner.invoke(artify.main, ["snapshot", "--help"])
        assert result.exit_code == 0
        assert "--timeout" in result.output
        assert "Trigger a snapshot" in result.output


# ---------------------------------------------------------------------------
# Custom collector hook (window.__artify_collect__)
# ---------------------------------------------------------------------------


class TestCustomCollectorHook:
    def test_custom_hook_data_flows_through_snapshot(
        self,
        runner: click.testing.CliRunner,
        tmp_path: Path,
    ) -> None:
        """When a page defines window.__artify_collect__, the snapshot
        uses the custom function's return value instead of the default
        form collector. We can't run JS in a unit test, so we simulate
        the page by returning the hook's payload directly.
        """
        html = tmp_path / "custom.html"
        html.write_text(
            (
                "<!doctype html><html><body>\n"
                "<script>\n"
                "window.__artify_collect__ = function() {\n"
                "  return { custom: 'data' };\n"
                "};\n"
                "</script>\n"
                "<p>no inputs</p>\n"
                "</body></html>\n"
            ),
            encoding="utf-8",
        )

        server, port, _state = _start_server_thread_with_timeout(
            html, snapshot_timeout=3.0
        )
        poller_stop = threading.Event()
        try:
            _wait_for_port("127.0.0.1", port)

            custom_payload = {"custom": "data", "answer": 42}

            def simulate_page_with_hook() -> None:
                while not poller_stop.is_set():
                    try:
                        conn = http.client.HTTPConnection(
                            "127.0.0.1", port, timeout=1
                        )
                        conn.request("GET", "/__commands")
                        resp = conn.getresponse()
                        cmds = json.loads(resp.read())
                        conn.close()
                    except Exception:
                        time.sleep(0.1)
                        continue
                    for cmd in cmds:
                        if cmd.get("type") == "snapshot":
                            sid = cmd["id"]
                            # The page would call window.__artify_collect__()
                            # and POST the result. We simulate that here.
                            conn = http.client.HTTPConnection(
                                "127.0.0.1", port, timeout=2
                            )
                            conn.request(
                                "POST",
                                "/__snapshot_result/" + sid,
                                body=json.dumps({"fields": custom_payload}).encode("utf-8"),
                                headers={"Content-Type": "application/json"},
                            )
                            r = conn.getresponse()
                            r.read()
                            conn.close()
                            return

            poller = threading.Thread(target=simulate_page_with_hook, daemon=True)
            poller.start()

            result = runner.invoke(
                artify.main, ["snapshot", str(port), "--timeout", "5"]
            )
            assert result.exit_code == 0, (
                f"snapshot exited {result.exit_code}: {result.output!r} {result.stderr!r}"
            )
            payload = json.loads(result.output)
            # The custom hook's payload must be what the CLI prints.
            assert payload == {"fields": custom_payload}
        finally:
            poller_stop.set()
            server.shutdown()
            server.server_close()

    def test_reload_js_collect_uses_custom_hook_when_defined(self) -> None:
        """Static check on the injected JS: it must call
        window.__artify_collect__ when defined.
        """
        js = artify.RELOAD_JS
        assert "__artify_collect__" in js
        assert "typeof window.__artify_collect__" in js


# ---------------------------------------------------------------------------
# ReloadState backward-compat alias
# ---------------------------------------------------------------------------


class TestReloadStateAlias:
    def test_reload_state_is_instance_state(self, html_file: Path) -> None:
        assert artify.ReloadState is artify.InstanceState
        # And it can be constructed the same way.
        state = artify.ReloadState(html_file, snapshot_timeout=2.0)
        assert state.snapshot_timeout == 2.0
        # Plus the legacy mtime API still works.
        assert state.get() >= 0
