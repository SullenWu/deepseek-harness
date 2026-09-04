/** Load and search the reviewed customer-service query catalog. */

import { readFileSync } from 'node:fs'
import { join } from 'node:path'
import type { CatalogRelation, CatalogTable, QueryCatalog } from './types.ts'

const IDENTIFIER = /^[A-Za-z_][A-Za-z0-9_]{0,63}$/u
const FIELD_USAGES = new Set([
  'select', 'literal-filter', 'order', 'member-mobile-filter', 'operator-uid-filter', 'unclaimed-member-filter',
])
const AGGREGATES = new Set(['count', 'sum', 'min', 'max'])

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function isStringArray(value: unknown, allowed: ReadonlySet<string>): value is string[] {
  return Array.isArray(value) && value.every(item => typeof item === 'string' && allowed.has(item))
}

function readJsonLines<T>(path: string): T[] {
  return readFileSync(path, 'utf8')
    .split(/\r?\n/u)
    .filter(line => line.trim().length > 0)
    .map((line, index) => {
      try {
        return JSON.parse(line) as T
      } catch (error) {
        throw new Error(`customer-service-database: invalid JSONL record ${index + 1} in ${path}`, { cause: error })
      }
    })
}

function assertCatalogTable(value: unknown): asserts value is CatalogTable {
  if (!isRecord(value)) throw new Error('customer-service-database: query catalog contains a non-object table')
  const fieldPolicy = value.fieldPolicy
  if (typeof value.policyVersion !== 'number'
    || value.policyVersion < 2
    || typeof value.scopeVersion !== 'number'
    || value.scopeVersion < 1
    || value.audience !== 'merchant-customer-service'
    || (fieldPolicy !== 'reviewed-business-fields' && fieldPolicy !== 'support-metadata-only')
    || typeof value.dataSource !== 'string'
    || !['main', 'finance'].includes(value.dataSource)
    || typeof value.table !== 'string'
    || !IDENTIFIER.test(value.table)
    || typeof value.domain !== 'string'
    || typeof value.businessGroup !== 'string'
    || typeof value.comment !== 'string'
    || typeof value.authority !== 'string'
    || !isStringArray(value.scopeColumns, new Set(['store_id', 'tenant_id']))
    || value.scopeColumns.length === 0
    || !isStringArray(value.rowCountAggregates, new Set(['count']))
    || !Array.isArray(value.fields)) {
    throw new Error(`customer-service-database: table ${JSON.stringify(value.table)} lacks a valid customer-service policy`)
  }
  const fields = new Set<string>()
  for (const field of value.fields) {
    if (!isRecord(field)
      || typeof field.name !== 'string'
      || !IDENTIFIER.test(field.name)
      || typeof field.dataType !== 'string'
      || !IDENTIFIER.test(field.dataType)
      || typeof field.comment !== 'string'
      || !isStringArray(field.usages, FIELD_USAGES)
      || !isStringArray(field.aggregates, AGGREGATES)
      || fields.has(field.name.toLocaleLowerCase())) {
      throw new Error(`customer-service-database: table ${value.table} contains an invalid or duplicate field policy`)
    }
    fields.add(field.name.toLocaleLowerCase())
  }
}

function assertCatalogRelation(value: unknown, tables: ReadonlySet<string>): asserts value is CatalogRelation {
  if (!isRecord(value)
    || (value.dataSource !== 'main' && value.dataSource !== 'finance')
    || typeof value.leftTable !== 'string'
    || !IDENTIFIER.test(value.leftTable)
    || typeof value.leftColumn !== 'string'
    || !IDENTIFIER.test(value.leftColumn)
    || typeof value.rightTable !== 'string'
    || !IDENTIFIER.test(value.rightTable)
    || typeof value.rightColumn !== 'string'
    || !IDENTIFIER.test(value.rightColumn)
    || typeof value.occurrences !== 'number'
    || !Number.isSafeInteger(value.occurrences)
    || value.occurrences < 1
    || !tables.has(`${value.dataSource}:${value.leftTable.toLocaleLowerCase()}`)
    || !tables.has(`${value.dataSource}:${value.rightTable.toLocaleLowerCase()}`)) {
    throw new Error('customer-service-database: query catalog contains an invalid relation policy')
  }
}

/**
 * Load the two reviewed JSONL policy files from a fixed directory.
 * @param directory - Server-owned catalog directory.
 * @returns Validated catalog records.
 */
export function loadCatalog(directory: string): QueryCatalog {
  const tableRecords = readJsonLines<unknown>(join(directory, 'database-agent-query-catalog.jsonl'))
  const relationRecords = readJsonLines<unknown>(join(directory, 'database-agent-query-relations.jsonl'))
  if (tableRecords.length === 0) throw new Error('customer-service-database: query catalog is empty')
  const tables: CatalogTable[] = []
  for (const table of tableRecords) {
    assertCatalogTable(table)
    tables.push(table)
  }
  const tableNames = new Set<string>()
  for (const table of tables) {
    const key = `${table.dataSource}:${table.table.toLocaleLowerCase()}`
    if (tableNames.has(key)) throw new Error('customer-service-database: query catalog contains a duplicate table policy')
    tableNames.add(key)
  }
  const relations: CatalogRelation[] = []
  for (const relation of relationRecords) {
    assertCatalogRelation(relation, tableNames)
    relations.push(relation)
  }
  return { tables, relations }
}

/** Catalog search result projected to the model. */
export interface CatalogSearchResult {
  /** Matching allowlisted table projections. */
  matches: Array<{
    dataSource: string
    table: string
    domain: string
    businessGroup: string
    comment: string
    scopeColumns: string[]
    fields: Array<{ name: string; dataType: string; comment: string; usages: string[]; aggregates: string[] }>
  }>
  /** Relations whose two endpoints are both present in `matches`. */
  relations: CatalogRelation[]
  /** Number of matching tables before the configured cap. */
  totalMatches: number
  /** Whether additional matching tables were omitted. */
  truncated: boolean
}

/**
 * Search table and field semantics without mapping customer phrases to fixed APIs.
 * @param catalog - Loaded reviewed catalog.
 * @param query - Model-chosen whitespace-separated terms.
 * @param dataSource - Optional logical source filter.
 * @param limit - Maximum returned tables.
 * @returns Ranked table/field subset and relations within that subset.
 */
export function searchCatalog(
  catalog: QueryCatalog,
  query: string,
  dataSource: string | undefined,
  limit: number,
): CatalogSearchResult {
  const terms = query.trim().toLocaleLowerCase().split(/\s+/u).filter(Boolean)
  if (terms.length === 0) throw new Error('query must contain at least one search term')
  const source = dataSource?.trim().toLocaleLowerCase()
  if (source !== undefined && source !== '' && source !== 'main' && source !== 'finance') {
    throw new Error('dataSource must be main or finance when provided')
  }
  const scored = catalog.tables
    .filter(table => source === undefined || source === '' || table.dataSource === source)
    .map((table) => {
      const tableText = [table.table, table.domain, table.businessGroup, table.comment].join(' ').toLocaleLowerCase()
      const matchingFields = table.fields.filter((field) => {
        const fieldText = [field.name, field.comment, field.dataType].join(' ').toLocaleLowerCase()
        return terms.some(term => fieldText.includes(term))
      })
      const score = terms.reduce((sum, term) => sum + (tableText.includes(term) ? 20 : 0), 0) + matchingFields.length
      return { table, matchingFields, score }
    })
    .filter(item => item.score > 0)
    .sort((left, right) => right.score - left.score || left.table.table.localeCompare(right.table.table))
  const selected = scored.slice(0, limit)
  const tableNames = new Set(selected.map(item => item.table.table.toLocaleLowerCase()))
  return {
    matches: selected.map(({ table, matchingFields }) => ({
      dataSource: table.dataSource,
      table: table.table,
      domain: table.domain,
      businessGroup: table.businessGroup,
      comment: table.comment,
      scopeColumns: [...table.scopeColumns],
      fields: (matchingFields.length > 0 ? matchingFields : table.fields).map(field => ({
        name: field.name,
        dataType: field.dataType,
        comment: field.comment,
        usages: [...field.usages],
        aggregates: [...field.aggregates],
      })),
    })),
    relations: catalog.relations.filter(relation =>
      tableNames.has(relation.leftTable.toLocaleLowerCase())
      && tableNames.has(relation.rightTable.toLocaleLowerCase())),
    totalMatches: scored.length,
    truncated: scored.length > selected.length,
  }
}
