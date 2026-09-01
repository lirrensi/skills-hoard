const { readFile } = require('node:fs/promises')
const { spawn } = require('node:child_process')
const path = require('node:path')
const os = require('node:os')

const RED = '\u001b[31;1m'
const RESET = '\u001b[0m'

const argv = process.argv.slice(2)

if (argv.length === 0) {
  console.error('Usage: node scripts/pl.js <EXACT SAME ARGS AS playwright-cli>')
  console.error('Example: node scripts/pl.js snapshot')
  process.exit(1)
}

const STATE_DIR = path.join(os.homedir(), '.playwright-stable-profile')
const SESSION_PATH = path.join(STATE_DIR, 'session.json')
const DEFAULT_SESSION = 'stable'

function hasArg(prefixOrExact) {
  return argv.some((arg) => arg === prefixOrExact || arg.startsWith(`${prefixOrExact}=`))
}

function runCommand(commandName, commandArgs, options = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(commandName, commandArgs, {
      stdio: options.stdio ?? 'inherit',
      shell: process.platform === 'win32',
      env: options.env ?? process.env,
    })

    child.on('error', reject)
    child.on('exit', (code, signal) => resolve({ code, signal }))
  })
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

  console.error(`${RED}PLAYWRIGHT-CLI IS NOT INSTALLED.${RESET}`)
  console.error(`${RED}INSTALL IT FIRST OR DIE.${RESET}`)
  console.error(`${RED}DOING NOTHING ELSE.${RESET}`)
  process.exit(1)
}

async function loadSession() {
  try {
    return JSON.parse(await readFile(SESSION_PATH, 'utf8'))
  } catch {
    console.error(`${RED}STABLE PROFILE SESSION IS NOT READY.${RESET}`)
    console.error(`${RED}RUN NODE SCRIPTS/START.JS FIRST.${RESET}`)
    process.exit(1)
  }
}

async function ensureAttached(runner, env, session) {
  const attachArgs = [`-s=${session.sessionName}`, 'attach', `--cdp=${session.endpoint}`]
  try {
    await runCommand(runner.command, [...runner.prefix, ...attachArgs], {
      env,
      stdio: 'ignore',
    })
  } catch {
    // ignore attach noise and let the real command surface problems
  }
}

async function main() {
  const command = argv.find((arg) => !arg.startsWith('-'))
  if (!command) {
    console.error('Could not determine command from arguments.')
    process.exit(1)
  }

  const session = await loadSession()
  const runner = await resolvePlaywrightCliRunner()
  const env = {
    ...process.env,
    ...(session.display ? { DISPLAY: session.display } : {}),
  }

  await ensureAttached(runner, env, session)

  if (command === 'open') {
    const openIndex = argv.indexOf('open')
    const urlArg = argv.find((arg, index) => index > openIndex && !arg.startsWith('-'))
    const translatedArgs = [`-s=${session.sessionName || DEFAULT_SESSION}`, ...(urlArg ? ['goto', urlArg] : ['snapshot'])]
    const translatedResult = await runCommand(runner.command, [...runner.prefix, ...translatedArgs], { env })

    if (translatedResult.signal) {
      process.kill(process.pid, translatedResult.signal)
      return
    }

    process.exit(translatedResult.code ?? 0)
  }

  const forwardedArgs = [...argv]
  if (!hasArg('-s') && !hasArg('--session')) {
    forwardedArgs.unshift(`-s=${session.sessionName || DEFAULT_SESSION}`)
  }

  const result = await runCommand(runner.command, [...runner.prefix, ...forwardedArgs], { env })
  if (result.signal) {
    process.kill(process.pid, result.signal)
    return
  }

  process.exit(result.code ?? 0)
}

main().catch((error) => {
  console.error(error?.stack || String(error))
  process.exit(1)
})
