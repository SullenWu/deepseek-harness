/**
 * Request-local customer-service database Provider and model-facing Consumer.
 * The model discovers the reviewed schema and authors a structured plan; this
 * plugin owns live scope validation, SQL compilation, and read-only execution.
 * @module @deepseek-ai/dsh-customer-service-database
 */

import type { Context } from '@deepseek-ai/cordis'
import z from '@deepseek-ai/schemastery'
import { defineTool } from '@deepseek-ai/dsh-tools'
import { catalogDirectory, connectionOptions, financeConnectionName, loadDatabaseConfig } from './config.ts'
import { loadCatalog, searchCatalog } from './catalog.ts'
import { compileQuery } from './compiler.ts'
import { executeReadOnly, verifyDatabaseScope } from './mysql.ts'

export const name = 'customer-service-database'
export const inject = ['tools']

/** Server-owned request configuration for the database tool pair. */
export interface Config {
  /** Absolute root containing the product skill directories. */
  skillRoot: string
  /** Trusted transport product code. */
  productCode: string
  /** Trusted current store id. */
  storeId: number
  /** Trusted current operator uid. */
  operatorUid: number
  /** Whether DuckAI already verified the merchant entry profile. */
  merchantProfileVerified: boolean
  /** Member mobile extracted from the current customer message, when available. */
  memberMobile?: string
  /** Maximum tables returned by one schema search. */
  maxCatalogTables?: number
}

/** Runtime configuration schema for the request-local database plugin. */
export const Config: z<Config> = z.object({
  skillRoot: z.string().required(),
  productCode: z.string().required(),
  storeId: z.number().required(),
  operatorUid: z.number().required(),
  merchantProfileVerified: z.boolean().required(),
  memberMobile: z.string(),
  maxCatalogTables: z.number().default(8),
})

const FIELD_OUTPUT = {
  type: 'object',
  additionalProperties: false,
  properties: {
    name: { type: 'string', required: true },
    dataType: { type: 'string', required: true },
    comment: { type: 'string', required: true },
    usages: { type: 'array', required: true, items: { type: 'string' } },
    aggregates: { type: 'array', required: true, items: { type: 'string' } },
  },
} as const

const RELATION_OUTPUT = {
  type: 'object',
  additionalProperties: false,
  properties: {
    dataSource: { type: 'string', required: true },
    leftTable: { type: 'string', required: true },
    leftColumn: { type: 'string', required: true },
    rightTable: { type: 'string', required: true },
    rightColumn: { type: 'string', required: true },
    occurrences: { type: 'integer', required: true },
  },
} as const

const TABLE_REF_INPUT = {
  type: 'object',
  required: true,
  additionalProperties: false,
  properties: {
    table: { type: 'string', required: true, description: 'Table name returned by search_business_schema.' },
    alias: { type: 'string', required: true, description: 'Query-local SQL-safe alias.' },
  },
} as const

const SELECT_INPUT = {
  type: 'object',
  additionalProperties: false,
  properties: {
    tableAlias: { type: 'string', required: true },
    column: { type: 'string', required: true, description: 'Catalog field, or * for an authorized count.' },
    outputName: { type: 'string', required: true, description: 'SQL-safe business result key.' },
    aggregate: { type: 'string', enum: ['count', 'sum', 'min', 'max'] },
  },
} as const

const JOIN_INPUT = {
  type: 'object',
  additionalProperties: false,
  properties: {
    type: { type: 'string', enum: ['inner', 'left'] },
    table: { type: 'string', required: true },
    alias: { type: 'string', required: true },
    leftAlias: { type: 'string', required: true },
    leftColumn: { type: 'string', required: true },
    rightAlias: { type: 'string', required: true },
    rightColumn: { type: 'string', required: true },
  },
} as const

const FILTER_INPUT = {
  type: 'object',
  additionalProperties: false,
  properties: {
    tableAlias: { type: 'string', required: true },
    column: { type: 'string', required: true },
    operator: {
      type: 'string',
      required: true,
      enum: ['eq', 'neq', 'gt', 'gte', 'lt', 'lte', 'contains', 'prefix', 'in', 'is-null', 'is-not-null'],
    },
    valueSource: {
      type: 'string',
      enum: ['literal', 'member-mobile', 'operator-uid', 'unclaimed-member', 'store-today', 'store-now'],
    },
    value: { type: 'string', description: 'Only for a single literal value.' },
    values: { type: 'array', items: { type: 'string' }, description: 'Only for in + literal.' },
  },
} as const

const ORDER_INPUT = {
  type: 'object',
  additionalProperties: false,
  properties: {
    tableAlias: { type: 'string', required: true },
    column: { type: 'string', required: true },
    direction: { type: 'string', required: true, enum: ['asc', 'desc'] },
  },
} as const

/**
 * Mount schema discovery and structured query tools for one trusted request.
 * @param ctx - Cordis context carrying the tool registry.
 * @param config - Server-owned product and identity scope.
 */
export function apply(ctx: Context, config: Config): void {
  if (!config.merchantProfileVerified
    || !Number.isSafeInteger(config.storeId)
    || config.storeId < 1
    || !Number.isSafeInteger(config.operatorUid)
    || config.operatorUid < 1) {
    throw new Error('customer-service-database: a verified merchant store and operator are required')
  }
  const maxCatalogTables = config.maxCatalogTables ?? 8
  if (!Number.isSafeInteger(maxCatalogTables) || maxCatalogTables < 1 || maxCatalogTables > 20) {
    throw new Error('customer-service-database: maxCatalogTables must be an integer from 1 to 20')
  }
  const database = loadDatabaseConfig(config.skillRoot, config.productCode)
  const catalog = loadCatalog(catalogDirectory(config.skillRoot))
  const timeoutMs = database.executionPolicy.commandTimeoutSeconds * 1_000

  ctx.tools.register(defineTool({
    name: 'search_business_schema',
    description: 'Search the reviewed customer-service database catalog before composing a query. This returns schema policy, not live customer facts. Choose search terms from the unresolved business question; no fixed question-to-table routing is applied.',
    parameters: {
      query: { type: 'string', required: true, description: 'Whitespace-separated business, table, or field terms.' },
      dataSource: { type: 'string', enum: ['main', 'finance'], description: 'Optional logical source filter.' },
    },
    output: {
      schema: {
        type: 'object',
        additionalProperties: false,
        properties: {
          matches: {
            type: 'array',
            required: true,
            items: {
              type: 'object',
              additionalProperties: false,
              properties: {
                dataSource: { type: 'string', required: true },
                table: { type: 'string', required: true },
                domain: { type: 'string', required: true },
                businessGroup: { type: 'string', required: true },
                comment: { type: 'string', required: true },
                scopeColumns: { type: 'array', required: true, items: { type: 'string' } },
                fields: { type: 'array', required: true, items: FIELD_OUTPUT },
              },
            },
          },
          relations: { type: 'array', required: true, items: RELATION_OUTPUT },
          totalMatches: { type: 'integer', required: true },
          truncated: { type: 'boolean', required: true },
        },
      },
      render: (_args, value) => [{ type: 'text', text: JSON.stringify(value) }],
    },
    isConcurrencySafe: () => true,
    execute(args) {
      return Promise.resolve(searchCatalog(catalog, args.query, args.dataSource, maxCatalogTables))
    },
    presentCall: args => ({ card: 'generic', title: 'Search business schema', kind: 'search', rawInput: args }),
  }))

  ctx.tools.register(defineTool({
    name: 'query_business_data',
    description: 'Execute one structured, parameterized, read-only SELECT using only tables, fields, usages, and joins returned by search_business_schema. Never submit SQL, database names, StoreId, TenantId, UID, a phone number, or another identity value; server-owned scope and supported value sources are injected after live authorization.',
    parameters: {
      dataSource: { type: 'string', required: true, enum: ['main', 'finance'] },
      root: TABLE_REF_INPUT,
      select: { type: 'array', required: true, items: SELECT_INPUT },
      joins: { type: 'array', items: JOIN_INPUT },
      filters: { type: 'array', items: FILTER_INPUT },
      orderBy: { type: 'array', items: ORDER_INPUT },
      limit: { type: 'integer' },
      distinct: { type: 'boolean' },
    },
    output: {
      schema: {
        type: 'object',
        additionalProperties: false,
        properties: {
          dataSource: { type: 'string', required: true },
          rowCount: { type: 'integer', required: true },
          rows: { type: 'array', required: true, items: { type: 'json' } },
          evidenceBoundary: { type: 'string', required: true },
        },
      },
      render: (_args, value) => [{ type: 'text', text: JSON.stringify(value) }],
    },
    async execute(args, exec) {
      const verified = await verifyDatabaseScope(
        connectionOptions(database, database.mainConnectionName),
        config.operatorUid,
        config.storeId,
        timeoutMs,
        exec.signal,
      )
      const storeNow = new Date(Date.now() + verified.utcOffsetHours * 60 * 60_000)
      const compiled = compileQuery(catalog, args, {
        storeId: verified.storeId,
        tenantId: verified.tenantId,
        operatorUid: verified.operatorUid,
        ...(config.memberMobile === undefined || config.memberMobile === '' ? {} : { memberMobile: config.memberMobile }),
        storeNow,
      })
      if (compiled.limit > database.executionPolicy.maxRows
        || compiled.outputNames.length > database.executionPolicy.maxFields
        || (args.joins?.length ?? 0) > database.executionPolicy.maxJoins) {
        throw new Error('query plan exceeds the product skill execution policy')
      }
      const connectionName = compiled.dataSource === 'finance'
        ? financeConnectionName(database, verified.tenantId)
        : database.mainConnectionName
      ctx.logger.info(
        'customer-service-database: compiled product=%s source=%s fields=%d sql=%s',
        database.productCode,
        compiled.dataSource,
        compiled.outputNames.length,
        compiled.sql,
      )
      const rows = await executeReadOnly(connectionOptions(database, connectionName), compiled, timeoutMs, exec.signal)
      const result = {
        dataSource: compiled.dataSource,
        rowCount: rows.length,
        rows,
        evidenceBoundary: 'Results come from one current read-only query inside the live verified product, store, and tenant scope. They do not prove that a write or business submission succeeded.',
      }
      if (JSON.stringify(result).length > database.executionPolicy.maxSerializedCharacters) {
        throw new Error('query result exceeds the product skill serialized-result limit; reduce fields or filters')
      }
      return result
    },
    presentCall: args => ({ card: 'generic', title: 'Query business data', kind: 'search', rawInput: args }),
  }))
}

export type { CompiledQuery, DynamicQueryPlan, QueryCatalog, QueryScope } from './types.ts'
export { compileQuery } from './compiler.ts'
export { loadCatalog, searchCatalog } from './catalog.ts'
