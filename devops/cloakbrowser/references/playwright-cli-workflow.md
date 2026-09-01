# CloakBrowser + playwright-cli workflow

This is the closest CLI-driven workflow to "Playwright, but using CloakBrowser stealth".

## Install

```bash
pnpm add cloakbrowser playwright-core playwright-cli
```

## Start CloakBrowser with a CDP port

```bash
node scripts/attach-cloakbrowser.mjs --port 9222 --headed --humanize
```

That helper launches the CloakBrowser Chromium binary with:

- a remote debugging port
- a persistent profile directory
- CloakBrowser stealth args

It prints the endpoint you should attach to.

## Attach playwright-cli

```bash
playwright-cli attach --cdp=http://127.0.0.1:9222
```

After attaching, use regular `playwright-cli` commands.

## Common commands

```bash
playwright-cli goto https://example.com
playwright-cli snapshot
playwright-cli click "text=More information"
playwright-cli type "hello world"
playwright-cli press Enter
playwright-cli screenshot
playwright-cli eval "document.title"
playwright-cli requests
playwright-cli console
```

## Typical full flow

```bash
pnpm add cloakbrowser playwright-core playwright-cli
node scripts/attach-cloakbrowser.mjs --port 9222 --headed --humanize
playwright-cli attach --cdp=http://127.0.0.1:9222
playwright-cli goto https://example.com
playwright-cli snapshot
playwright-cli screenshot --filename=example.png
playwright-cli detach
node scripts/stop-cloakbrowser.mjs
```

## Useful launcher options

### Headed mode

```bash
node scripts/attach-cloakbrowser.mjs --headed
```

### Humanized interactions

```bash
node scripts/attach-cloakbrowser.mjs --humanize
```

### Custom profile dir

```bash
node scripts/attach-cloakbrowser.mjs --profile-dir ./.cloak-profile
```

### Proxy

```bash
node scripts/attach-cloakbrowser.mjs --proxy http://user:pass@host:port
```

### Locale and timezone

```bash
node scripts/attach-cloakbrowser.mjs --locale en-US --timezone America/New_York
```

## Notes

- `playwright-cli detach` detaches the controller session; it does not necessarily stop the external browser.
- `node scripts/stop-cloakbrowser.mjs` stops the launched CloakBrowser process tracked by the helper.
- For sticky login state, reuse the same `--profile-dir`.
- If a target is especially sensitive, prefer headed mode and `--humanize`.
