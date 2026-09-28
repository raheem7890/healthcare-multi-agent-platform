import { existsSync } from 'node:fs'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const isWindows = process.platform === 'win32'
const npmCommand = isWindows ? 'npm.cmd' : 'npm'
const virtualPython = path.join(root, '.venv', isWindows ? 'Scripts/python.exe' : 'bin/python')
const pythonCommand = process.env.PYTHON_BIN || (existsSync(virtualPython) ? virtualPython : 'python')

function run(label, command, args, cwd = root) {
  console.log(`\n${label}`)
  const result = spawnSync(command, args, {
    cwd,
    stdio: 'inherit',
    shell: isWindows && command.endsWith('.cmd'),
  })
  if (result.status !== 0) process.exit(result.status ?? 1)
}

run('Backend tests', pythonCommand, ['-m', 'pytest', 'tests'], path.join(root, 'backend'))
run('Frontend lint', npmCommand, ['run', 'lint'], path.join(root, 'frontend'))
run('Frontend production build', npmCommand, ['run', 'build'], path.join(root, 'frontend'))
