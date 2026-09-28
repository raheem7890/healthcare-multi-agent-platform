import { constants, copyFileSync, existsSync } from 'node:fs'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const isWindows = process.platform === 'win32'
const systemPython = process.env.PYTHON_BIN || 'python'
const npmCommand = isWindows ? 'npm.cmd' : 'npm'
const virtualPython = path.join(root, '.venv', isWindows ? 'Scripts/python.exe' : 'bin/python')

function run(command, args, cwd = root) {
  const result = spawnSync(command, args, {
    cwd,
    stdio: 'inherit',
    shell: isWindows && command.endsWith('.cmd'),
  })
  if (result.status !== 0) process.exit(result.status ?? 1)
}

function copyExample(relativeExample, relativeTarget) {
  const example = path.join(root, relativeExample)
  const target = path.join(root, relativeTarget)
  if (!existsSync(target)) {
    copyFileSync(example, target, constants.COPYFILE_EXCL)
    console.log(`Created ${relativeTarget} from ${relativeExample}`)
  }
}

if (!existsSync(virtualPython)) {
  run(systemPython, ['-m', 'venv', '.venv'])
}

run(virtualPython, ['-m', 'pip', 'install', '-r', 'backend/requirements-dev.txt'])
run(npmCommand, ['install'], path.join(root, 'frontend'))
copyExample('backend/.env.example', 'backend/.env')
copyExample('frontend/.env.example', 'frontend/.env')

console.log('\nSetup complete. Start both applications with: npm run dev')
