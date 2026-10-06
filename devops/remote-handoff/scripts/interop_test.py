#!/usr/bin/env python3
"""Interop test for handoff v2: handoff.py (python tier) <-> handoff.js (node tier).
Run: python3 interop_test.py   (needs `node` on PATH). Two impls, one format, both directions."""
import base64, os, subprocess, sys, time

SK = os.path.dirname(os.path.abspath(__file__))
PY, JS = [sys.executable, SK + "/handoff.py"], ["node", SK + "/handoff.js"]
BEGIN = "-----BEGIN HANDOFF PACK-----"

ok = fail = 0


def check(label, cond):
    global ok, fail
    ok, fail = ok + (1 if cond else 0), fail + (0 if cond else 1)
    print(("  PASS " if cond else "  FAIL ") + label)


def run(cmd, data=b"", want_err=False):
    p = subprocess.run(cmd, input=data, capture_output=True)
    if not want_err and p.returncode != 0:
        print("   !! FAILED", cmd[1:3], p.stderr.decode()[:160])
    return p


def container(armored):
    return base64.b64decode("".join(armored.decode().split(BEGIN)[1].split("-----END HANDOFF PACK-----")[0].split()))


def tamper(armored):
    blob = bytearray(container(armored))
    blob[40] ^= 0x01
    b = base64.b64encode(bytes(blob)).decode()
    return (BEGIN + "\n" + "\n".join(b[i:i + 64] for i in range(0, len(b), 64))
            + "\n-----END HANDOFF PACK-----\n").encode()


for name, payload in [("ascii", b"handoff pack\nline two\n"),
                      ("unicode", "cats \U0001f63c \u043a\u043e\u0448\u043a\u0438 \u732b\n".encode()),
                      ("empty", b""), ("1MiB random", os.urandom(1 << 20)),
                      ("4KB text", (b"the quick brown fox jumps over the lazy dog. " * 100))]:
    print("== %s (%d B) ==" % (name, len(payload)))
    k = base64.b64encode(os.urandom(32)).decode()
    pe, ne = run(PY + ["enc", "-k", k], payload), run(JS + ["enc", "-k", k], payload)
    check("py enc -> node dec", run(JS + ["dec", "-k", k], pe.stdout).stdout == payload)
    check("node enc -> py dec", run(PY + ["dec", "-k", k], ne.stdout).stdout == payload)
    check("header parity (5 bytes)", container(pe.stdout)[:5] == container(ne.stdout)[:5])
    check("armored, not raw", pe.stdout.decode().startswith(BEGIN))
    gen = run(PY + ["enc"], payload)
    gk = [l for l in gen.stderr.decode().splitlines() if l.startswith("KEY:")][0][4:]
    check("self-generated KEY:<b64> path", run(JS + ["dec", "-k", gk], gen.stdout).stdout == payload)
    e1 = run(JS + ["dec", "-k", k], tamper(pe.stdout), want_err=True)
    check("tampered rejected (node)", e1.returncode != 0)
    check("wrong key rejected (py)",
          run(PY + ["dec", "-k", base64.b64encode(os.urandom(32)).decode()], pe.stdout, want_err=True).returncode != 0)
    check("garbage input rejected", run(PY + ["dec", "-k", k], b"hello not a pack", want_err=True).returncode != 0)

big = os.urandom(5 << 20)
t0 = time.time(); k = base64.b64encode(os.urandom(32)).decode()
r = run(JS + ["enc", "-k", k], big); te = time.time() - t0
t1 = time.time(); back = run(PY + ["dec", "-k", k], r.stdout).stdout; td = time.time() - t1
check("5 MiB random: node enc -> py dec identical", back == big)
print("\n%d passed, %d failed" % (ok, fail))
print("5MiB random: node enc %.2fs, py dec %.2fs, armor %d chars (%.2fx)"
      % (te, td, len(r.stdout), len(r.stdout) / len(big)))
print("line counts: handoff.py=%d handoff.js=%d"
      % (len(open(SK + "/handoff.py").read().splitlines()), len(open(SK + "/handoff.js").read().splitlines())))
sys.exit(1 if fail else 0)
