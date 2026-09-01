# Install `playwright-cli`

## What this is

`playwright-cli` is the command-line tool whose command words this setup reuses.

Before using `scripts/start.js` or `scripts/pl.js`, make sure `playwright-cli` exists.

## Check whether it exists

```bash
playwright-cli --help
```

If that works, you are good.

## Install options

### Global install

```bash
npm install -g @playwright/cli@latest
```

### Local project install with pnpm

```bash
pnpm add playwright-cli playwright
```

### Local project install with npm

```bash
npm install playwright-cli playwright
```

## Reference

```text
https://github.com/microsoft/playwright-cli
```

## Important rule

If `playwright-cli` does not exist, stop and install it first.
Do not continue into the two-script workflow until this is fixed.
