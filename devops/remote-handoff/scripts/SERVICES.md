# SERVICES — where the encrypted pack can go

**Rule that never changes:** these hosts are dumb storage. They are never trusted, they only ever receive
ciphertext. If a host is hostile, coerced, or sells its logs, it still learns nothing (§ Step 2 of SKILL.md).
Every entry below was probed from this box; re-probe before relying on it (hosts churn fast).

## Upload hosts — file transport (last verified 2026-10-06)

| host | command | status | notes |
| --- | --- | --- | --- |
| `x0.at` | `curl -s -F file=@pack.asc https://x0.at` | ✅ live | returns `https://x0.at/XXXX.asc`; **max 1024 MiB**; retention **3–100 days**, size-dependent (`MIN+(MAX-MIN)*(1-size/max)^2`); **no delete token is returned — uploads are not removable** |
| `temp.sh` | `curl -s -F file=@pack.asc https://temp.sh/upload` | ✅ live | returns `https://temp.sh/<id>/<name>` |
| `envs.sh` | `curl -s -F file=@pack.asc https://envs.sh` | ✅ live | answers **302** — must follow redirect (`curl -L`) |
| `0x0.st` | — | ❌ dead | "uploads disabled … AI botnet spam for the past few months … no ETA" |
| `transfer.sh` | — | ❌ no response | connection hangs |
| `bashupload.com` | — | ❌ no response | connection fails |
| `catbox litterbox` | — | ❌ no response | blocked/unreachable from this box |
| `pixeldrain` | — | ❌ gated | `authentication_required` — needs an API key |
| GitHub Gist | — | ❌ not viable | anonymous gist API is gone; `gh` CLI not installed |

Order the senders use: `x0.at` → `temp.sh` → `envs.sh`. `pack.py --host URL` forces one.

## Paste services — they add their own client-side encryption (key in URL fragment)

Useful when you want **expiry**, **burn-after-reading**, or a one-time read rather than a raw file.

| service | status | notes |
| --- | --- | --- |
| `privatebin.net` | ✅ verified headless | 2.0.6, A+ Observatory, CH. Expiry max **3 days**; **60 s between posts**; script `scripts/privatebin_pack.py` |
| other PrivateBin instances | ✅ listed | `privatebin.info/directory/` — e.g. `secret.timeweb.ru` (RU), `paste.ononoki.org`, `0in.ch`, `anonpaste.org`, all 2.0.6 / A+ |
| `onetimesecret.com` | ⚠️ unverified | API needs an account (guest endpoints exist but were not tested from this box) |
| Bitwarden Send | ⚠️ unverified | best UX (100 MB, max-access-count, password) but needs an account + `bw` CLI |

PrivateBin's own docs: it stores nothing readable ("the server has zero knowledge of stored data"), but a
**browser** user "has to trust the server administrator not to inject any malicious code". Our CLI path never
executes server code, so the key stays local. Access logs (who fetched when) are NOT protected — only content.

## Adding / re-checking a host

```
head -c 200 /dev/urandom | base64 > /tmp/t.txt
python3 scripts/handoff.py enc -o /tmp/t.asc /tmp/t.txt        # NEVER probe with plaintext
curl -s -A 'remote-handoff/1.0' -F file=@/tmp/t.asc <HOST>    # expect a URL back
curl -sL <URL> | python3 scripts/handoff.py dec -k "<key>"    # must round-trip, then update this file
```
Never upload a probe that contains anything real. And keep this table's dates current — a host that worked
last month is a guess until re-probed.
