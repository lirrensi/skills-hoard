# Configuration

All default configuration lives in:

```text
scripts/start.js
```

If you want to change behavior, edit the `CONFIG` object there.

## Current fields

```js
const CONFIG = {
  sessionName: 'stable',
  port: 9222,
  browser: 'chromium',
  display: ':99',
  modeOverrideEnv: 'PW_MODE',
  browserReadyTimeoutMs: 20000,
  restoreLastSession: true,
  stateDir: path.join(os.homedir(), '.playwright-stable-profile'),
  profileDir: path.join(os.homedir(), '.playwright-stable-profile', 'profile'),
  url: null,
}
```

## What each field means

- `sessionName` — the named session used by `pl.js`
- `port` — CDP/debugging port for the started browser
- `browser` — current intended browser label; startup uses Playwright Chromium
- `display` — Xvfb display to use on Linux when there is no physical UI
- `modeOverrideEnv` — env var name that can force startup mode
- `browserReadyTimeoutMs` — how long to wait for the browser port to become ready
- `restoreLastSession` — whether startup should explicitly restore the previous browser session
- `stateDir` — where session metadata and logs are stored
- `profileDir` — persistent browser profile directory
- `url` — optional startup page; `null` is better when you want natural session restore

## Startup modes

`start.js` supports two modes:

- `desktop`
- `container`

Selection order:

1. explicit override wins
2. otherwise auto-detect

### Explicit override

By environment variable:

```bash
PW_MODE=desktop node scripts/start.js
PW_MODE=container node scripts/start.js
```

Or by argument:

```bash
node scripts/start.js --mode=desktop
node scripts/start.js --mode=container
```

### Mode behavior

#### Desktop mode

- use the real desktop if available
- do not auto-force Xvfb
- do not auto-add sandbox-disabling Chromium args

#### Container mode

- use Xvfb if there is no display
- add `--no-sandbox`
- add `--disable-setuid-sandbox`
- use more defensive startup assumptions for VPS/container environments

## Session restore behavior

This setup now does best-effort restore using both:

- Chromium launch flag: `--restore-last-session`
- profile preference patching in the `Preferences` file

That combination is meant to behave more like a normal desktop browser reopening where it left off.

## Most common changes

### Change profile location

Edit:

```js
profileDir: path.join(os.homedir(), '.playwright-stable-profile', 'profile')
```

### Change port

Edit:

```js
port: 9222
```

### Change startup page

Edit:

```js
url: null
```

Use `null` if you want session restore to be the default behavior.

### Change session restore behavior

Edit:

```js
restoreLastSession: true
```

### Change Linux virtual display

Edit:

```js
display: ':99'
```

### Change the mode override variable name

Edit:

```js
modeOverrideEnv: 'PW_MODE'
```

### Change browser readiness timeout

Edit:

```js
browserReadyTimeoutMs: 20000
```

## Important rule

Do not try to configure the core startup model through random command-line flags.
This setup is intentionally opinionated. Change the file if you want different defaults.
