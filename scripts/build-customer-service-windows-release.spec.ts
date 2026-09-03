import { readFile } from 'node:fs/promises'
import { resolve } from 'node:path'
import { describe, expect, it } from 'vitest'

const root = resolve(import.meta.dirname, '..')

async function read(relativePath: string): Promise<string> {
  return readFile(resolve(root, relativePath), 'utf8')
}

describe('customer-service Windows release builder', () => {
  it('uses the official native Windows executable and wheel build routes', async () => {
    const script = await read('scripts/build-customer-service-windows-release.ps1')

    expect(script).toContain("$env:DSH_BUILD_CLIENT_PROFILE = 'official'")
    expect(script).toContain("'--targets=node24-win-x64'")
    expect(script).toContain("'--package', 'sdk'")
    expect(script).toContain("'--platform', 'win-x64'")
    expect(script).toContain("@('310', '311', '312', '313', '314')")
  })

  it('never packages the server-local model credential file', async () => {
    const script = await read('scripts/build-customer-service-windows-release.ps1')

    expect(script).toContain("'customer-service.model.example.json'")
    expect(script).not.toMatch(/Copy-Item[^\n]+customer-service\.model\.json/)
  })

  it('installs exact project wheels offline and refreshes an existing venv', async () => {
    const template = await read('integrations/customer-service-api/windows-release/install.ps1')

    expect(template).toContain('__SDK_WHEEL__')
    expect(template).toContain('__RUNTIME_WHEEL__')
    expect(template).toContain('--no-index')
    expect(template).toContain('--force-reinstall')
  })

  it('starts through the two visible runtime executables directory', async () => {
    const template = await read('integrations/customer-service-api/windows-release/start.ps1')

    expect(template).toContain('runtime\\deepseek-harness-sdk-runtime-win-x64.exe')
    expect(template).toContain('runtime\\deepseek-harness-sdk-runtime-win-x64-rg.exe')
    expect(template).toContain("Set-DefaultEnvironmentVariable 'DCS_DSH_BIN' $Runtime")
  })

  it('keeps every PowerShell file ASCII-safe for Windows PowerShell 5.1', async () => {
    for (const relativePath of [
      'scripts/build-customer-service-windows-release.ps1',
      'integrations/customer-service-api/windows-release/install.ps1',
      'integrations/customer-service-api/windows-release/start.ps1',
    ]) {
      const bytes = await readFile(resolve(root, relativePath))
      expect([...bytes].every(byte => byte <= 0x7f), relativePath).toBe(true)
    }
  })
})
