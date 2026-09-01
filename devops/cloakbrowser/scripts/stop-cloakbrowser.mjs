import { readFile, rm } from 'node:fs/promises'
import path from 'node:path'

const argv = process.argv.slice(2)

function getOption(name, fallback) {
  const i = argv.indexOf(name)
  return i >= 0 && argv[i + 1] ? argv[i + 1] : fallback
}

const stateDir = path.resolve(getOption('--state-dir', './.cloakbrowser-cli'))
const sessionPath = path.join(stateDir, 'session.json')

let session
try {
  session = JSON.parse(await readFile(sessionPath, 'utf8'))
} catch {
  console.error(`No session file found at ${sessionPath}`)
  process.exit(1)
}

try {
  process.kill(session.pid)
  console.log(`Stopped CloakBrowser process ${session.pid}`)
} catch (error) {
  console.error(`Could not stop PID ${session.pid}: ${error.message}`)
}

await rm(sessionPath, { force: true })
