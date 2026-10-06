#!/usr/bin/env python3
"""backend.py — crypto tier resolution for remote-handoff.

Chain: python3+cryptography  ->  node (zero installs)  ->  openssl (LEGACY, different format).
python and node both produce/consume HPK2 (aes-256-gcm + zlib) — identical bytes either way, so swapping
tiers never changes the message. Only openssl changes the FORMAT (aes-256-cbc + pbkdf2), so only that tier
must be announced to the far side.

Never returns silently: if no backend exists it exits with a message and the caller must refuse to upload.
"""
import base64, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OPENSSL_MIN = (1, 1, 1)          # -pbkdf2 exists only from 1.1.1; 3.0.13 (typical) is fine

HPK2_LABEL = "HPK2 (aes-256-gcm + zlib, base64 armor, tier={tier})"
LEGACY_LABEL = ("LEGACY openssl (aes-256-cbc + pbkdf2)  "
                "[NOT HPK2 — far side must run: openssl enc -d -aes-256-cbc -pbkdf2]")


def have_python_crypto():
    try:
        import cryptography  # noqa: F401
        return True
    except ImportError:
        return False


def node_ver():
    n = shutil.which("node")
    if not n:
        return None
    try:
        return subprocess.run([n, "-v"], capture_output=True, text=True).stdout.strip()
    except Exception:
        return None


def openssl_ver():
    o = shutil.which("openssl")
    if not o:
        return None
    try:
        return subprocess.run([o, "version"], capture_output=True, text=True).stdout.strip()
    except Exception:
        return None


def openssl_pbkdf2_ok():
    v = openssl_ver()
    if not v:
        return False
    m = re.search(r"(\d+)\.(\d+)\.(\d+)", v)
    return bool(m) and tuple(int(x) for x in m.groups()) >= OPENSSL_MIN


def survey():
    """What this box actually has — for reporting, then decision."""
    return {"python_cryptography": have_python_crypto(), "node": node_ver(),
            "openssl": openssl_ver(), "tar": (subprocess.run(["tar", "--version"],
                     capture_output=True, text=True).stdout.splitlines() or [""])[0].strip()}


def resolve(prefer=None):
    """Return ('python'|'node'|'openssl'). prefer forces one (error if unavailable)."""
    avail = {"python": have_python_crypto(), "node": bool(node_ver()),
             "openssl": openssl_pbkdf2_ok()}
    if prefer:
        if not avail.get(prefer):
            sys.exit("backend: forced tier %r unavailable (%s)" % (prefer, survey()))
        return prefer
    for t in ("python", "node", "openssl"):
        if avail[t]:
            return t
    sys.exit("backend: no crypto backend — need python cryptography, node, or openssl>=1.1.1 "
             "(survey: %s)" % survey())


def label(tier):
    return HPK2_LABEL.format(tier=tier) if tier in ("python", "node") else LEGACY_LABEL


# ---------------------------------------------------------------- encrypt / decrypt
def enc(plain: bytes, key_b64: str, tier: str):
    """Return the payload to upload: armored text for HPK2, raw binary for openssl."""
    if tier == "python":
        import handoff
        return handoff.armor(handoff.enc(plain, base64.b64decode(key_b64))).encode()  # bytes, like node
    if tier == "node":
        r = subprocess.run([shutil.which("node"), os.path.join(HERE, "handoff.js"),
                            "enc", "-k", key_b64], input=plain, capture_output=True)
        if r.returncode:
            sys.exit("backend: node encrypt failed: " + r.stderr.decode()[:200])
        return r.stdout
    fd, tarp = tempfile.mkstemp(suffix=".bin"); os.close(fd)
    fd, asc = tempfile.mkstemp(suffix=".enc"); os.close(fd)
    try:
        open(tarp, "wb").write(plain)
        r = subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-salt",
                            "-pass", "pass:" + key_b64, "-in", tarp, "-out", asc], capture_output=True)
        if r.returncode:
            sys.exit("backend: openssl encrypt failed: " + r.stderr.decode()[:200])
        return open(asc, "rb").read()
    finally:
        os.unlink(tarp); os.unlink(asc)


def dec(raw: bytes, key_b64: str, tier: str) -> bytes:
    if tier == "python":
        import handoff
        blob = handoff.dearmor(raw.decode()) if raw.lstrip().startswith(b"-") else raw
        return handoff.dec(blob, base64.b64decode(key_b64))
    if tier == "node":
        r = subprocess.run([shutil.which("node"), os.path.join(HERE, "handoff.js"),
                            "dec", "-k", key_b64], input=raw, capture_output=True)
        if r.returncode:
            raise RuntimeError(r.stderr.decode()[:160] or "node decrypt failed")
        return r.stdout
    fd, asc = tempfile.mkstemp(suffix=".enc"); os.close(fd)
    fd, tarp = tempfile.mkstemp(suffix=".tar.gz"); os.close(fd)
    try:
        open(asc, "wb").write(raw)
        r = subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
                            "-pass", "pass:" + key_b64, "-in", asc, "-out", tarp], capture_output=True)
        if r.returncode:
            raise RuntimeError((r.stderr.decode() or "openssl decrypt failed")[:160])
        return open(tarp, "rb").read()
    finally:
        os.unlink(asc); os.unlink(tarp)


def order():
    """Receiver attempt order: both HPK2 impls first (format-identical), openssl last (format change)."""
    seq = []
    for t in ("python", "node"):
        avail = have_python_crypto() if t == "python" else bool(node_ver())
        if avail:
            seq.append(t)
    if openssl_pbkdf2_ok():
        seq.append("openssl")
    return seq


if __name__ == "__main__":
    s = survey()
    for k, v in s.items():
        print("%-20s %s" % (k, v))
    print("resolved tier:      %s" % resolve())
    print("receiver order:     %s" % order())
    print("label:              %s" % label(resolve()))
