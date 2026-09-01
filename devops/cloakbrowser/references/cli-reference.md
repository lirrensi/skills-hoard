# CloakBrowser CLI reference

CloakBrowser ships a small CLI for **binary management**, not browser page automation.

## Commands

### Install the Chromium binary

```bash
pnpm dlx cloakbrowser install
```

If the package is already installed locally:

```bash
pnpm exec cloakbrowser install
```

Downloads the CloakBrowser Chromium binary and prints the installed path.

### Show install info

```bash
pnpm exec cloakbrowser info
```

Shows:

- Chromium version
- platform
- binary path
- whether it is installed
- cache directory
- binary override path, if `CLOAKBROWSER_BINARY_PATH` is set

### Update the binary

```bash
pnpm exec cloakbrowser update
```

Checks for a newer CloakBrowser Chromium build and downloads it if available.

### Clear cache

```bash
pnpm exec cloakbrowser clear-cache
```

Removes cached CloakBrowser binaries.

## Command summary

```text
cloakbrowser install
cloakbrowser info
cloakbrowser update
cloakbrowser clear-cache
```

## Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `CLOAKBROWSER_BINARY_PATH` | — | Use an existing local Chromium binary and skip auto-download |
| `CLOAKBROWSER_CACHE_DIR` | `~/.cloakbrowser` | Change the binary cache directory |
| `CLOAKBROWSER_DOWNLOAD_URL` | upstream default | Override the binary download source |
| `CLOAKBROWSER_AUTO_UPDATE` | `true` | Disable background update checks by setting `false` |
| `CLOAKBROWSER_SKIP_CHECKSUM` | `false` | Skip SHA-256 verification after download |

## Important limitation

This CLI does **not** expose commands like:

- `cloakbrowser open https://...`
- `cloakbrowser click ...`
- `cloakbrowser screenshot ...`

For those tasks, use Node code with the Playwright-like API.
