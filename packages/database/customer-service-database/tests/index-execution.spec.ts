/** Model-facing database tool registration, execution, and presentation. */

import { Context } from '@deepseek-ai/cordis'
import SystemPrompt from '@deepseek-ai/dsh-system-prompt'
import ToolRuntime, { type ToolRunContext } from '@deepseek-ai/dsh-tools'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const dependencies = vi.hoisted(() => ({
  catalogDirectory: vi.fn(),
  compileQuery: vi.fn(),
  connectionOptions: vi.fn(),
  executeReadOnly: vi.fn(),
  financeConnectionName: vi.fn(),
  loadCatalog: vi.fn(),
  loadDatabaseConfig: vi.fn(),
  searchCatalog: vi.fn(),
  verifyDatabaseScope: vi.fn(),
}))

vi.mock('../src/config.ts', () => ({
  catalogDirectory: dependencies.catalogDirectory,
  connectionOptions: dependencies.connectionOptions,
  financeConnectionName: dependencies.financeConnectionName,
  loadDatabaseConfig: dependencies.loadDatabaseConfig,
}))
vi.mock('../src/catalog.ts', () => ({
  loadCatalog: dependencies.loadCatalog,
  searchCatalog: dependencies.searchCatalog,
}))
vi.mock('../src/compiler.ts', () => ({ compileQuery: dependencies.compileQuery }))
vi.mock('../src/mysql.ts', () => ({
  executeReadOnly: dependencies.executeReadOnly,
  verifyDatabaseScope: dependencies.verifyDatabaseScope,
}))

import { apply, type Config } from '../src/index.ts'

const signal = new AbortController().signal
const runContext = { signal } as ToolRunContext
const catalog = { tables: [], relations: [] }
const searchResult = { matches: [], relations: [], totalMatches: 0, truncated: false }

function pluginConfig(overrides: Partial<Config> = {}): Config {
  return {
    skillRoot: '/skills',
    productCode: 'kxm_pc',
    storeId: 12,
    operatorUid: 34,
    merchantProfileVerified: true,
    ...overrides,
  }
}

function databaseConfig(overrides: Record<string, unknown> = {}) {
  return {
    productCode: 'kexiaomi',
    mainConnectionName: 'main',
    connections: new Map(),
    tenantRoutes: [],
    financeFallback: null,
    executionPolicy: {
      readOnly: true,
      commandTimeoutSeconds: 5,
      maxRows: 20,
      maxFields: 16,
      maxJoins: 4,
      maxSerializedCharacters: 12_000,
    },
    ...overrides,
  }
}

function compiledQuery(overrides: Record<string, unknown> = {}) {
  return {
    sql: 'SELECT `card_name` FROM `user_card` WHERE `store_id` = ? LIMIT 10',
    parameters: [12],
    dataSource: 'main',
    outputNames: ['cardName'],
    limit: 10,
    ...overrides,
  }
}

function queryArgs(overrides: Record<string, unknown> = {}) {
  return {
    dataSource: 'main',
    root: { table: 'user_card', alias: 'card' },
    select: [{ tableAlias: 'card', column: 'card_name', outputName: 'cardName' }],
    ...overrides,
  }
}

async function mount(config = pluginConfig()): Promise<Context> {
  const ctx = new Context()
  await ctx.plugin(SystemPrompt)
  await ctx.plugin(ToolRuntime)
  apply(ctx, config)
  return ctx
}

beforeEach(() => {
  vi.clearAllMocks()
  dependencies.loadDatabaseConfig.mockReturnValue(databaseConfig())
  dependencies.catalogDirectory.mockReturnValue('/skills/catalog')
  dependencies.loadCatalog.mockReturnValue(catalog)
  dependencies.searchCatalog.mockReturnValue(searchResult)
  dependencies.connectionOptions.mockImplementation((_config: unknown, name: string) => ({ host: name }))
  dependencies.financeConnectionName.mockReturnValue('finance-56')
  dependencies.verifyDatabaseScope.mockResolvedValue({
    storeId: 12,
    tenantId: 56,
    operatorUid: 34,
    utcOffsetHours: 8,
  })
  dependencies.compileQuery.mockReturnValue(compiledQuery())
  dependencies.executeReadOnly.mockResolvedValue([{ cardName: 'Morning Yoga' }])
})

describe('customer-service database tool entry', () => {
  it.each([
    { merchantProfileVerified: false },
    { storeId: 1.5 },
    { storeId: 0 },
    { operatorUid: 1.5 },
    { operatorUid: 0 },
  ])('rejects invalid trusted request scope %#', async (overrides) => {
    const ctx = new Context()
    await ctx.plugin(SystemPrompt)
    await ctx.plugin(ToolRuntime)

    expect(() => { apply(ctx, pluginConfig(overrides)) }).toThrow(/verified merchant/u)
    expect(dependencies.loadDatabaseConfig).not.toHaveBeenCalled()
  })

  it.each([0, 1.5, 21])('rejects invalid maxCatalogTables %s', async (maxCatalogTables) => {
    const ctx = new Context()
    await ctx.plugin(SystemPrompt)
    await ctx.plugin(ToolRuntime)

    expect(() => { apply(ctx, pluginConfig({ maxCatalogTables })) }).toThrow(/maxCatalogTables/u)
  })

  it('searches, renders, and presents the reviewed schema catalog', async () => {
    const ctx = await mount()
    const tool = ctx.tools.get('search_business_schema')!
    const args = { query: 'course schedule', dataSource: 'main' }
    const result = await tool.execute(args, runContext)

    expect(dependencies.searchCatalog).toHaveBeenCalledWith(catalog, 'course schedule', 'main', 8)
    expect(result).toEqual(searchResult)
    expect(tool.isConcurrencySafe?.(args)).toBe(true)
    expect(tool.output.render(args, searchResult)).toEqual([{ type: 'text', text: JSON.stringify(searchResult) }])
    expect(tool.presentCall?.(args)).toMatchObject({ title: 'Search business schema', kind: 'search', rawInput: args })
  })

  it('executes a main query without inventing a missing member identity', async () => {
    const ctx = await mount(pluginConfig({ maxCatalogTables: 3 }))
    const tool = ctx.tools.get('query_business_data')!
    const args = {
      dataSource: 'main',
      root: { table: 'user_card', alias: 'card' },
      select: [{ tableAlias: 'card', column: 'card_name', outputName: 'cardName' }],
    }
    const result = await tool.execute(args, runContext)

    expect(dependencies.verifyDatabaseScope).toHaveBeenCalledWith(
      { host: 'main' }, 34, 12, 5_000, signal,
    )
    expect(dependencies.compileQuery).toHaveBeenCalledWith(catalog, args, expect.objectContaining({
      storeId: 12,
      tenantId: 56,
      operatorUid: 34,
    }))
    expect(dependencies.compileQuery.mock.calls[0]![2]).not.toHaveProperty('memberMobile')
    expect(dependencies.executeReadOnly).toHaveBeenCalledWith(
      { host: 'main' }, expect.objectContaining({ dataSource: 'main' }), 5_000, signal,
    )
    expect(result).toMatchObject({ dataSource: 'main', rowCount: 1, rows: [{ cardName: 'Morning Yoga' }] })
    expect(tool.output.render(args, result as never)).toEqual([{ type: 'text', text: JSON.stringify(result) }])
    expect(tool.presentCall?.(args)).toMatchObject({ title: 'Query business data', kind: 'search', rawInput: args })
  })

  it('routes a finance query and injects a present member identity', async () => {
    dependencies.compileQuery.mockReturnValue(compiledQuery({ dataSource: 'finance' }))
    const ctx = await mount(pluginConfig({ memberMobile: '13800138000' }))
    const tool = ctx.tools.get('query_business_data')!
    const args = {
      dataSource: 'finance',
      root: { table: 'ledger', alias: 'ledger' },
      select: [{ tableAlias: 'ledger', column: 'amount', outputName: 'amount' }],
    }

    await tool.execute(args, runContext)

    expect(dependencies.financeConnectionName).toHaveBeenCalledWith(expect.anything(), 56)
    expect(dependencies.compileQuery.mock.calls[0]![2]).toMatchObject({ memberMobile: '13800138000' })
    expect(dependencies.executeReadOnly).toHaveBeenCalledWith(
      { host: 'finance-56' }, expect.objectContaining({ dataSource: 'finance' }), 5_000, signal,
    )
  })

  it('treats an empty member identity as absent', async () => {
    const ctx = await mount(pluginConfig({ memberMobile: '' }))
    await ctx.tools.get('query_business_data')!.execute(queryArgs(), runContext)

    expect(dependencies.compileQuery.mock.calls[0]![2]).not.toHaveProperty('memberMobile')
  })

  it.each([
    [databaseConfig({ executionPolicy: { ...databaseConfig().executionPolicy, maxRows: 9 } }), compiledQuery({ limit: 10 }), []],
    [databaseConfig({ executionPolicy: { ...databaseConfig().executionPolicy, maxFields: 1 } }), compiledQuery({ outputNames: ['one', 'two'] }), []],
    [databaseConfig({ executionPolicy: { ...databaseConfig().executionPolicy, maxJoins: 0 } }), compiledQuery(), [{}]],
  ])('rejects a plan exceeding a product execution limit %#', async (database, compiled, joins) => {
    dependencies.loadDatabaseConfig.mockReturnValue(database)
    dependencies.compileQuery.mockReturnValue(compiled)
    const ctx = await mount()

    const validJoin = {
      table: 'users', alias: 'member', leftAlias: 'card', leftColumn: 'uid', rightAlias: 'member', rightColumn: 'id',
    }
    await expect(ctx.tools.get('query_business_data')!.execute(queryArgs({
      joins: joins.length === 0 ? [] : [validJoin],
    }), runContext)).rejects.toThrow(/execution policy/u)
    expect(dependencies.executeReadOnly).not.toHaveBeenCalled()
  })

  it('rejects an oversized serialized result', async () => {
    dependencies.executeReadOnly.mockResolvedValue([{ value: 'x'.repeat(12_000) }])
    const ctx = await mount()

    await expect(ctx.tools.get('query_business_data')!.execute(queryArgs(), runContext)).rejects.toThrow(/serialized-result limit/u)
  })
})
