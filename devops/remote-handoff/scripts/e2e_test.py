#!/usr/bin/env python3
"""End-to-end suite for the remote-handoff skill: pack/unpack across runtimes + leak checks."""
import os, re, shutil, subprocess, sys, time

S = os.path.dirname(os.path.abspath(__file__))
WS = "/tmp/rh_ws"
ok = fail = 0


def check(label, cond, extra=""):
    global ok, fail
    ok, fail = ok + (1 if cond else 0), fail + (0 if cond else 1)
    print(("  PASS " if cond else "  FAIL ") + label + (("  " + extra) if extra else ""))
    return cond


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


MARKER = "SECRET-CANARY-" + os.urandom(4).hex().upper()
shutil.rmtree(WS, ignore_errors=True)
os.makedirs(WS + "/project/src", exist_ok=True)
open(WS + "/notes.md", "w").write("# Summary\nwe were doing the thing\nnext: finish the thing\n")
open(WS + "/project/README.md", "w").write("tiny project\n")
open(WS + "/project/src/main.py", "w").write("print('hello')\n" * 40)
open(WS + "/project/blob.bin", "wb").write(os.urandom(200_000))
open(WS + "/secrets.env", "w").write("API_KEY=%s\nDB=postgres://user:pw@host/db\n" % MARKER)

four = [
    ("py->py", ["python3", S + "/pack.py"], ["python3", S + "/unpack.py"]),
    ("py->node", ["python3", S + "/pack.py"], ["node", S + "/unpack.js"]),
    ("node->py", ["node", S + "/pack.js"], ["python3", S + "/unpack.py"]),
    ("node->node", ["node", S + "/pack.js"], ["node", S + "/unpack.js"]),
]
urls = {}
for name, packer, unpacker in four:
    print("== %s ==" % name)
    r = run(packer + ["-t", "Handoff suite " + name, "-c", "end-to-end test", "-n", WS + "/notes.md",
                      WS + "/project", WS + "/secrets.env"])
    if r.returncode:
        check(name + " pack", False, r.stderr.strip()[:200]); continue
    link = re.search(r"^link: (\S+)", r.stdout, re.M)
    pw = re.search(r"^password: (\S+)", r.stdout, re.M)
    urls[name] = (link.group(1) if link else None, pw.group(1) if pw else None)
    check(name + " message has title+link+password+enc",
          bool(link and pw and "HANDOFF —" in r.stdout and "enc: HPK2" in r.stdout))
    # far side, clean dir
    dest = "/tmp/rh_far_" + name.replace("->", "_")
    shutil.rmtree(dest, ignore_errors=True)
    u = run(unpacker + ["-k", pw.group(1), link.group(1), "--dir", dest])
    check(name + " unpack ok", u.returncode == 0, u.stderr.strip()[:160])
    if u.returncode == 0:
        same = (open(dest + "/secrets.env").read() == open(WS + "/secrets.env").read()
                and open(dest + "/project/src/main.py").read() == open(WS + "/project/src/main.py").read()
                and open(dest + "/project/blob.bin", "rb").read() == open(WS + "/project/blob.bin", "rb").read())
        check(name + " contents byte-identical (incl. binary + secret)", same)
        check(name + " _HANDOFF.md present with enc label",
              "_HANDOFF.md" in os.listdir(dest) and "HPK2" in open(dest + "/_HANDOFF.md").read())

print("== hostile checks ==")
link, pw = urls["py->py"]
raw = run(["curl", "-sL", "-A", "probe/1.0", link]).stdout
check("no plaintext canary in the uploaded blob", MARKER not in raw)
check("uploaded blob is armored ciphertext", raw.lstrip().startswith("-----BEGIN HANDOFF PACK-----"))
bad = run(["python3", S + "/unpack.py", "-k", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
           link, "--dir", "/tmp/rh_bad"])
check("wrong password rejected", bad.returncode != 0, bad.stderr.strip()[:120])

print("== legacy openssl mode ==")
r = run(["python3", S + "/pack.py", "--force-legacy", "-t", "Legacy pack", "-c", "openssl tier",
         "-n", WS + "/notes.md", WS + "/project"])
check("legacy message labels ENC loudly", "LEGACY openssl" in r.stdout and "openssl enc -d" in r.stdout)
lk = re.search(r"^link: (\S+)", r.stdout, re.M).group(1)
lp = re.search(r"^password: (\S+)", r.stdout, re.M).group(1)
shutil.rmtree("/tmp/rh_far_legacy", ignore_errors=True)
u = run(["python3", S + "/unpack.py", "-k", lp, lk, "--dir", "/tmp/rh_far_legacy"])
check("legacy pack unpacks via auto-detect", u.returncode == 0, u.stderr.strip()[:160])
if u.returncode == 0:
    check("legacy contents match", open("/tmp/rh_far_legacy/project/src/main.py").read() == open(WS + "/project/src/main.py").read()
    and open("/tmp/rh_far_legacy/_NOTES-notes.md").read() == open(WS + "/notes.md").read())

print("== crash-path plaintext scrub ==")
import tempfile
ct = tempfile.mkdtemp(prefix="remote-handoff-crashtest-")
child = subprocess.run(["python3", "-c",
    "import importlib.util,sys,os\n"
    "spec=importlib.util.spec_from_file_location('packmod', %r)\n"
    "m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
    "open(os.path.join(%r,'pack.tar.gz'),'wb').write(b'PLAINTEXT')\n"
    "m._register_scrub(%r, False)\n"
    "sys.exit('simulated crash after archiving')" % (S + "/pack.py", ct, ct)],
    capture_output=True, text=True)
check("plaintext archive scrubbed even when the sender crashes",
      child.returncode != 0 and not os.path.exists(os.path.join(ct, "pack.tar.gz")))

print("== no-plaintext-left-behind ==")
litter = []
for d in os.listdir("/tmp"):
    if d.startswith("remote-handoff"):
        for root, _, fs_ in os.walk("/tmp/" + d):
            litter += [os.path.join(root, f) for f in fs_ if f.endswith(".tar.gz")]
check("no plaintext .tar.gz left in any temp dir", not litter, str(litter[:3]))

print("\n%d passed, %d failed" % (ok, fail))
sys.exit(1 if fail else 0)
