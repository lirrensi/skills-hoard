---
name: remote-handoff
description: Send an encrypted handoff pack to another chat or agent.
---

# remote-handoff

**Trigger:** "remote handoff" (or any request to move work to another chat / harness / machine / agent).
⚠️ **Word collision:** plain `handoff` is owned by the hermes-handoff plugin (an in-chat capsule for the next
session of _this_ conversation). Use "remote handoff" for this skill. If he says just "handoff" and context
suggests moving work outside this chat, ask in one line which he means.

Pipeline: **assemble → archive → ENCRYPT (mandatory) → upload ciphertext → return the message block.**

---

## Step 1 — assemble what goes in the pack (agent work, not scripted)

Default: a good, extensive summary. On request: an **whole chat export** (if harness allows) plus everything needed to continue.

What a pack must answer for a stranger with ZERO chat history:

- what we were doing and why (goal, current state)
- decisions taken + the reason, and what was rejected
- open questions / blockers / what's unknown
- exact next actions, commands, file paths, versions
- gotchas and already-failed attempts (so they don't repeat them)
- file inventory

Avoid large binaries and files unless really requited, priority: text files, code snippets, whole documents allowed, prefer to keep under 50mb.s

**Secrets are ALLOWED inside the pack** — API keys, tokens, connection strings, credentials, private URLs.
That is deliberate: the far side must be able to _continue_, not come back asking for a key it can't get.
Encryption is mandatory (Step 2), so secrets ride safely. This is the reason encryption is non-negotiable,
not an excuse to skip it.

## Step 2 — archive + encrypt + upload (scripts)

```
python3 scripts/pack.py -t "TITLE" -c "one-line context" -n summary.md PATH [PATH...]
```

**Hard rules — do not break:**

1. **ENCRYPT ALWAYS.** Never upload an unencrypted file, never "just this once". The service is never trusted:
   the host only ever sees ciphertext, so a hostile/compromised/coerced host learns nothing.
2. **Secrets inside the pack are fine — only because of (1).** If encryption is unavailable, include no secrets
   and do not upload: fix the crypto first.
3. **Use the system temp dir** (`TMPDIR` / `TEMP` / else `/tmp`) — the scripts do this via `tempfile` / `os.tmpdir()`.
   Never build a pack inside the working tree or a repo.
4. Plaintext archive is deleted before upload (`pack.py`), and receivers clean their own temp (verified).
5. If the far side might lack both runtimes, say so in the message (see Step 3).

**Crypto tier chain (resolved by `scripts/backend.py`, in this order):**

1. `python3` + `cryptography` → HPK2
2. `node` → HPK2 (**zero installs**; the ace when pip is blocked)
3. `openssl` ≥ 1.1.1 → **LEGACY format** (aes-256-cbc + pbkdf2)

Tiers 1 and 2 produce **identical HPK2 bytes**, so swapping between them is invisible to the far side and the
message does not change. They are also **authenticated**: GCM fails hard on any tamper (verified — one flipped
bit ⇒ `unable to authenticate data`).

**⚠️ Tier 3 (openssl) has NO cryptographic integrity.** aead is unavailable in `openssl enc`, so it is
cbc+pbkdf2: unauthenticated and malleable. Verified live: one flipped bit in a legacy pack **decrypted
silently to corrupted content with exit code 0** — no error, garbage output. Accidental corruption may be
caught by gzip's CRC; a _deliberate_ edit can be re-compressed to a valid CRC. So for tier-3 packs the message
MUST carry an out-of-band check: `sha256` of the plaintext archive, sent as its own part, verified after
decryption. Never present a legacy pack as tamper-evident.
`--tier python|node|openssl` forces one; `--force-legacy` is an alias for `--tier openssl`. `backend.py`
refuses to fall through silently: if no tier exists, `pack.py` exits — plaintext never leaves the box.
Show the box's inventory any time: `python3 scripts/backend.py` (prints python/node/openssl/tar versions,
the resolved tier, and the receiver attempt order). Typical web-interface box measured 2026-10-06:
python3 3.12 + cryptography 46.0.6 preinstalled, node 22, openssl 3.0.13 (`-pbkdf2` OK), GNU tar 1.35.

Upload hosts are tried in order (`x0.at` → `temp.sh` → `envs.sh`); the live/dead list is in
`scripts/SERVICES.md`. `--no-upload` prints the message with the artifact path instead.

## Step 3 — return the message (the deliverable)

Copy the printed block verbatim. Its shape:

```
HANDOFF — <title, so the far side knows instantly what this is>
doing: <one line of context>
link: <PART 1>
password: <PART 2>
enc: <encryption type — ALWAYS state it; flag loudly when it is not the default HPK2>
unpack: curl -sL <link> -o pack.asc && <python3 unpack.py|node unpack.js> -k '<password>' pack.asc
```

- Title must be human-meaningful ("{Topic} — {What work was being done}", not "handoff-3").
- **Two-part rule:** send link and password in separate messages when it matters. Lose PART 2 = pack is gone
  forever, no recovery — say that out loud.
- State the enc type even when default: the far side picks its runner from it. `LEGACY openssl` means
  `openssl enc -d -aes-256-cbc -pbkdf2 -in pack.asc -out pack.tar.gz && tar xzf pack.tar.gz`.
  Agent should know immediately what method to use.

---

## Files

| file                         | role                                                                          |
| ---------------------------- | ----------------------------------------------------------------------------- |
| `scripts/handoff.py` / `.js` | core crypto, importable, both do enc AND dec (HPK2: aes-256-gcm + zlib)       |
| `scripts/pack.py` / `.js`    | sender: archive → encrypt → upload → print the message block                  |
| `scripts/unpack.py` / `.js`  | receiver: fetch → decrypt → extract → print manifest                          |
| `scripts/privatebin_pack.py` | alternative transport with server-side expiry (see the paste-service notes)   |
| `scripts/SERVICES.md`        | live/dead upload hosts + paste services, with last-verified dates             |
| `scripts/backend.py`         | tier chain resolution (python → node → openssl), enc/dec dispatch, box survey |
| `scripts/tier_test.py`       | tier matrix: 3 senders × 2 receivers, real uploads, format/announce checks    |
| `scripts/interop_test.py`    | core cross-runtime proof (py↔node, both directions)                           |
| `scripts/e2e_test.py`        | full end-to-end suite: 4 runtime combos, legacy tier, leak + wrong-key checks |

Re-verify before trusting (each needs `node` on PATH; the last two need network):
`python3 scripts/interop_test.py` (41 checks) · `python3 scripts/e2e_test.py` (24) · `python3 scripts/tier_test.py` (14).
Total green as of the last run: **79/79**.
Deep format/PrivateBin detail lives in the `encrypted-handoff-pack` skill; the tools live here.
