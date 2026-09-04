/** Server-local database configuration boundary behavior. */

import { mkdirSync, mkdtempSync, realpathSync, renameSync, rmSync, symlinkSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, describe, expect, it } from 'vitest'
import {
  catalogDirectory,
  connectionOptions,
  financeConnectionName,
  loadDatabaseConfig,
  productDomain,
} from '../src/config.ts'

const roots: string[] = []

afterEach(() => {
  for (const root of roots.splice(0)) rmSync(root, { recursive: true, force: true })
})

function fixture(value: unknown, domain = 'kexiaomi'): { root: string; configPath: string } {
  const root = mkdtempSync(join(tmpdir(), 'dsh-customer-database-config-'))
  roots.push(root)
  const runtime = join(root, `${domain}-product-agent`, 'runtime')
  mkdirSync(runtime, { recursive: true })
  const configPath = join(runtime, 'data-access.local.json')
  writeFileSync(configPath, JSON.stringify(value))
  return { root, configPath }
}

function validConfig(): Record<string, unknown> {
  return {
    schemaVersion: 1,
    productCode: 'kexiaomi',
    mainConnectionName: 'MainReadOnly',
    connections: [{
      name: 'MainReadOnly',
      providerName: 'MySql',
      connectionString: 'Server=127.0.0.1;Database=customer_test;User Id=readonly;Password=test-only;',
    }],
    tenantRoutes: [],
    financeFallback: null,
    executionPolicy: {
      readOnly: true,
      commandTimeoutSeconds: 5,
      maxRows: 20,
      maxFields: 16,
      maxJoins: 4,
      maxSerializedCharacters: 12000,
    },
  }
}

describe('loadDatabaseConfig', () => {
  it.each([
    ['kxm_pc', 'kexiaomi'],
    [' KXM_C_MP ', 'kexiaomi'],
    ['kxm_b_mp', 'kexiaomi'],
    ['nutcards_c', 'nutcards'],
    ['NUTCARDS_B_MP', 'nutcards'],
  ])('maps product code %s to %s', (code, domain) => {
    expect(productDomain(code)).toBe(domain)
  })

  it('rejects an unsupported product code', () => {
    expect(() => productDomain('another')).toThrow(/unsupported productCode/u)
  })

  it('rejects a symbolic-link configuration before resolving it', () => {
    const { root, configPath } = fixture(validConfig())
    const target = join(root, 'private-config.json')
    renameSync(configPath, target)
    symlinkSync(target, configPath)

    expect(() => loadDatabaseConfig(root, 'kxm_pc')).toThrow(/cannot use symbolic links/u)
  })

  it.each(['skill', 'runtime'])('rejects a symbolic-link %s directory', (target) => {
    const { root } = fixture(validConfig())
    const skill = join(root, 'kexiaomi-product-agent')
    const runtime = join(skill, 'runtime')
    const original = target === 'skill' ? skill : runtime
    const moved = `${original}-real`
    renameSync(original, moved)
    symlinkSync(moved, original)

    expect(() => loadDatabaseConfig(root, 'kxm_pc')).toThrow(/cannot use symbolic links/u)
  })

  it('loads normalized connection aliases, ignored safe settings, and required TLS', () => {
    const value = validConfig()
    value.connections = [{
      name: 'MainReadOnly',
      providerName: 'mysql',
      connectionString: [
        'Host=database.example.test',
        'Initial Catalog=customer_test',
        'UID=readonly',
        'Pwd=test-only',
        'Port=3307',
        'Ssl Mode=Require',
        'Pooling=false',
        'AllowUserVariables=yes',
        'AllowLoadLocalInfile=no',
        'Minimum Pool Size=0',
        'MaximumPoolSize=10',
        'Connection Timeout=3',
        'DefaultCommandTimeout=5',
        'Charset=utf8mb4',
      ].join(';'),
    }]
    const { root } = fixture(value)
    mkdirSync(join(root, 'kexiaomi-product-agent', 'references', 'database'), { recursive: true })

    const loaded = loadDatabaseConfig(root, 'kxm_pc')
    expect(connectionOptions(loaded, 'MainReadOnly')).toMatchObject({
      host: 'database.example.test',
      database: 'customer_test',
      user: 'readonly',
      password: 'test-only',
      port: 3307,
      ssl: {},
      multipleStatements: false,
    })
    expect(catalogDirectory(root)).toBe(realpathSync(join(root, 'kexiaomi-product-agent', 'references', 'database')))
  })

  it('loads the NutCards product domain with default port and non-required SSL', () => {
    const value = validConfig()
    value.productCode = 'nutcards'
    value.connections = [{
      name: 'MainReadOnly',
      providerName: 'MySql',
      connectionString: 'Data Source=127.0.0.1;Database=cards;Username=readonly;Password=test-only;SslMode=Preferred;',
    }]
    const { root } = fixture(value, 'nutcards')

    expect(connectionOptions(loadDatabaseConfig(root, 'nutcards_c'), 'MainReadOnly')).toMatchObject({
      host: '127.0.0.1', port: 3306,
    })
  })

  it('rejects a catalog directory that resolves outside the skill root', () => {
    const { root } = fixture(validConfig())
    const references = join(root, 'kexiaomi-product-agent', 'references')
    const outside = mkdtempSync(join(tmpdir(), 'dsh-customer-catalog-outside-'))
    roots.push(outside)
    mkdirSync(references, { recursive: true })
    symlinkSync(outside, join(references, 'database'))

    expect(() => catalogDirectory(root)).toThrow(/escapes the skill root/u)
  })

  it('rejects malformed JSON and invalid root configuration records', () => {
    const malformed = fixture(validConfig())
    writeFileSync(malformed.configPath, '{')
    expect(() => loadDatabaseConfig(malformed.root, 'kxm_pc')).toThrow(/invalid JSON/u)

    for (const value of [null, [], {}, { ...validConfig(), schemaVersion: 2 }, { ...validConfig(), productCode: 'nutcards' }, { ...validConfig(), connections: null }, { ...validConfig(), tenantRoutes: null }, { ...validConfig(), financeFallback: [] }]) {
      const current = fixture(value)
      expect(() => loadDatabaseConfig(current.root, 'kxm_pc')).toThrow(/version or product domain/u)
    }
  })

  it('rejects malformed nested records at the JSON boundary', () => {
    const value = validConfig()
    value.connections = [null]
    const { root } = fixture(value)

    expect(() => loadDatabaseConfig(root, 'kxm_pc')).toThrow(/invalid connection record/u)
  })

  it.each([
    [{ name: 1, providerName: 'MySql', connectionString: 'x' }, /invalid connection record/u],
    [{ name: 'Main', providerName: 1, connectionString: 'x' }, /invalid connection record/u],
    [{ name: 'Main', providerName: 'MySql', connectionString: 1 }, /invalid connection record/u],
    [{ name: 'bad-name', providerName: 'MySql', connectionString: 'x' }, /invalid connection name/u],
    [{ name: 'MainReadOnly', providerName: 'Postgres', connectionString: 'x' }, /only MySql/u],
  ])('rejects invalid connection record %#', (record, message) => {
    const value = validConfig()
    value.connections = [record]
    const { root } = fixture(value)
    expect(() => loadDatabaseConfig(root, 'kxm_pc')).toThrow(message)
  })

  it('rejects duplicate connections and invalid or missing main connections', () => {
    const duplicate = validConfig()
    duplicate.connections = [
      ...(duplicate.connections as unknown[]),
      ...(duplicate.connections as unknown[]),
    ]
    expect(() => loadDatabaseConfig(fixture(duplicate).root, 'kxm_pc')).toThrow(/duplicate connection/u)

    const invalidName = validConfig()
    invalidName.mainConnectionName = 'bad-name'
    expect(() => loadDatabaseConfig(fixture(invalidName).root, 'kxm_pc')).toThrow(/invalid main connection name/u)

    const missing = validConfig()
    missing.mainConnectionName = 'Missing'
    expect(() => loadDatabaseConfig(fixture(missing).root, 'kxm_pc')).toThrow(/main connection is missing/u)
  })

  it.each([
    ['broken', /invalid MySQL connection string/u],
    ['Server=;Database=db;User Id=u;Password=p', /invalid MySQL connection setting/u],
    ['Server=a;Server=b;Database=db;User Id=u;Password=p', /invalid MySQL connection setting/u],
    ['Server=a;Database=db;User Id=u;Password=p;Pooling=maybe', /invalid boolean/u],
    ['Server=a;Database=db;User Id=u;Password=p;AllowLoadLocalInfile=true', /must remain disabled/u],
    ['Server=a;Database=db;User Id=u;Password=p;Unknown=x', /unsupported MySQL connection settings/u],
    ['Database=db;User Id=u;Password=p', /requires server/u],
    ['Server=a;User Id=u;Password=p', /requires server/u],
    ['Server=a;Database=db;Password=p', /requires server/u],
    ['Server=a;Database=db;User Id=u', /requires server/u],
    ['Server=a;Database=db;User Id=u;Password=p;Port=0', /invalid MySQL port/u],
    ['Server=a;Database=db;User Id=u;Password=p;Port=65536', /invalid MySQL port/u],
    ['Server=a;Database=db;User Id=u;Password=p;Port=not-a-number', /invalid MySQL port/u],
    ['Server=a;Database=db;User Id=u;Password=p;SslMode=VerifyFull', /unsupported MySQL SslMode/u],
  ])('rejects unsafe connection string %s', (connectionString, message) => {
    const value = validConfig()
    value.connections = [{ name: 'MainReadOnly', providerName: 'MySql', connectionString }]
    expect(() => loadDatabaseConfig(fixture(value).root, 'kxm_pc')).toThrow(message)
  })

  it.each([
    null,
    { readOnly: false, commandTimeoutSeconds: 5, maxRows: 20, maxFields: 16, maxJoins: 4, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: '5', maxRows: 20, maxFields: 16, maxJoins: 4, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 2.5, maxRows: 20, maxFields: 16, maxJoins: 4, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 1, maxRows: 20, maxFields: 16, maxJoins: 4, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 16, maxRows: 20, maxFields: 16, maxJoins: 4, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: '20', maxFields: 16, maxJoins: 4, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 1.5, maxFields: 16, maxJoins: 4, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 0, maxFields: 16, maxJoins: 4, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 21, maxFields: 16, maxJoins: 4, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 20, maxFields: '16', maxJoins: 4, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 20, maxFields: 1.5, maxJoins: 4, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 20, maxFields: 0, maxJoins: 4, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 20, maxFields: 17, maxJoins: 4, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 20, maxFields: 16, maxJoins: '4', maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 20, maxFields: 16, maxJoins: 1.5, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 20, maxFields: 16, maxJoins: -1, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 20, maxFields: 16, maxJoins: 5, maxSerializedCharacters: 12000 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 20, maxFields: 16, maxJoins: 4, maxSerializedCharacters: '12000' },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 20, maxFields: 16, maxJoins: 4, maxSerializedCharacters: 2000.5 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 20, maxFields: 16, maxJoins: 4, maxSerializedCharacters: 1999 },
    { readOnly: true, commandTimeoutSeconds: 5, maxRows: 20, maxFields: 16, maxJoins: 4, maxSerializedCharacters: 30001 },
  ])('rejects execution policy %#', (executionPolicy) => {
    const value = validConfig()
    value.executionPolicy = executionPolicy
    expect(() => loadDatabaseConfig(fixture(value).root, 'kxm_pc')).toThrow(/executionPolicy/u)
  })

  it.each([
    null,
    { connectionName: 1, tenantId: 1, minTenantId: 0, maxTenantId: 0 },
    { connectionName: 'MainReadOnly', tenantId: '1', minTenantId: 0, maxTenantId: 0 },
    { connectionName: 'MainReadOnly', tenantId: 1, minTenantId: '0', maxTenantId: 0 },
    { connectionName: 'MainReadOnly', tenantId: 1, minTenantId: 0, maxTenantId: '0' },
  ])('rejects malformed finance route %#', (route) => {
    const value = validConfig()
    value.tenantRoutes = [route]
    expect(() => loadDatabaseConfig(fixture(value).root, 'kxm_pc')).toThrow(/invalid finance route record/u)
  })

  it.each([
    { modulo: '10', connectionNameTemplate: 'Tenant{index}' },
    { modulo: 10, connectionNameTemplate: 1 },
  ])('rejects malformed finance fallback %#', (financeFallback) => {
    const value = validConfig()
    value.financeFallback = financeFallback
    expect(() => loadDatabaseConfig(fixture(value).root, 'kxm_pc')).toThrow(/invalid finance fallback/u)
  })

  it('requires a fallback when explicit finance routes exist', () => {
    const value = validConfig()
    value.tenantRoutes = [{ tenantId: 1, minTenantId: 0, maxTenantId: 0, connectionName: 'MainReadOnly' }]
    expect(() => loadDatabaseConfig(fixture(value).root, 'kxm_pc')).toThrow(/routes require a fallback/u)
  })

  it.each([
    { modulo: 1.5, connectionNameTemplate: 'Tenant{index}' },
    { modulo: 0, connectionNameTemplate: 'Tenant{index}' },
    { modulo: 101, connectionNameTemplate: 'Tenant{index}' },
    { modulo: 1, connectionNameTemplate: 'bad-template' },
  ])('rejects unsafe finance fallback %#', (financeFallback) => {
    const value = validConfig()
    value.financeFallback = financeFallback
    expect(() => loadDatabaseConfig(fixture(value).root, 'kxm_pc')).toThrow(/invalid finance fallback/u)
  })

  it('requires every deterministic fallback connection', () => {
    const value = validConfig()
    value.financeFallback = { modulo: 2, connectionNameTemplate: 'Tenant{index}' }
    expect(() => loadDatabaseConfig(fixture(value).root, 'kxm_pc')).toThrow(/Tenant0 is missing/u)
  })

  it.each([
    [{ tenantId: 1, minTenantId: 0, maxTenantId: 0, connectionName: 'bad-name' }, /invalid finance route connection name/u],
    [{ tenantId: 1, minTenantId: 0, maxTenantId: 0, connectionName: 'Missing' }, /route connection is missing/u],
    [{ tenantId: 1.5, minTenantId: 0, maxTenantId: 0, connectionName: 'MainReadOnly' }, /invalid finance tenant route/u],
    [{ tenantId: -1, minTenantId: 0, maxTenantId: 0, connectionName: 'MainReadOnly' }, /invalid finance tenant route/u],
    [{ tenantId: 0, minTenantId: -1, maxTenantId: 2, connectionName: 'MainReadOnly' }, /invalid finance tenant range/u],
    [{ tenantId: 0, minTenantId: 2.5, maxTenantId: 3, connectionName: 'MainReadOnly' }, /invalid finance tenant range/u],
    [{ tenantId: 0, minTenantId: 2, maxTenantId: 3.5, connectionName: 'MainReadOnly' }, /invalid finance tenant range/u],
    [{ tenantId: 0, minTenantId: 3, maxTenantId: 2, connectionName: 'MainReadOnly' }, /invalid finance tenant range/u],
  ])('rejects invalid validated route %#', (route, message) => {
    const value = validConfig()
    value.connections = [
      ...(value.connections as unknown[]),
      { name: 'Tenant0', providerName: 'MySql', connectionString: 'Server=a;Database=db;User Id=u;Password=p' },
    ]
    value.financeFallback = { modulo: 1, connectionNameTemplate: 'Tenant{index}' }
    value.tenantRoutes = [route]
    expect(() => loadDatabaseConfig(fixture(value).root, 'kxm_pc')).toThrow(message)
  })

  it('rejects duplicate exact routes and overlapping ranges', () => {
    const base = validConfig()
    base.connections = [
      ...(base.connections as unknown[]),
      { name: 'Tenant0', providerName: 'MySql', connectionString: 'Server=a;Database=db;User Id=u;Password=p' },
    ]
    base.financeFallback = { modulo: 1, connectionNameTemplate: 'Tenant{index}' }
    base.tenantRoutes = [
      { tenantId: 1, minTenantId: 0, maxTenantId: 0, connectionName: 'MainReadOnly' },
      { tenantId: 1, minTenantId: 0, maxTenantId: 0, connectionName: 'MainReadOnly' },
    ]
    expect(() => loadDatabaseConfig(fixture(base).root, 'kxm_pc')).toThrow(/duplicate finance tenant route/u)

    base.tenantRoutes = [
      { tenantId: 0, minTenantId: 1, maxTenantId: 3, connectionName: 'MainReadOnly' },
      { tenantId: 0, minTenantId: 3, maxTenantId: 4, connectionName: 'MainReadOnly' },
    ]
    expect(() => loadDatabaseConfig(fixture(base).root, 'kxm_pc')).toThrow(/overlapping finance tenant ranges/u)
  })

  it('accepts non-overlapping explicit finance ranges', () => {
    const value = validConfig()
    value.connections = [
      ...(value.connections as unknown[]),
      { name: 'Tenant0', providerName: 'MySql', connectionString: 'Server=a;Database=db;User Id=u;Password=p' },
    ]
    value.financeFallback = { modulo: 1, connectionNameTemplate: 'Tenant{index}' }
    value.tenantRoutes = [
      { tenantId: 0, minTenantId: 1, maxTenantId: 2, connectionName: 'MainReadOnly' },
      { tenantId: 0, minTenantId: 3, maxTenantId: 4, connectionName: 'MainReadOnly' },
    ]

    expect(loadDatabaseConfig(fixture(value).root, 'kxm_pc').tenantRoutes).toHaveLength(2)
  })

  it('resolves exact, ranged, and deterministic finance connections', () => {
    const value = validConfig()
    value.connections = [
      ...(value.connections as unknown[]),
      { name: 'Tenant0', providerName: 'MySql', connectionString: 'Server=a;Database=db0;User Id=u;Password=p' },
      { name: 'Tenant1', providerName: 'MySql', connectionString: 'Server=a;Database=db1;User Id=u;Password=p' },
    ]
    value.financeFallback = { modulo: 2, connectionNameTemplate: 'Tenant{index}' }
    value.tenantRoutes = [
      { tenantId: 9, minTenantId: 0, maxTenantId: 0, connectionName: 'MainReadOnly' },
      { tenantId: 0, minTenantId: 10, maxTenantId: 19, connectionName: 'Tenant0' },
    ]
    const loaded = loadDatabaseConfig(fixture(value).root, 'kxm_pc')

    expect(financeConnectionName(loaded, 9)).toBe('MainReadOnly')
    expect(financeConnectionName(loaded, 12)).toBe('Tenant0')
    expect(financeConnectionName(loaded, 21)).toBe('Tenant1')
  })

  it('rejects an unavailable finance or requested connection', () => {
    const loaded = loadDatabaseConfig(fixture(validConfig()).root, 'kxm_pc')
    expect(() => financeConnectionName(loaded, 3)).toThrow(/not configured/u)
    expect(() => connectionOptions(loaded, 'Missing')).toThrow(/requested connection is missing/u)
  })
})
