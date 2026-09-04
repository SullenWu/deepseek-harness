/** Load the server-local MySQL connection catalog and enforce its hard safety limits. */

import { lstatSync, readFileSync, realpathSync } from 'node:fs'
import { join, relative, resolve } from 'node:path'
import type { ConnectionOptions } from 'mysql2/promise'

interface NamedConnectionFile {
  name: string
  providerName: string
  connectionString: string
}

interface TenantRoute {
  tenantId: number
  minTenantId: number
  maxTenantId: number
  connectionName: string
}

interface FinanceFallback {
  modulo: number
  connectionNameTemplate: string
}

/** Query limits supplied by a reviewed server-local file. */
export interface ExecutionPolicy {
  /** Must remain true. */
  readOnly: boolean
  /** Server-side query timeout. */
  commandTimeoutSeconds: number
  /** Maximum returned rows. */
  maxRows: number
  /** Maximum selected fields. */
  maxFields: number
  /** Maximum joins. */
  maxJoins: number
  /** Maximum serialized model-facing result size. */
  maxSerializedCharacters: number
}

interface DatabaseConfigFile {
  schemaVersion: number
  productCode: string
  mainConnectionName: string
  connections: NamedConnectionFile[]
  tenantRoutes: TenantRoute[]
  financeFallback: FinanceFallback | null
  executionPolicy: ExecutionPolicy
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

/** Immutable database configuration used by one request-local Harness process. */
export interface DatabaseConfig {
  /** Product data domain selected by the transport. */
  productCode: 'kexiaomi' | 'nutcards'
  /** Main database connection name. */
  mainConnectionName: string
  /** Parsed MySQL connection options keyed by reviewed logical name. */
  connections: ReadonlyMap<string, ConnectionOptions>
  /** Explicit finance routes. */
  tenantRoutes: readonly TenantRoute[]
  /** Deterministic finance fallback. */
  financeFallback: FinanceFallback | null
  /** Validated execution limits. */
  executionPolicy: ExecutionPolicy
}

const CONNECTION_NAME = /^[A-Za-z][A-Za-z0-9_]{0,63}$/u
const CONNECTION_TEMPLATE = /^[A-Za-z][A-Za-z0-9_]{0,48}\{index\}[A-Za-z0-9_]{0,15}$/u

/**
 * Convert a supported customer-service product code to its database domain.
 * @param productCode - Trusted transport product code.
 * @returns Product data domain.
 */
export function productDomain(productCode: string): 'kexiaomi' | 'nutcards' {
  const value = productCode.trim().toLocaleLowerCase()
  if (['kxm_pc', 'kxm_c_mp', 'kxm_b_mp'].includes(value)) return 'kexiaomi'
  if (['nutcards_c', 'nutcards_b_mp'].includes(value)) return 'nutcards'
  throw new Error('customer-service-database: unsupported productCode')
}

function assertChild(root: string, child: string): string {
  const rootReal = realpathSync(root)
  const childReal = realpathSync(child)
  const rel = relative(rootReal, childReal)
  if (rel === '' || rel.startsWith('..') || resolve(rootReal, rel) !== childReal) {
    throw new Error('customer-service-database: database configuration path escapes the skill root')
  }
  return childReal
}

function requiredName(value: string, label: string): string {
  const name = value.trim()
  if (!CONNECTION_NAME.test(name)) throw new Error(`customer-service-database: invalid ${label}`)
  return name
}

function parseBoolean(value: string): boolean {
  if (/^(true|1|yes)$/iu.test(value)) return true
  if (/^(false|0|no)$/iu.test(value)) return false
  throw new Error('invalid boolean connection setting')
}

function parseConnectionString(connectionString: string): ConnectionOptions {
  const settings = new Map<string, string>()
  for (const segment of connectionString.split(';')) {
    if (segment.trim() === '') continue
    const equals = segment.indexOf('=')
    if (equals < 1) throw new Error('customer-service-database: invalid MySQL connection string')
    const key = segment.slice(0, equals).trim().replaceAll(' ', '').toLocaleLowerCase()
    const value = segment.slice(equals + 1).trim()
    if (value === '' || settings.has(key)) throw new Error('customer-service-database: invalid MySQL connection setting')
    settings.set(key, value)
  }
  const take = (...keys: string[]): string | undefined => {
    for (const key of keys) {
      const normalized = key.replaceAll(' ', '').toLocaleLowerCase()
      const value = settings.get(normalized)
      if (value !== undefined) {
        settings.delete(normalized)
        return value
      }
    }
    return undefined
  }
  const host = take('server', 'host', 'data source')
  const database = take('database', 'initial catalog')
  const user = take('user id', 'uid', 'user', 'username')
  const password = take('password', 'pwd')
  const portText = take('port')
  const sslMode = take('sslmode', 'ssl mode')?.toLocaleLowerCase()
  const ignoredBooleanKeys = ['pooling', 'allowuservariables', 'allowloadlocalinfile']
  for (const key of ignoredBooleanKeys) {
    const value = take(key)
    if (value !== undefined) {
      const enabled = parseBoolean(value)
      if (key === 'allowloadlocalinfile' && enabled) {
        throw new Error('customer-service-database: AllowLoadLocalInfile must remain disabled')
      }
    }
  }
  for (const key of [
    'minimum pool size', 'minimumpoolsize', 'maximum pool size', 'maximumpoolsize',
    'connection timeout', 'connectiontimeout', 'default command timeout', 'defaultcommandtimeout', 'charset',
  ]) take(key)
  if (settings.size > 0) {
    throw new Error(`customer-service-database: unsupported MySQL connection settings: ${[...settings.keys()].join(', ')}`)
  }
  if (host === undefined || database === undefined || user === undefined || password === undefined) {
    throw new Error('customer-service-database: MySQL connection requires server, database, user, and password')
  }
  const port = portText === undefined ? 3306 : Number(portText)
  if (!Number.isSafeInteger(port) || port < 1 || port > 65_535) throw new Error('customer-service-database: invalid MySQL port')
  if (sslMode !== undefined && !['none', 'disabled', 'preferred', 'prefer', 'required', 'require'].includes(sslMode)) {
    throw new Error('customer-service-database: unsupported MySQL SslMode')
  }
  return {
    host,
    database,
    user,
    password,
    port,
    namedPlaceholders: false,
    multipleStatements: false,
    supportBigNumbers: true,
    bigNumberStrings: true,
    dateStrings: true,
    ...(sslMode === 'required' || sslMode === 'require' ? { ssl: {} } : {}),
  }
}

function assertPolicy(policy: unknown): asserts policy is ExecutionPolicy {
  if (!isRecord(policy)
    || policy.readOnly !== true
    || typeof policy.commandTimeoutSeconds !== 'number'
    || !Number.isSafeInteger(policy.commandTimeoutSeconds)
    || policy.commandTimeoutSeconds < 2
    || policy.commandTimeoutSeconds > 15
    || typeof policy.maxRows !== 'number'
    || !Number.isSafeInteger(policy.maxRows)
    || policy.maxRows < 1
    || policy.maxRows > 20
    || typeof policy.maxFields !== 'number'
    || !Number.isSafeInteger(policy.maxFields)
    || policy.maxFields < 1
    || policy.maxFields > 16
    || typeof policy.maxJoins !== 'number'
    || !Number.isSafeInteger(policy.maxJoins)
    || policy.maxJoins < 0
    || policy.maxJoins > 4
    || typeof policy.maxSerializedCharacters !== 'number'
    || !Number.isSafeInteger(policy.maxSerializedCharacters)
    || policy.maxSerializedCharacters < 2_000
    || policy.maxSerializedCharacters > 30_000) {
    throw new Error('customer-service-database: executionPolicy is invalid or exceeds hard safety limits')
  }
}

function validateRoutes(config: DatabaseConfig): void {
  const exact = new Set<number>()
  const ranges: TenantRoute[] = []
  for (const route of config.tenantRoutes) {
    requiredName(route.connectionName, 'finance route connection name')
    if (!config.connections.has(route.connectionName)) throw new Error('customer-service-database: finance route connection is missing')
    if (!Number.isSafeInteger(route.tenantId) || route.tenantId < 0) throw new Error('customer-service-database: invalid finance tenant route')
    if (route.tenantId > 0 && exact.has(route.tenantId)) throw new Error('customer-service-database: duplicate finance tenant route')
    if (route.tenantId > 0) exact.add(route.tenantId)
    const hasRange = route.minTenantId !== 0 || route.maxTenantId !== 0
    if (hasRange) {
      if (!Number.isSafeInteger(route.minTenantId)
        || !Number.isSafeInteger(route.maxTenantId)
        || route.minTenantId < 0
        || route.maxTenantId < route.minTenantId) {
        throw new Error('customer-service-database: invalid finance tenant range')
      }
      ranges.push(route)
    }
  }
  for (const [left, leftRoute] of ranges.entries()) {
    for (const rightRoute of ranges.slice(left + 1)) {
      if (leftRoute.minTenantId <= rightRoute.maxTenantId
        && rightRoute.minTenantId <= leftRoute.maxTenantId) {
        throw new Error('customer-service-database: overlapping finance tenant ranges')
      }
    }
  }
}

/**
 * Load `runtime/data-access.local.json` from the transport-selected product skill.
 * @param skillRoot - Server-owned root containing product skill directories.
 * @param requestedProductCode - Trusted transport product code.
 * @returns Parsed immutable connection catalog and policy.
 */
export function loadDatabaseConfig(skillRoot: string, requestedProductCode: string): DatabaseConfig {
  const domain = productDomain(requestedProductCode)
  const skillName = domain === 'kexiaomi' ? 'kexiaomi-product-agent' : 'nutcards-product-agent'
  const requestedSkillDirectory = join(skillRoot, skillName)
  const requestedRuntimeDirectory = join(requestedSkillDirectory, 'runtime')
  const requestedConfigPath = join(requestedRuntimeDirectory, 'data-access.local.json')
  if (lstatSync(requestedSkillDirectory).isSymbolicLink()
    || lstatSync(requestedRuntimeDirectory).isSymbolicLink()
    || lstatSync(requestedConfigPath).isSymbolicLink()) {
    throw new Error('customer-service-database: data access configuration cannot use symbolic links')
  }
  const skillDirectory = assertChild(skillRoot, requestedSkillDirectory)
  const runtimeDirectory = assertChild(skillDirectory, requestedRuntimeDirectory)
  const configPath = assertChild(runtimeDirectory, requestedConfigPath)
  let parsed: unknown
  try {
    parsed = JSON.parse(readFileSync(configPath, 'utf8')) as unknown
  } catch (error) {
    throw new Error('customer-service-database: data access configuration is invalid JSON', { cause: error })
  }
  if (!isRecord(parsed)
    || parsed.schemaVersion !== 1
    || parsed.productCode !== domain
    || !Array.isArray(parsed.connections)
    || !Array.isArray(parsed.tenantRoutes)
    || !(parsed.financeFallback === null || isRecord(parsed.financeFallback))) {
    throw new Error('customer-service-database: data access configuration version or product domain is invalid')
  }
  assertPolicy(parsed.executionPolicy)
  const file = parsed as unknown as DatabaseConfigFile
  const connections = new Map<string, ConnectionOptions>()
  for (const item of file.connections) {
    if (!isRecord(item)
      || typeof item.name !== 'string'
      || typeof item.providerName !== 'string'
      || typeof item.connectionString !== 'string') {
      throw new Error('customer-service-database: invalid connection record')
    }
    const name = requiredName(item.name, 'connection name')
    if (item.providerName.toLocaleLowerCase() !== 'mysql') throw new Error('customer-service-database: only MySql connections are supported')
    if (connections.has(name)) throw new Error('customer-service-database: duplicate connection name')
    connections.set(name, parseConnectionString(item.connectionString))
  }
  const mainConnectionName = requiredName(file.mainConnectionName, 'main connection name')
  if (!connections.has(mainConnectionName)) throw new Error('customer-service-database: main connection is missing')
  for (const route of file.tenantRoutes) {
    if (!isRecord(route)
      || typeof route.connectionName !== 'string'
      || typeof route.tenantId !== 'number'
      || typeof route.minTenantId !== 'number'
      || typeof route.maxTenantId !== 'number') {
      throw new Error('customer-service-database: invalid finance route record')
    }
  }
  if (file.financeFallback !== null
    && (typeof file.financeFallback.modulo !== 'number'
      || typeof file.financeFallback.connectionNameTemplate !== 'string')) {
    throw new Error('customer-service-database: invalid finance fallback')
  }
  const config: DatabaseConfig = {
    productCode: domain,
    mainConnectionName,
    connections,
    tenantRoutes: file.tenantRoutes,
    financeFallback: file.financeFallback,
    executionPolicy: file.executionPolicy,
  }
  if (config.tenantRoutes.length > 0 && config.financeFallback === null) {
    throw new Error('customer-service-database: finance routes require a fallback')
  }
  if (config.financeFallback !== null) {
    if (!Number.isSafeInteger(config.financeFallback.modulo)
      || config.financeFallback.modulo < 1
      || config.financeFallback.modulo > 100
      || !CONNECTION_TEMPLATE.test(config.financeFallback.connectionNameTemplate)) {
      throw new Error('customer-service-database: invalid finance fallback')
    }
    for (let index = 0; index < config.financeFallback.modulo; index++) {
      const name = config.financeFallback.connectionNameTemplate.replace('{index}', String(index))
      if (!config.connections.has(name)) throw new Error(`customer-service-database: finance fallback connection ${name} is missing`)
    }
  }
  validateRoutes(config)
  return config
}

/**
 * Resolve a finance connection without trying alternate shards.
 * @param config - Validated database config.
 * @param tenantId - Live tenant id from identity validation.
 * @returns Reviewed logical connection name.
 */
export function financeConnectionName(config: DatabaseConfig, tenantId: number): string {
  const exact = config.tenantRoutes.find(route => route.tenantId === tenantId)?.connectionName
  const ranged = config.tenantRoutes.find(route =>
    (route.minTenantId !== 0 || route.maxTenantId !== 0)
    && tenantId >= route.minTenantId
    && tenantId <= route.maxTenantId)?.connectionName
  const fallback = config.financeFallback === null
    ? undefined
    : config.financeFallback.connectionNameTemplate.replace('{index}', String(tenantId % config.financeFallback.modulo))
  const name = exact ?? ranged ?? fallback
  if (name === undefined || !config.connections.has(name)) throw new Error('customer-service-database: finance connection is not configured for this tenant')
  return name
}

/**
 * Return a connection while keeping credentials inside this module.
 * @param config - Validated database configuration.
 * @param name - Reviewed logical connection name.
 * @returns Parsed MySQL options for the named connection.
 */
export function connectionOptions(config: DatabaseConfig, name: string): ConnectionOptions {
  const options = config.connections.get(name)
  if (options === undefined) throw new Error('customer-service-database: requested connection is missing')
  return options
}

/**
 * Return the directory containing the shared reviewed query catalog.
 * @param skillRoot - Absolute product-skill root selected by the server.
 * @returns Canonical catalog directory inside the Kexiaomi skill.
 */
export function catalogDirectory(skillRoot: string): string {
  return assertChild(skillRoot, join(skillRoot, 'kexiaomi-product-agent', 'references', 'database'))
}
