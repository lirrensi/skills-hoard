import { buildLaunchOptions } from 'cloakbrowser'
import { mkdir, writeFile } from 'node:fs/promises'
import fs from 'node:fs'
import path from 'node:path'
import { spawn } from 'node:child_process'

const argv = process.argv.slice(2)

function getFlag(name) {
  return argv.includes(name)
}

function getOption(name, fallback) {
  const i = argv.indexOf(name)
  return i >= 0 && argv[i + 1] ? argv[i + 1] : fallback
}

const port = Number(getOption('--port', '9222'))
const headed = getFlag('--headed')
const humanize = getFlag('--humanize')
const proxy = getOption('--proxy')
const locale = getOption('--locale')
const timezone = getOption('--timezone')
const profileDir = path.resolve(getOption('--profile-dir', './.cloakbrowser-cli/profile'))
const stateDir = path.resolve(getOption('--state-dir', './.cloakbrowser-cli'))
const startUrl = getOption('--url', 'about:blank')

await mkdir(profileDir, { recursive: true })
await mkdir(stateDir, { recursive: true })

const launchOptions = await buildLaunchOptions({
  headless: !headed,
  humanize,
  ...(proxy ? { proxy } : {}),
  ...(locale ? { locale } : {}),
  ...(timezone ? { timezone } : {}),
})

const browserArgs = [
  ...(launchOptions.args ?? []),
  `--remote-debugging-port=${port}`,
  `--user-data-dir=${profileDir}`,
  startUrl,
]

const logPath = path.join(stateDir, 'cloakbrowser.log')
const sessionPath = path.join(stateDir, 'session.json')
const logFd = fs.openSync(logPath, 'a')

const child = spawn(launchOptions.executablePath, browserArgs, {
  detached: true,
  stdio: ['ignore', logFd, logFd],
  windowsHide: false,
})

child.unref()

await writeFile(
  sessionPath,
  JSON.stringify(
    {
      pid: child.pid,
      port,
      endpoint: `http://127.0.0.1:${port}`,
      profileDir,
      stateDir,
      logPath,
      startedAt: new Date().toISOString(),
      executablePath: launchOptions.executablePath,
    },
    null,
    2,
  ),
)

console.log(`CloakBrowser started.`)
console.log(`CDP endpoint: http://127.0.0.1:${port}`)
console.log(`PID: ${child.pid}`)
console.log(`Profile: ${profileDir}`)
console.log(`Log: ${logPath}`)
console.log('Attach with:')
console.log(`playwright-cli attach --cdp=http://127.0.0.1:${port}`)
