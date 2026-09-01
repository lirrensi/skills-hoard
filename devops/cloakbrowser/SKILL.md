---
name: cloakbrowser
description: Use this skill whenever the user wants to use CloakBrowser, migrate from Playwright or Puppeteer to CloakBrowser, manage the CloakBrowser binary from the CLI, or do stealth browser automation with a nearly drop-in Playwright API. Trigger on: "cloakbrowser", "CloakBrowser", "stealth playwright", "anti-bot browser automation", "replace playwright with cloakbrowser", "how do I use cloakbrowser from cli", "cloakbrowser install/update/info", or when the user wants Playwright-style browser code but with CloakBrowser stealth.
depends: playwright-cli
---

# CloakBrowser skill

Use this skill to help the user run **CloakBrowser** for **CLI-driven browser automation**
by pairing it with **playwright-cli**. The main trick is to launch CloakBrowser with a
CDP port and then let `playwright-cli attach --cdp=...` drive it almost 1:1.

## First, clarify the user's lane

Figure out which of these they actually want:

1. **CLI automation via playwright-cli** — the default path for this skill
2. **CLI binary management** — install/update/info/clear cache
3. **Playwright-style JS automation** — `launch()`, `launchContext()`, `launchPersistentContext()`
4. **Puppeteer mode** — `import { launch } from 'cloakbrowser/puppeteer'`
5. **Stealth tuning** — proxy, geoip, timezone, locale, `humanize`, persistent profiles
6. **Migration help** — convert existing Playwright code with minimal edits

If the request is vague, ask one short question and offer the likely default:

> Do you want the **playwright-cli attach workflow** for driving CloakBrowser from the
> terminal, or plain **Node code usage**? The sweet spot for CLI automation is:
> launch CloakBrowser with CDP, then control it through playwright-cli.

That distinction matters. Do not pretend CloakBrowser ships a full page-driving CLI.

## Core truth to preserve

CloakBrowser is **almost 1:1 with Playwright at the automation level** once you attach
`playwright-cli` over CDP.

- **Management CLI exists**: `cloakbrowser install|info|update|clear-cache`
- **Automation CLI path**: launch CloakBrowser with CDP, then `playwright-cli attach`
- **Automation API exists**: `launch()`, `launchContext()`, `launchPersistentContext()`
- **Default JS entrypoint is Playwright-compatible**
- **Puppeteer is a separate import path**

When answering, explicitly separate:

- **"management CLI"** from
- **"automation CLI via playwright-cli attach"** from
- **"direct Node automation code"**

## Installation guidance

Prefer `pnpm` in this environment.

### CLI automation stack

```bash
pnpm add cloakbrowser playwright-core playwright-cli
```

### Playwright-style setup

```bash
pnpm add cloakbrowser playwright-core
```

### Puppeteer-style setup

```bash
pnpm add cloakbrowser puppeteer-core
```

### Optional GeoIP support

```bash
pnpm add mmdb-lib
```

Tell the user:

- first launch auto-downloads a Chromium binary (~200MB)
- default cache directory is `~/.cloakbrowser`
- Node.js 20+ is required

## CLI command reference

Read `references/cli-reference.md` when the user asks about shell commands,
binary management, install status, cache locations, or env vars.

## Playwright CLI attach workflow

Read `references/playwright-cli-workflow.md` when the user wants:

- terminal-driven browser automation
- commands like `open`, `goto`, `click`, `fill`, `snapshot`, `screenshot`
- a flow that feels very close to `playwright-cli`
- CloakBrowser stealth with CLI control

## Playwright migration guidance

Read `references/playwright-migration.md` when the user wants to:

- convert existing Playwright code
- launch a headed or headless browser
- use proxies or persistent profiles
- avoid detection issues
- map Playwright calls to CloakBrowser calls

## Bundled helper scripts

If the user wants terminal automation, point them to:

- `scripts/attach-cloakbrowser.mjs` — starts CloakBrowser with a CDP endpoint
- `scripts/stop-cloakbrowser.mjs` — stops the launched browser process
- `scripts/open-url.mjs` — tiny direct Node example

Example:

```bash
pnpm add cloakbrowser playwright-core playwright-cli
node scripts/attach-cloakbrowser.mjs --port 9222 --headed --humanize
playwright-cli attach --cdp=http://127.0.0.1:9222
playwright-cli goto https://example.com
playwright-cli snapshot
```

## Default answer shape

When the user asks how to use CloakBrowser, structure the answer like this:

1. **What CloakBrowser is** in one sentence
2. **Recommended CLI path**: CloakBrowser CDP launch + `playwright-cli attach`
3. **Install command** using `pnpm`
4. **Attach command** and a few `playwright-cli` commands
5. **Smallest working example**
6. **Migration diff** if they mentioned Playwright
7. **Stealth gotchas** only if relevant

## Default CLI automation recipe

```bash
pnpm add cloakbrowser playwright-core playwright-cli
node scripts/attach-cloakbrowser.mjs --port 9222 --headed --humanize
playwright-cli attach --cdp=http://127.0.0.1:9222
playwright-cli goto https://example.com
playwright-cli snapshot
playwright-cli click "text=More information"
playwright-cli screenshot
playwright-cli detach
node scripts/stop-cloakbrowser.mjs
```

## Smallest working Playwright-style example

```ts
import { launch } from 'cloakbrowser'

const browser = await launch({ headless: true })
const page = await browser.newPage()
await page.goto('https://example.com')
console.log(await page.title())
await browser.close()
```

## Migration rules

### Standard Playwright → CloakBrowser

```diff
- import { chromium } from 'playwright-core'
- const browser = await chromium.launch()
+ import { launch } from 'cloakbrowser'
+ const browser = await launch()
```

After that, most page code stays the same:

- `browser.newPage()`
- `page.goto()`
- `page.click()`
- `page.type()`
- `page.screenshot()`
- `browser.close()`

### Context-first usage

If the user wants a single ready-to-use context instead of a browser object, recommend:

```ts
import { launchContext } from 'cloakbrowser'

const context = await launchContext({
  locale: 'en-US',
  timezone: 'America/New_York',
})

const page = await context.newPage()
await page.goto('https://example.com')
await context.close()
```

### Persistent profile usage

If the site detects incognito mode or the user wants session reuse:

```ts
import { launchPersistentContext } from 'cloakbrowser'

const context = await launchPersistentContext({
  userDataDir: './chrome-profile',
  headless: false,
})

const page = context.pages()[0] || await context.newPage()
await page.goto('https://example.com')
await context.close()
```

## Stealth-specific guidance

Only bring these up when relevant:

- Prefer **Playwright mode** over Puppeteer for tougher anti-bot flows
- Prefer **top-level `timezone` and `locale`** instead of `contextOptions.timezoneId` or `contextOptions.locale`
- Use **`launchPersistentContext()`** when incognito detection matters
- Use **`humanize: true`** when behavioral detection matters
- Avoid **`page.waitForTimeout()`** on sensitive flows; prefer native sleeps
- For forms, **`page.type()`** often looks more human than `page.fill()`

## What not to claim

Do not say:

- that CloakBrowser has a full Playwright-style page-driving CLI
- that it replaces Playwright Test
- that it solves CAPTCHAs directly
- that Puppeteer and Playwright have identical stealth results

## If the user wants a shell-only workflow

Be honest and helpful:

1. Explain that upstream CloakBrowser's built-in CLI is only for **binary lifecycle management**.
2. Recommend the **CDP attach workflow** as the closest thing to a Playwright-style CLI.
3. Fall back to a tiny Node script only when attach is not suitable.

## Output preference

Prefer concise, runnable snippets. Keep examples close to upstream API names so the user
can cross-check against official docs without playing archaeology in clown shoes.
