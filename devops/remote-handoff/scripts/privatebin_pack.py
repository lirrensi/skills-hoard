#!/usr/bin/env python3
"""PrivateBin v2 pack: create (prints LINK#KEY) and read (decrypt) in pure CLI, no browser.
Usage: privatebin_pack.py send <file>   |   privatebin_pack.py get <full_url#key>
Verified against privatebin.net (1 post / 60 s).
"""
import base64, hashlib, json, os, subprocess, sys, urllib.parse, zlib

UA = "handoff-pack/1.0 (+curl)"
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def b58(b: bytes) -> str:
    n = int.from_bytes(b, "big"); out = ""
    while n:
        n, r = divmod(n, 58); out = B58[r] + out
    return out

def un_b58(s: str) -> bytes:
    n = 0
    for c in s:
        n = n * 58 + B58.index(c)
    pad = len(s) - len(s.lstrip("1"))
    return b"\x00" * pad + n.to_bytes((n.bit_length() + 7) // 8, "big")

def curl(*a: str) -> str:
    return subprocess.run(["curl", "-s", "-L", "-A", UA, *a],
                          capture_output=True).stdout.decode(errors="replace")

def send(instance: str, text: str, expire: str = "1hour"):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    salt, key, iv = os.urandom(8), os.urandom(32), os.urandom(16)
    derived = hashlib.pbkdf2_hmac("sha256", key, salt, 100000, 32)
    co = zlib.compressobj(9, zlib.DEFLATED, -15)
    blob = co.compress(json.dumps({"paste": text}).encode()) + co.flush()
    adata = [[base64.b64encode(iv).decode(), base64.b64encode(salt).decode(),
              100000, 256, 128, "aes", "gcm", "zlib"], "plaintext", 0, 0]
    aad = json.dumps(adata, separators=(",", ":")).encode()
    ct = AESGCM(derived).encrypt(iv, blob, aad)
    body = json.dumps({"v": 2, "adata": adata, "ct": base64.b64encode(ct).decode(),
                       "meta": {"expire": expire}})
    r = json.loads(curl("-H", "Content-Type: application/json",
                        "-H", "X-Requested-With: JSONHttpRequest",
                        "-X", "POST", "--data-binary", body, instance))
    if r.get("status") != 0:
        raise SystemExit("create failed: %s" % r)
    return "%s?%s#%s" % (instance, r["id"], b58(key)), r["deletetoken"]

def get(url: str) -> str:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    u = urllib.parse.urlsplit(url)
    pid, key_b58 = u.query.lstrip("?"), u.fragment
    d = json.loads(curl("-H", "Accept: application/json",
                        "-H", "X-Requested-With: JSONHttpRequest",
                        "%s://%s?%s" % (u.scheme, u.netloc, pid)))
    a = json.loads(d["adata"]) if isinstance(d["adata"], str) else d["adata"]
    k = hashlib.pbkdf2_hmac("sha256", un_b58(key_b58),
                            base64.b64decode(a[0][1] + "=" * (-len(a[0][1]) % 4)), a[0][2], 32)
    pt = AESGCM(k).decrypt(base64.b64decode(a[0][0]), base64.b64decode(d["ct"]),
                           json.dumps(a, separators=(",", ":")).encode())
    return json.loads(zlib.decompressobj(-15).decompress(pt).decode())["paste"]

if __name__ == "__main__":
    if sys.argv[1] == "send":
        link, dtok = send("https://privatebin.net/", open(sys.argv[2]).read())
        print("LINK:%s" % link)
        print("DELETE_TOKEN:%s" % dtok)
    else:
        print(get(sys.argv[2]))
