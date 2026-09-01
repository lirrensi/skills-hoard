---
name: playwright-stable-profile
description: Use this skill whenever the user wants Playwright or playwright-cli to reuse a stable real-browser profile with persistent logins, tabs, cookies, or session state. Trigger on: "persistent playwright profile", "reuse chrome profile", "attach playwright to existing browser", "keep logins between runs", "playwright stable profile", "real browser profile for playwright", "launch Chrome with remote debugging and attach", or when the user wants headed browser automation that preserves login state across runs.
depends: playwright-cli
---

# Playwright stable profile skill

Use this skill when the user wants a **two-script headed browser workflow** with a
stable persistent profile.

The workflow is:

0. ensure `playwright-cli` exists
1. `node scripts/start.js`
2. `node scripts/pl.js <PLAYWRIGHT-CLI STYLE COMMAND>`

## STEP 0

Before anything else:

1. check `playwright-cli --help`
2. if it does not exist, stop and redirect to `references/install-playwright-cli.md`
3. consult the **`playwright-cli` skill** body before describing command usage, so command examples follow the real CLI surface

## NON-NEGOTIABLE RULE

**ALWAYS USE HEADED MODE.**

- If a physical desktop exists, use the real visible browser window.
- If no physical desktop exists, use a virtual display workaround such as Xvfb.
- Do not switch to headless mode as the default answer.

The safe default is:

- use **Playwright's default bundled Chromium**
- create a **persistent profile under the user's home directory**
- run the browser in **headed mode with full JS rendering**
- never touch the user's daily live browser profile by default
- keep all startup defaults hardcoded in `scripts/start.js`

The default recommended pattern is:

1. run `node scripts/start.js`
2. wait until it reports the stable profile is ready
3. run `node scripts/pl.js ...`
4. keep it **headed** so sites behave like a real visible browser
5. reuse the same profile next time so tabs, cookies, and logins survive

## Core truth to preserve

The stable session behavior comes from the persistent profile started by `start.js`.

- `start.js` owns setup, browser startup, display bootstrap, and readiness
- `pl.js` owns command forwarding against the already-started session
- the user should not need extra attach steps
- if something must change, edit `scripts/start.js`
- cleanup may kill the running browser process, but must **NOT** delete the persistent profile directory by default
- do not casually delete `~/.playwright-stable-profile/profile/` or wipe browser state during normal recovery

## Recommended default answer shape

When the user asks how to do this, structure the answer like this:

1. explain the two-script model in one sentence
2. show the install command using `pnpm`
3. show `node scripts/start.js`
4. show a few `node scripts/pl.js ...` commands
5. point to configuration or troubleshooting docs if needed

## Installation guidance

Prefer `pnpm` here.

```bash
pnpm add playwright playwright-cli
```

The scripts handle Chromium installation at startup if needed.

## Read these references when needed

- `references/install-playwright-cli.md` — install/check the CLI tool before doing anything else
- `references/setup.md` — exact install and run steps
- `references/configuration.md` — what to change in `scripts/start.js`
- `references/troubleshooting.md` — diagnose failures and stale state

## Bundled scripts

- `scripts/start.js` — full startup and readiness script
- `scripts/pl.js` — command wrapper using Playwright CLI style commands

## Default CLI recipe

```bash
pnpm add playwright playwright-cli
node scripts/start.js
node scripts/pl.js open https://example.com
node scripts/pl.js snapshot
node scripts/pl.js click e15
node scripts/pl.js close
```

This is a **headed** browser flow. Do not switch to headless by default.

### Headed-only realism rule

If the user cares about realism, anti-bot flows, captchas, or browser parity, recommend:

- **ALWAYS USE HEADED MODE**
- full JS rendering in the normal browser process
- virtual display infrastructure when a real desktop cannot be used safely

Do not casually suggest headless mode for these flows.

### What not to claim

Do not say:

- that the user needs a manual attach step
- that the user needs extra helper scripts beyond `start.js` and `pl.js`
- that headless mode is equivalent to a real visible browser for sensitive flows
- that normal cleanup should delete the persistent profile files

## Output preference

Prefer concise, runnable snippets and point directly to `scripts/start.js` for configuration changes.
