const { mkdir, readFile, writeFile } = require('node:fs/promises')
const fs = require('node:fs')
const os = require('node:os')
const path = require('node:path')
const { spawn } = require('node:child_process')
const net = require('node:net')

const RED = '\u001b[31;1m'
const RESET = '\u001b[0m'

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

const SESSION_PATH = path.join(CONFIG.stateDir, 'session.json')
const LOG_PATH = path.join(CONFIG.stateDir, 'browser.log')

function getArgOption(name) {
  const exact = `${name}=`
  const match = process.argv.slice(2).find((arg) => arg.startsWith(exact))
  return match ? match.slice(exact.length) : null
}

function die(message, extraLines = []) {
  console.error(`${RED}${message}${RESET}`)
  for (const line of extraLines) {
    console.error(line)
  }
  process.exit(1)
}

function info(label, value) {
  console.log(`${label}: ${value}`)
}

function runCommand(commandName, commandArgs, options = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(commandName, commandArgs, {
      stdio: options.stdio ?? 'inherit',
      shell: process.platform === 'win32',
      env: options.env ?? process.env,
      detached: options.detached ?? false,
    })

    child.on('error', reject)
    child.on('exit', (code, signal) => resolve({ code, signal, pid: child.pid }))

    if (options.detached) {
      child.unref()
    }
  })
}

function spawnDetached(commandName, commandArgs, options = {}) {
  const child = spawn(commandName, commandArgs, {
    stdio: options.stdio ?? 'ignore',
    shell: process.platform === 'win32',
    env: options.env ?? process.env,
    detached: true,
  })

  child.on('error', (error) => {
    console.error(`${RED}FAILED TO START BACKGROUND PROCESS: ${commandName}${RESET}`)
    console.error(error?.message || String(error))
  })

  child.unref()
  return child.pid
}

function canReachPort(port, timeoutMs = 700) {
  return new Promise((resolve) => {
    const socket = net.createConnection({ host: '127.0.0.1', port, timeout: timeoutMs })
    socket.once('connect', () => {
      socket.destroy()
      resolve(true)
    })
    const fail = () => {
      socket.destroy()
      resolve(false)
    }
    socket.once('timeout', fail)
    socket.once('error', fail)
  })
}

async function waitForPort(port, timeoutMs = 20000) {
  const started = Date.now()
  while (Date.now() - started < timeoutMs) {
    if (await canReachPort(port, 500)) return
    await new Promise((resolve) => setTimeout(resolve, 350))
  }
  throw new Error(`Timed out waiting for port ${port}`)
}

async function resolvePlaywrightCliRunner() {
  const candidates = [
    { command: 'playwright-cli', prefix: [] },
    { command: 'pnpm', prefix: ['exec', 'playwright-cli'] },
  ]

  for (const candidate of candidates) {
    try {
      const result = await runCommand(candidate.command, [...candidate.prefix, '--version'], { stdio: 'ignore' })
      if (result.code === 0) return candidate
    } catch {
      // try next
    }
  }

  die('PLAYWRIGHT-CLI IS NOT INSTALLED.', [
    'INSTALL IT FIRST OR DIE.',
    'SEE: references/install-playwright-cli.md',
  ])
}

function resolvePlaywrightPackage() {
  try {
    return require('playwright')
  } catch {
    die('PLAYWRIGHT PACKAGE IS NOT INSTALLED.', [
      'INSTALL IT FIRST OR DIE.',
      'Example: pnpm add playwright',
    ])
  }
}

function detectMode() {
  const override = getArgOption('--mode') || process.env[CONFIG.modeOverrideEnv]
  if (override) {
    if (override !== 'desktop' && override !== 'container') {
      die(`INVALID MODE OVERRIDE: ${override}`, [
        'Allowed values: desktop, container',
        `Use --mode=desktop or --mode=container, or set ${CONFIG.modeOverrideEnv}.`,
      ])
    }

    return {
      mode: override,
      source: 'override',
      reasons: [`explicit override via ${override === getArgOption('--mode') ? '--mode' : CONFIG.modeOverrideEnv}`],
    }
  }

  const reasons = []
  const hasDisplay = Boolean(process.env.DISPLAY)
  const isLinux = process.platform === 'linux'
  const isCI = Boolean(process.env.CI)
  const isContainer = fs.existsSync('/.dockerenv') || fs.existsSync('/run/.containerenv')

  if (isLinux && !hasDisplay) reasons.push('linux without DISPLAY')
  if (isCI) reasons.push('CI environment detected')
  if (isContainer) reasons.push('container markers detected')

  if (reasons.length > 0) {
    return { mode: 'container', source: 'auto', reasons }
  }

  return {
    mode: 'desktop',
    source: 'auto',
    reasons: [hasDisplay ? `DISPLAY present (${process.env.DISPLAY})` : 'non-linux or local desktop assumptions'],
  }
}

function getXvfbLockPath(display) {
  const match = /^:(\d+)$/.exec(display)
  return match ? `/tmp/.X${match[1]}-lock` : null
}

async function ensureDisplay(modeDecision) {
  if (modeDecision.mode === 'desktop') {
    return { ...process.env, DISPLAY: process.env.DISPLAY ?? null, PW_MODE_SELECTED: modeDecision.mode }
  }

  if (process.platform !== 'linux') {
    die('CONTAINER MODE REQUIRES LINUX OR A REAL DISPLAY STRATEGY.', [
      `Current platform: ${process.platform}`,
      'Use desktop mode instead, or patch start.js for your environment.',
    ])
  }

  if (process.env.DISPLAY) {
    return { ...process.env, PW_MODE_SELECTED: modeDecision.mode }
  }

  const env = { ...process.env, DISPLAY: CONFIG.display, PW_MODE_SELECTED: modeDecision.mode }
  const lockPath = getXvfbLockPath(CONFIG.display)

  if (!lockPath || !fs.existsSync(lockPath)) {
    try {
      spawnDetached('Xvfb', [CONFIG.display, '-screen', '0', '1920x1080x24'], { env })
      await new Promise((resolve) => setTimeout(resolve, 700))
    } catch {
      die('NO DISPLAY AND XVFB COULD NOT BE STARTED.', [
        'INSTALL XVFB OR PROVIDE A REAL DISPLAY.',
        `Expected virtual display: ${CONFIG.display}`,
      ])
    }
  }

  return env
}

async function ensureChromiumInstalled(env) {
  const playwright = resolvePlaywrightPackage()

  if (playwright.chromium.executablePath()) {
    return playwright.chromium.executablePath()
  }

  const result = await runCommand('pnpm', ['exec', 'playwright', 'install', 'chromium'], { env })
  if (result.code !== 0) {
    die('FAILED TO INSTALL PLAYWRIGHT CHROMIUM.', [
      'Try running: pnpm exec playwright install chromium',
    ])
  }

  return playwright.chromium.executablePath()
}

async function loadExistingSession() {
  try {
    return JSON.parse(await readFile(SESSION_PATH, 'utf8'))
  } catch {
    return null
  }
}

function mergeDeep(target, source) {
  for (const [key, value] of Object.entries(source)) {
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      if (!target[key] || typeof target[key] !== 'object' || Array.isArray(target[key])) {
        target[key] = {}
      }
      mergeDeep(target[key], value)
      continue
    }
    target[key] = value
  }
  return target
}

async function patchProfilePreferencesForSessionRestore() {
  const defaultProfileDir = path.join(CONFIG.profileDir, 'Default')
  const preferencesPath = path.join(defaultProfileDir, 'Preferences')

  await mkdir(defaultProfileDir, { recursive: true })

  let preferences = {}
  try {
    preferences = JSON.parse(await readFile(preferencesPath, 'utf8'))
  } catch {
    preferences = {}
  }

  mergeDeep(preferences, {
    browser: {
      check_default_browser: false,
    },
    session: {
      restore_on_startup: 1,
      restore_on_startup_migrated: true,
    },
    profile: {
      exit_type: 'Normal',
      exited_cleanly: true,
    },
  })

  await writeFile(preferencesPath, JSON.stringify(preferences, null, 2))
}

async function main() {
  await resolvePlaywrightCliRunner()
  const modeDecision = detectMode()
  const env = await ensureDisplay(modeDecision)

  info('MODE', modeDecision.mode)
  info('MODE SOURCE', modeDecision.source)
  info('MODE REASONS', modeDecision.reasons.join('; '))

  await mkdir(CONFIG.profileDir, { recursive: true })
  await mkdir(CONFIG.stateDir, { recursive: true })

  if (CONFIG.restoreLastSession) {
    await patchProfilePreferencesForSessionRestore()
  }

  const existing = await loadExistingSession()
  if (existing?.port && (await canReachPort(existing.port))) {
    console.log('STABLE PROFILE ALREADY READY.')
    console.log(`SESSION: ${existing.sessionName}`)
    console.log(`PROFILE: ${existing.profileDir}`)
    console.log(`PORT: ${existing.port}`)
    console.log(`PID: ${existing.pid}`)
    console.log(`DISPLAY: ${existing.display ?? 'native desktop'}`)
    console.log(`LOG: ${existing.logPath ?? LOG_PATH}`)
    return
  }

  const executablePath = await ensureChromiumInstalled(env)
  if (!executablePath) {
    die('COULD NOT RESOLVE CHROMIUM EXECUTABLE.', [
      'Try: pnpm exec playwright install chromium',
    ])
  }

  const logFd = fs.openSync(LOG_PATH, 'a')
  const browserArgs = [
    `--remote-debugging-port=${CONFIG.port}`,
    `--user-data-dir=${CONFIG.profileDir}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--start-maximized',
    ...(CONFIG.restoreLastSession ? ['--restore-last-session'] : []),
    ...(modeDecision.mode === 'container' ? ['--no-sandbox', '--disable-setuid-sandbox'] : []),
    ...(CONFIG.url ? [CONFIG.url] : []),
  ]

  const child = spawn(executablePath, browserArgs, {
    detached: true,
    stdio: ['ignore', logFd, logFd],
    windowsHide: false,
    env,
  })

  child.unref()

  try {
    await waitForPort(CONFIG.port, CONFIG.browserReadyTimeoutMs)
  } catch (error) {
    die(`BROWSER DID NOT BECOME READY ON PORT ${CONFIG.port}.`, [
      error.message,
      `MODE: ${modeDecision.mode}`,
      `DISPLAY: ${env.DISPLAY ?? 'native desktop'}`,
      `LOG: ${LOG_PATH}`,
      'Read the browser log and patch start.js if this environment needs extra launch args.',
    ])
  }

  await writeFile(
    SESSION_PATH,
    JSON.stringify(
      {
        sessionName: CONFIG.sessionName,
        port: CONFIG.port,
        endpoint: `http://127.0.0.1:${CONFIG.port}`,
        browser: CONFIG.browser,
        profileDir: CONFIG.profileDir,
        stateDir: CONFIG.stateDir,
        logPath: LOG_PATH,
        pid: child.pid,
        display: env.DISPLAY ?? null,
        mode: modeDecision.mode,
        modeSource: modeDecision.source,
        modeReasons: modeDecision.reasons,
        restoreLastSession: CONFIG.restoreLastSession,
        startedAt: new Date().toISOString(),
      },
      null,
      2,
    ),
  )

  console.log('STABLE PROFILE READY.')
  console.log(`SESSION: ${CONFIG.sessionName}`)
  console.log(`PROFILE: ${CONFIG.profileDir}`)
  console.log(`PORT: ${CONFIG.port}`)
  console.log(`PID: ${child.pid}`)
  console.log(`DISPLAY: ${env.DISPLAY ?? 'native desktop'}`)
  console.log(`RESTORE LAST SESSION: ${CONFIG.restoreLastSession ? 'enabled' : 'disabled'}`)
  console.log(`LOG: ${LOG_PATH}`)
}

main().catch((error) => {
  console.error(error?.stack || String(error))
  process.exit(1)
})
