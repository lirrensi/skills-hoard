#!/usr/bin/env python3
"""handoff.py — remote-handoff core (python tier). Importable: from handoff import enc, dec, armor.
Container v2: "HPK2" (4) | flags (1, bit0=zlib) | nonce (12) | AES-256-GCM ct | tag (16, trailing)
Key: 32 raw bytes, base64 for transport. No KDF, no passphrase mode, no salt — nothing to disagree about.
CLI:  handoff.py enc [-k KEY_B64] [-o OUT] [IN]   (no -k -> prints KEY:<b64> on stderr)
      handoff.py dec -k KEY_B64 [IN]
"""
import base64, os, sys, zlib

MAGIC, HDR = b"HPK2", 17
BEGIN, END = "-----BEGIN HANDOFF PACK-----", "-----END HANDOFF PACK-----"


def enc(pt: bytes, key: bytes) -> bytes:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    n = os.urandom(12)
    return MAGIC + b"\x01" + n + AESGCM(key).encrypt(n, zlib.compress(pt, 9), None)


def dec(blob: bytes, key: bytes) -> bytes:
    if len(blob) < HDR + 16 or blob[:4] != MAGIC:
        raise ValueError("not a handoff pack (bad magic or truncated)")
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    pt = AESGCM(key).decrypt(blob[5:17], blob[17:], None)  # raises on any tamper/wrong key
    return zlib.decompress(pt) if blob[4] & 1 else pt


def armor(blob: bytes) -> str:
    b = base64.b64encode(blob).decode()
    return BEGIN + "\n" + "\n".join(b[i:i + 64] for i in range(0, len(b), 64)) + "\n" + END + "\n"


def dearmor(text: str) -> bytes:
    if BEGIN in text and END in text:
        return base64.b64decode("".join(text.split(BEGIN)[1].split(END)[0].split()))
    return base64.b64decode("".join(text.split()))


def main(a):
    if len(a) < 2 or a[1] not in ("enc", "dec"):
        sys.exit("usage: handoff.py enc|dec [-k KEY_B64] [-o OUT] [IN]")
    fl, files, i = {}, [], 2
    while i < len(a):
        if a[i] in ("-k", "-o") and i + 1 < len(a):
            fl[a[i]] = a[i + 1]; i += 2
        else:
            files.append(a[i]); i += 1
    src = open(files[0], "rb").read() if files else sys.stdin.buffer.read()
    if a[1] == "enc":
        key = base64.b64decode(fl["-k"]) if "-k" in fl else os.urandom(32)
        if "-k" not in fl:
            sys.stderr.write("KEY:%s\n" % base64.b64encode(key).decode())
        out = armor(enc(src, key))
        open(fl["-o"], "w").write(out) if "-o" in fl else sys.stdout.write(out)
    else:
        if "-k" not in fl:
            sys.exit("handoff: dec needs -k KEY_B64")
        raw = src
        try:
            sys.stdout.buffer.write(dec(dearmor(raw.decode()) if raw.lstrip().startswith(b"-") else raw,
                                        base64.b64decode(fl["-k"])))
        except Exception as e:
            sys.exit("handoff: %s" % e)


if __name__ == "__main__":
    main(sys.argv)
