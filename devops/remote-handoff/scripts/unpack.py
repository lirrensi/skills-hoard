#!/usr/bin/env python3
"""unpack.py — remote-handoff RECEIVER (python tier).
Usage: unpack.py -k KEY_B64 <url|pack.asc|-> [--dir DEST] [--enc hpk2|openssl]
Fetches (if given http/https), decrypts, extracts, prints a manifest. Refuses unsafe tar members.
"""
import argparse, atexit, base64, datetime, os, shutil, subprocess, sys, tarfile, tempfile, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import handoff
import backend

UA = "remote-handoff/1.0 (+curl)"


def fetch(src):
    if src.startswith(("http://", "https://")):
        req = urllib.request.Request(src, headers={"User-Agent": UA})
        return urllib.request.urlopen(req, timeout=60).read()
    if src == "-":
        return sys.stdin.buffer.read()
    return open(src, "rb").read()


def safe_extract(tar, dest):
    """Extract only regular files/dirs whose paths stay inside dest."""
    root = os.path.realpath(dest)
    bad = []
    for m in tar.getmembers():
        if m.name.startswith(("/", "\\")) or ".." in m.name.split("/"):
            bad.append(m.name); continue
        target = os.path.realpath(os.path.join(root, m.name))
        if not (target == root or target.startswith(root + os.sep)):
            bad.append(m.name); continue
        if m.issym() or m.islnk():
            bad.append(m.name + " (link)"); continue
    if bad:
        sys.exit("unpack: refusing unsafe archive members: %s" % ", ".join(bad[:5]))
    tar.extractall(dest)


def main():
    ap = argparse.ArgumentParser(prog="unpack.py")
    ap.add_argument("-k", "--key", required=True, help="base64 key (PART 2 of the handoff message)")
    ap.add_argument("src", help="url, local file, or - for stdin")
    ap.add_argument("--dir", default=None, help="destination dir (default: ./handoff-<UTC stamp>)")
    ap.add_argument("--enc", default="auto", choices=["auto", "python", "node", "openssl", "hpk2"],
                    help="force a crypto tier (default auto: python -> node -> openssl)")
    a = ap.parse_args()
    raw = fetch(a.src)
    dest = a.dir or ("handoff-" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%S"))
    os.makedirs(dest, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="remote-handoff-in-")
    atexit.register(shutil.rmtree, tmp, ignore_errors=True)   # cleans up even on sys.exit()
    tar_path = os.path.join(tmp, "pack.tar.gz")

    forced = {"hpk2": "python"}.get(a.enc, a.enc)
    tries = backend.order() if forced == "auto" else [forced]
    errs, used = [], None
    for tier in tries:
        try:
            open(tar_path, "wb").write(backend.dec(raw, a.key, tier))
            used = tier
            break
        except Exception as e:
            errs.append("%s: %s" % (tier, e))
    if used is None:
        sys.exit("unpack: decrypt failed — wrong password, tampered pack, or unknown format (%s)"
                 % " | ".join(errs))
    print("decrypted with tier: %s" % used)

    with tarfile.open(tar_path) as t:
        names = [(m.name, m.size) for m in t.getmembers() if m.isfile()]
        safe_extract(t, dest)
    shutil.rmtree(tmp, ignore_errors=True)   # no leftover plaintext archive in temp
    print("unpacked %d files into %s/" % (len(names), dest))
    for n, s in names:
        print("   %9d  %s" % (s, n))
    head = os.path.join(dest, "_HANDOFF.md")
    if os.path.exists(head):
        print("\n--- _HANDOFF.md ---")
        print(open(head).read().strip())


if __name__ == "__main__":
    main()
