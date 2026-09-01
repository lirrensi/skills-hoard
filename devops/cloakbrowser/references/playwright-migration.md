# CloakBrowser Playwright migration

## The mental model

Treat CloakBrowser as:

- **Playwright-compatible browser launch layer**
- plus a **small CLI** for binary management

Your page automation code usually stays the same.

## Install

```bash
pnpm add cloakbrowser playwright-core
```

## Fastest migration

### Before

```ts
import { chromium } from 'playwright-core'

const browser = await chromium.launch({ headless: true })
const page = await browser.newPage()
await page.goto('https://example.com')
console.log(await page.title())
await browser.close()
```

### After

```ts
import { launch } from 'cloakbrowser'

const browser = await launch({ headless: true })
const page = await browser.newPage()
await page.goto('https://example.com')
console.log(await page.title())
await browser.close()
```

## Main entrypoints

### `launch()`

Returns a Playwright `Browser`.

Use it when you want the usual pattern:

```ts
const browser = await launch()
const page = await browser.newPage()
```

### `launchContext()`

Returns a ready-to-use `BrowserContext` and closes the underlying browser when the context closes.

Use it when you want context options like:

- `userAgent`
- `viewport`
- `permissions`
- `storageState`
- `extraHTTPHeaders`

Example:

```ts
import { launchContext } from 'cloakbrowser'

const context = await launchContext({
  locale: 'en-US',
  timezone: 'America/New_York',
  contextOptions: {
    storageState: 'state.json',
    permissions: ['geolocation'],
  },
})

const page = await context.newPage()
await page.goto('https://example.com')
await context.close()
```

### `launchPersistentContext()`

Use this when the site dislikes incognito mode or you want cookies/localStorage/session persistence.

```ts
import { launchPersistentContext } from 'cloakbrowser'

const context = await launchPersistentContext({
  userDataDir: './chrome-profile',
  headless: false,
  humanize: true,
})

const page = context.pages()[0] || await context.newPage()
await page.goto('https://example.com')
await context.close()
```

## Option mapping

| Need | CloakBrowser option |
| --- | --- |
| Visible browser | `headless: false` |
| Proxy | `proxy: 'http://user:pass@host:port'` |
| SOCKS5 proxy | `proxy: 'socks5://user:pass@host:port'` |
| Extra Chromium args | `args: ['--flag']` |
| Timezone | top-level `timezone` |
| Locale | top-level `locale` |
| Behavioral stealth | `humanize: true` |
| Sticky browser profile | `launchPersistentContext({ userDataDir })` |
| Arbitrary context settings | `contextOptions: { ... }` |

## Stealth gotchas that matter

### Use top-level `timezone` and `locale`

Do not prefer `contextOptions.timezoneId` or `contextOptions.locale` for stealth-sensitive work.
The wrapper intentionally routes the top-level values through binary flags.

### Prefer Playwright mode for harder targets

If the user is choosing between Playwright and Puppeteer imports, favor Playwright unless they have a strong reason otherwise.

### Avoid `page.waitForTimeout()` in sensitive flows

Use a native sleep instead:

```ts
await new Promise((resolve) => setTimeout(resolve, 3000))
```

### Prefer `page.type()` over `page.fill()` when behavior matters

```ts
await page.type('#email', 'user@example.com', { delay: 50 })
```

## Tiny CLI + script workflow

If the user wants to stay close to the shell, the honest pattern is:

```bash
pnpm add cloakbrowser playwright-core
pnpm exec cloakbrowser install
node script.mjs
```

Example `script.mjs`:

```js
import { launch } from 'cloakbrowser'

const browser = await launch({ headless: false, humanize: true })
const page = await browser.newPage()
await page.goto(process.argv[2] || 'https://example.com')
console.log(await page.title())
await browser.close()
```

Run it with:

```bash
node script.mjs https://example.com
```
