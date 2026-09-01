# Setup

## STEP 0: ENSURE `playwright-cli` EXISTS

Check it first:

```bash
playwright-cli --help
```

If that fails, stop and read:

- `references/install-playwright-cli.md`

Also, before giving command examples or explaining command behavior, consult the
**`playwright-cli` skill** body so command usage matches the real CLI surface.

## Required packages

`start.js` and `pl.js` assume these already exist in the project:

```bash
pnpm add playwright playwright-cli
```

If `playwright-cli` is missing, the scripts stop immediately.

## Normal usage

Step 1:

```bash
node scripts/start.js
```

Optional mode override:

```bash
PW_MODE=desktop node scripts/start.js
PW_MODE=container node scripts/start.js
node scripts/start.js --mode=desktop
node scripts/start.js --mode=container
```

Step 2:

```bash
node scripts/pl.js open https://example.com
node scripts/pl.js snapshot
node scripts/pl.js click e15
node scripts/pl.js close
```

When you are done, prefer a graceful close first:

```bash
node scripts/pl.js close
```

That gives session restore a better chance to bring tabs back cleanly on the next startup.

## What `start.js` does

- checks that `playwright-cli` exists
- checks that `playwright` exists
- creates the stable profile under the user's home directory
- starts Xvfb on Linux if there is no display
- installs Playwright Chromium if needed
- starts the headed browser on port `9222`
- enables best-effort session restore so tabs come back like a normal desktop browser
- writes session info to `~/.playwright-stable-profile/session.json`

## Cleanup rule

Normal cleanup means:

- stop or kill the running browser process if needed
- keep the persistent profile files
- keep tabs/cookies/session data in the profile unless the user explicitly asks to wipe them

Do **not** delete this by default:

```text
~/.playwright-stable-profile/profile/
```

## What `pl.js` does

- loads the saved session info
- silently attaches that stable session name to the running browser
- forwards the command using normal `playwright-cli` command words
- treats `open <url>` as navigation against the already-running browser
- can be used for graceful shutdown with `node scripts/pl.js close`
