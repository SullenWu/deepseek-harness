import { spawnSync } from 'node:child_process'
import { resolve } from 'node:path'

const root = resolve(import.meta.dirname, '..')

function git(args: string[]): string {
  const result = spawnSync('git', args, { cwd: root, encoding: 'utf8' })
  if (result.error !== undefined) throw result.error
  if (result.status !== 0) throw new Error(result.stderr.trim() || `git exited with status ${result.status}`)
  return result.stdout
}

const staged = git(['diff', '--cached', '--name-only', '-z'])
  .split('\0')
  .filter(path => path !== '')

const vendorSourceChanges = staged.filter(path => /^vendor\/[^/]+\/(?:src\/|bin\.js$)/.test(path))
const manifestChanged = staged.includes('vendor/README.md')

if (vendorSourceChanges.length > 0 && !manifestChanged) {
  console.error('vendor manifest guard: vendored SOURCE changed without updating vendor/README.md:')
  for (const path of vendorSourceChanges) console.error(`  ${path}`)
  console.error('Log the modification in vendor/README.md ("Local modifications") and stage it.')
  process.exit(1)
}
