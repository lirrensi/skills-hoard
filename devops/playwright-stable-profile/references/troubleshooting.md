# Troubleshooting

## `PLAYWRIGHT-CLI IS NOT INSTALLED.`

Install it first:

```bash
pnpm add playwright-cli
```

## `PLAYWRIGHT PACKAGE IS NOT INSTALLED.`

Install it first:

```bash
pnpm add playwright
```

## `FAILED TO INSTALL PLAYWRIGHT CHROMIUM.`

Try the install directly:

```bash
pnpm exec playwright install chromium
```

## `NO DISPLAY AND XVFB COULD NOT BE STARTED.`

This usually means Linux without a desktop and without Xvfb.

Fix one of these:

- provide a real display / desktop session
- install Xvfb

If auto-detect picked the wrong mode, force one explicitly:

```bash
PW_MODE=desktop node scripts/start.js
PW_MODE=container node scripts/start.js
```

## `BROWSER DID NOT BECOME READY ON PORT 9222.`

Likely causes:

- browser failed to launch
- port already in use
- display/Xvfb problem
- wrong startup mode for the environment
- sandbox issue on VPS/container

Check the log file:

```text
~/.playwright-stable-profile/browser.log
```

Also check what mode startup selected:

- `MODE:`
- `MODE SOURCE:`
- `MODE REASONS:`

If needed, rerun with an explicit override:

```bash
PW_MODE=desktop node scripts/start.js
PW_MODE=container node scripts/start.js
```

## `STABLE PROFILE SESSION IS NOT READY.`

Run startup first:

```bash
node scripts/start.js
```

## Browser opens but commands behave strangely

Try these in order:

1. close the existing browser window started by this setup
2. delete only `~/.playwright-stable-profile/session.json`
3. rerun:

```bash
node scripts/start.js
```

Do **not** delete the persistent profile directory unless the user explicitly wants to wipe browser state:

```text
~/.playwright-stable-profile/profile/
```

Deleting `session.json` is a reconnect/reset step.
Deleting the profile directory is destructive state loss.

## Do tabs survive restart?

### While the browser stays running

Yes. Tabs stay because the same live browser process and profile are still in use.

### After killing the browser and starting again

Best effort: yes.

The setup now tries to restore the last browser session by:

- launching Chromium with `--restore-last-session`
- patching profile preferences for restore behavior

Still, the most reliable path is:

1. close gracefully with:

```bash
node scripts/pl.js close
```

2. then start again with:

```bash
node scripts/start.js
```

Hard kills can still reduce restore reliability on some systems.

## Need to inspect saved state paths

Main files:

```text
~/.playwright-stable-profile/session.json
~/.playwright-stable-profile/browser.log
~/.playwright-stable-profile/profile/
```
