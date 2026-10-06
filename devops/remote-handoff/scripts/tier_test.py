#!/usr/bin/env python3
"""tier_test.py — remote-handoff tier matrix: sender tier {python,node,openssl} x receiver {python,node}.
Real uploads, real fetches. Verifies that python/node are byte-compatible (same HPK2 format) and that
openssl is a distinct, announced format that python- and node-side receivers still open via the chain."""
import os, re, shutil, subprocess, sys

S = os.path.dirname(os.path.abspath(__file__))
WS, CANARY = "/tmp/rh_tier_ws", "TIER-CANARY-" + os.urandom(3).hex().upper()
ok = fail = 0


def check(label, cond, extra=""):
    global ok, fail
    ok, fail = ok + (1 if cond else 0), fail + (0 if cond else 1)
    print(("  PASS " if cond else "  FAIL ") + label + (("  " + extra) if extra else ""))


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


print("== box survey ==")
print(run(["python3", S + "/backend.py"]).stdout.strip())

shutil.rmtree(WS, ignore_errors=True)
os.makedirs(WS + "/project/src")
open(WS + "/project/src/a.py", "w").write("a = 1\n" * 50)
open(WS + "/project/data.bin", "wb").write(os.urandom(120_000))
open(WS + "/notes.md", "w").write("# notes\nstate: tier matrix\n")
open(WS + "/key.env", "w").write("TOKEN=%s\n" % CANARY)

for tier in ["python", "node", "openssl"]:
    print("== sender tier: %s ==" % tier)
    r = run(["python3", S + "/pack.py", "--tier", tier, "-t", "Tier test %s" % tier,
             "-c", "tier matrix", "-n", WS + "/notes.md", WS + "/project", WS + "/key.env"])
    if r.returncode:
        check("pack --tier %s" % tier, False, r.stderr.strip()[:200]); continue
    link = re.search(r"^link: (\S+)", r.stdout, re.M).group(1)
    pw = re.search(r"^password: (\S+)", r.stdout, re.M).group(1)
    announced = re.search(r"^enc: (.+)$", r.stdout, re.M).group(1)
    if tier == "openssl":
        check("openssl pack announces LEGACY + openssl unpack cmd",
              "LEGACY" in announced and "openssl enc -d" in r.stdout)
    else:
        check("HPK2 pack announces tier %s" % tier, "HPK2" in announced and "tier=" + tier in announced)
    # ciphertext-only on the wire
    raw = subprocess.run(["curl", "-sL", "-A", "tier-probe/1.0", link],
                         capture_output=True).stdout.decode("utf-8", "replace")
    check("no canary in uploaded blob", CANARY not in raw)
    for rtier, cmd in [("python", ["python3", S + "/unpack.py"]), ("node", ["node", S + "/unpack.js"])]:
        dest = "/tmp/rh_tier_%s_%s" % (tier, rtier)
        shutil.rmtree(dest, ignore_errors=True)
        u = run(cmd + ["-k", pw, link, "--dir", dest])
        good = u.returncode == 0 and open(dest + "/key.env").read() == open(WS + "/key.env").read() \
            and open(dest + "/project/data.bin", "rb").read() == open(WS + "/project/data.bin", "rb").read()
        check("  %s -> %s open + byte-identical" % (tier, rtier), good, u.stderr.strip()[:120])

print("== receiver chain: HPK2 pack opened by node-only receiver ==")
shutil.rmtree("/tmp/rh_chain", ignore_errors=True)
r = run(["python3", S + "/pack.py", "--tier", "node", "-t", "chain",
         "-n", WS + "/notes.md", WS + "/key.env"])
link = re.search(r"^link: (\S+)", r.stdout, re.M).group(1)
pw = re.search(r"^password: (\S+)", r.stdout, re.M).group(1)
u = run(["node", S + "/unpack.js", "-k", pw, link, "--dir", "/tmp/rh_chain"])
check("node receiver alone opens node-tier pack", u.returncode == 0, u.stderr.strip()[:120])

print("== wrong tier forced must fail cleanly ==")
bad = run(["python3", S + "/unpack.py", "--enc", "openssl", "-k", pw, link, "--dir", "/tmp/rh_wrongtier"])
check("forcing openssl on an HPK2 pack fails with a clear error",
      bad.returncode != 0 and "garbage" in bad.stderr or "bad" in bad.stderr.lower())

print("\n%d passed, %d failed" % (ok, fail))
sys.exit(1 if fail else 0)
