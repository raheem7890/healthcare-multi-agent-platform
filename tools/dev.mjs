import { existsSync } from 'node:fs'
import { spawn } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const isWindows = process.platform === 'win32'
const npmCommand = isWindows ? 'npm.cmd' : 'npm'
const virtualPython = path.join(root, '.venv', isWindows ? 'Scripts/python.exe' : 'bin/python')
const pythonCommand = process.env.PYTHON_BIN || (existsSync(virtualPython) ? virtualPython : 'python')
const target = process.argv[2] ?? 'all'
const children = []

function start(name, command, args, cwd = root) {
  const child = spawn(command, args, {
    cwd,
    stdio: 'inherit',
    shell: isWindows && command.endsWith('.cmd'),
  })
  child.on('error', (error) => {
    console.error(`${name} failed to start: ${error.message}`)
    shutdown(1)
  })
  child.on('exit', (code) => {
    if (code && code !== 0) console.error(`${name} exited with code ${code}`)
    if (target === 'all') shutdown(code ?? 0)
  })
  children.push(child)
}

function shutdown(code = 0) {
  for (const child of children) {
    if (!child.killed) child.kill()
  }
  process.exit(code)
}

if (!['all', 'api', 'web'].includes(target)) {
  console.error('Usage: node tools/dev.mjs [api|web]')
  process.exit(1)
}

if (target === 'all' || target === 'api') {
  start('FastAPI', pythonCommand, [
    '-m', 'uvicorn', 'app.main:app', '--reload', '--app-dir', 'backend', '--port', '8000',
  ])
}
if (target === 'all' || target === 'web') {
  start('React', npmCommand, ['run', 'dev'], path.join(root, 'frontend'))
}

process.on('SIGINT', () => shutdown(0))
process.on('SIGTERM', () => shutdown(0))
