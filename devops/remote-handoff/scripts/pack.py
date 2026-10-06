#!/usr/bin/env python3
"""pack.py — remote-handoff SENDER: collect -> archive -> ENCRYPT (mandatory) -> upload -> print message.

Usage:
  pack.py -t "TITLE" [-c "one-line context"] [-n notes.md] [--no-upload] [--keep-plain] PATH [PATH...]

Rules enforced here:
  * The plaintext archive is deleted before upload. Nothing unencrypted is ever uploaded.
  * Uses the system temp dir (TMPDIR / TMP / TEMP, else /tmp) — never the working tree.
  * ENC is HPK2 (aes-256-gcm+zlib) via handoff.py. If `cryptography` is missing it degrades to
    LEGACY openssl (aes-256-cbc+pbkdf2) and labels it loudly so the far side knows the difference.
  * Prints the outer message (title + context + link + password + enc type + unpack command).
"""
import argparse, atexit, base64, datetime, os, shutil, subprocess, sys, tarfile, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import handoff    # core HPK2 container (aes-256-gcm + zlib, importable)
import backend    # tier chain: python+cryptography -> node -> openssl(legacy)

HOSTS = ["https://x0.at", "https://temp.sh/upload", "https://envs.sh"]
# never ship junk: bytecode, VCS metadata, dependency trees
EXCLUDE_DIRS = {"__pycache__", ".git", ".svn", "node_modules", ".venv", "venv", ".tox", ".mypy_cache"}
EXCLUDE_SUFFIX = (".pyc", ".pyo", ".DS_Store", ".swp")
UA = "remote-handoff/1.0 (+curl)"


def which(b):
    return shutil.which(b)


def tar_filter(ti):
    """tarfile filter: drop excluded dirs/suffixes from the archive."""
    parts = ti.name.split("/")
    if any(p in EXCLUDE_DIRS for p in parts) or ti.name.endswith(EXCLUDE_SUFFIX):
        return None
    return ti


def scrub_plaintext(tmp, keep):
    """Remove the unencrypted archive from temp on ANY exit path — including a crash.
    pack.asc (ciphertext) is deliberately left in place: it is the artifact the message points at."""
    if keep:
        return
    for f in ("pack.tar.gz", "pack.tar"):
        p = os.path.join(tmp, f)
        if os.path.exists(p):
            os.unlink(p)


def _register_scrub(tmp, keep):
    atexit.register(scrub_plaintext, tmp, keep)


def make_archive(paths, notes, title, context, out_dir, enc_label):
    """Build pack.tar.gz in out_dir; return (tarpath, manifest list)."""
    manifest = []
    for p in paths:
        if not os.path.exists(p):
            sys.exit("pack: path not found: %s" % p)
    tarpath = os.path.join(out_dir, "pack.tar.gz")
    readme = os.path.join(out_dir, "_HANDOFF.md")
    with open(readme, "w") as f:
        f.write("# HANDOFF — %s\n\nwhere: %s\ncreated: %s\nenc: %s\n\n"
                "This archive was shipped encrypted; if you are reading it, decryption already worked.\n"
                % (title, context or "(no context given)",
                   datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), enc_label))
    with tarfile.open(tarpath, "w:gz") as t:
        t.add(readme, arcname="_HANDOFF.md")
        for n in notes:
            t.add(n, arcname="_NOTES-" + os.path.basename(n))
        for p in paths:
            t.add(p, arcname=os.path.basename(os.path.normpath(p)), filter=tar_filter)
    with tarfile.open(tarpath) as t:
        for m in t.getmembers():
            if m.isfile():
                manifest.append((m.name, m.size))
    return tarpath, manifest


def encrypt_file(tarpath, out_dir, tier):
    """Encrypt to pack.asc with the resolved tier. Returns (ascpath, key_b64).

    Reported tier order: python+cryptography -> node -> openssl. python/node keep the HPK2 format, so the
    far side never notices the swap. openssl is LEGACY and changes the format — it gets announced.
    If no tier exists this exits: plaintext is never uploaded, no exceptions.
    """
    blob = open(tarpath, "rb").read()
    asc = os.path.join(out_dir, "pack.asc")
    if tier == "openssl":
        key_b64 = base64.b64encode(os.urandom(24)).decode()
        open(asc, "wb").write(backend.enc(blob, key_b64, tier))
        return asc, key_b64
    key_b64 = base64.b64encode(os.urandom(32)).decode()
    open(asc, "wb").write(backend.enc(blob, key_b64, tier))   # backend always returns bytes
    return asc, key_b64


def upload(asc, host=None):
    order = [host] if host else HOSTS
    for h in order:
        if not h:
            continue
        r = subprocess.run(["curl", "-s", "-A", UA, "-F", "file=@" + asc, h], capture_output=True)
        out = r.stdout.decode(errors="replace").strip()
        if out.startswith("http"):
            return out, h
        else:
            sys.stderr.write("pack: host %s refused: %s\n" % (h, out[:120]))
    return None, None


def main():
    ap = argparse.ArgumentParser(prog="pack.py")
    ap.add_argument("-t", "--title", required=True, help="session title the far side sees first")
    ap.add_argument("-c", "--context", default="", help="one line: what we were doing")
    ap.add_argument("-n", "--notes", action="append", default=[], help="extra summary file(s) to include")
    ap.add_argument("--no-upload", action="store_true")
    ap.add_argument("--keep-plain", action="store_true", help="keep the unencrypted tar (default: delete)")
    ap.add_argument("--host", default=None, help="force one upload host")
    ap.add_argument("--tier", choices=["python", "node", "openssl"], default=None,
                    help="force a crypto tier (default: auto = python -> node -> openssl)")
    ap.add_argument("--force-legacy", action="store_true",
                    help="alias for --tier openssl (LEGACY format, announced in the message)")
    ap.add_argument("paths", nargs="*", help="files/dirs to include")
    a = ap.parse_args()

    tmp = tempfile.mkdtemp(prefix="remote-handoff-")
    _register_scrub(tmp, a.keep_plain)   # protects crash paths too, not just the happy one
    sys.stderr.write("pack: temp = %s\n" % tmp)
    tier = backend.resolve("openssl" if a.force_legacy else a.tier)   # BEFORE archiving: README states it
    enc_label = backend.label(tier)
    sys.stderr.write("pack: tier = %s   |  survey: %s\n" % (tier, backend.survey()))
    tarpath, manifest = make_archive(a.paths, a.notes, a.title, a.context, tmp, enc_label)
    asc, key_b64 = encrypt_file(tarpath, tmp, tier)
    if not a.keep_plain:
        os.remove(tarpath)          # plaintext never lingers, never uploads
    total = sum(s for _, s in manifest)
    sys.stderr.write("pack: manifest (%d files, %.1f KB)\n" % (len(manifest), total / 1024))
    for n, s in manifest:
        sys.stderr.write("   %9d  %s\n" % (s, n))

    url, host = (None, None) if a.no_upload else upload(asc, a.host)
    asc_tmp = asc
    # both runtimes auto-detect the format, so these two lines are valid even for a legacy pack
    runner_py = "python3 unpack.py -k '%s' pack.asc" % key_b64
    runner_js = "node unpack.js -k '%s' pack.asc" % key_b64
    runner_raw = ("openssl enc -d -aes-256-cbc -pbkdf2 -in pack.asc -out pack.tar.gz && tar xzf pack.tar.gz"
                  if tier == "openssl" else None)
    print("======= HANDOFF MESSAGE (copy/paste to the other side) =======")
    print("HANDOFF — %s" % a.title)
    print("doing: %s" % (a.context or "(no context given)"))
    print("link: %s" % (url or "<not uploaded — upload %s yourself>" % asc_tmp))
    print("password: %s" % key_b64)
    print("enc: %s" % enc_label)
    print("size: %d files, %.1f KB (encrypted, %.1f KB)%s"
          % (len(manifest), total / 1024, os.path.getsize(asc) / 1024,
             "" if url else "  [NOT YET UPLOADED]"))
    print("unpack (any runtime):")
    print("   curl -sL <link> -o pack.asc && %s" % runner_py)
    print("   curl -sL <link> -o pack.asc && %s" % runner_js)
    if runner_raw:
        print("   (no runtime at all) curl -sL <link> -o pack.asc && %s" % runner_raw)
    print("============= END =============")
    print("\nartifacts: %s" % asc_tmp, file=sys.stderr)


if __name__ == "__main__":
    main()
