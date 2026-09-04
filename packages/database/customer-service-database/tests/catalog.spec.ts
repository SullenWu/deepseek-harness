/** Reviewed database catalog parsing, validation, and search behavior. */

import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, describe, expect, it } from 'vitest'
import { loadCatalog, searchCatalog } from '../src/catalog.ts'
import type { CatalogRelation, CatalogTable, QueryCatalog } from '../src/types.ts'

const roots: string[] = []

afterEach(() => {
  for (const root of roots.splice(0)) rmSync(root, { recursive: true, force: true })
})

function table(overrides: Record<string, unknown> = {}): CatalogTable {
  return {
    policyVersion: 2,
    scopeVersion: 2,
    dataSource: 'main',
    table: 'user_card',
    domain: 'member',
    businessGroup: 'member-card',
    audience: 'merchant-customer-service',
    authority: 'primary-business-source',
    fieldPolicy: 'reviewed-business-fields',
    comment: 'member card',
    scopeColumns: ['store_id', 'tenant_id'],
    rowCountAggregates: ['count'],
    fields: [{
      name: 'card_name',
      dataType: 'varchar',
      comment: 'card name',
      usages: ['select', 'literal-filter', 'order'],
      aggregates: ['count', 'min', 'max'],
    }],
    ...overrides,
  }
}

function relation(overrides: Record<string, unknown> = {}): CatalogRelation {
  return {
    dataSource: 'main',
    leftTable: 'user_card',
    leftColumn: 'uid',
    rightTable: 'users',
    rightColumn: 'id',
    occurrences: 3,
    ...overrides,
  }
}

function files(tables: unknown[], relations: unknown[] = []): string {
  const root = mkdtempSync(join(tmpdir(), 'dsh-customer-catalog-'))
  roots.push(root)
  mkdirSync(root, { recursive: true })
  writeFileSync(join(root, 'database-agent-query-catalog.jsonl'), `\n${tables.map(value => JSON.stringify(value)).join('\n')}\n`)
  writeFileSync(join(root, 'database-agent-query-relations.jsonl'), `\n${relations.map(value => JSON.stringify(value)).join('\n')}\n`)
  return root
}

describe('loadCatalog', () => {
  it('loads valid table policies, both field-policy forms, and relations', () => {
    const users = table({ table: 'users', fieldPolicy: 'support-metadata-only' })
    const loaded = loadCatalog(files([table(), users], [relation()]))

    expect(loaded.tables).toHaveLength(2)
    expect(loaded.relations).toEqual([relation()])
  })

  it('rejects invalid JSONL and an empty table catalog', () => {
    const malformed = files([], [])
    writeFileSync(join(malformed, 'database-agent-query-catalog.jsonl'), '{')
    expect(() => loadCatalog(malformed)).toThrow(/invalid JSONL record 1/u)

    expect(() => loadCatalog(files([], []))).toThrow(/catalog is empty/u)
  })

  it.each([
    null,
    [],
  ])('rejects non-object table policy %j', (value) => {
    expect(() => loadCatalog(files([value]))).toThrow(/non-object table/u)
  })

  it.each([
    ['policyVersion', '2'],
    ['policyVersion', 1],
    ['scopeVersion', '2'],
    ['scopeVersion', 0],
    ['audience', 'public'],
    ['fieldPolicy', 'unreviewed'],
    ['dataSource', 1],
    ['dataSource', 'archive'],
    ['table', 1],
    ['table', 'bad-name'],
    ['domain', 1],
    ['businessGroup', 1],
    ['comment', 1],
    ['authority', 1],
    ['scopeColumns', 'store_id'],
    ['scopeColumns', [1]],
    ['scopeColumns', ['uid']],
    ['scopeColumns', []],
    ['rowCountAggregates', 'count'],
    ['rowCountAggregates', [1]],
    ['rowCountAggregates', ['sum']],
    ['fields', null],
  ])('rejects invalid table field %s=%j', (key, value) => {
    expect(() => loadCatalog(files([table({ [key]: value })]))).toThrow(/lacks a valid customer-service policy/u)
  })

  it.each([
    null,
    [],
    { name: 1, dataType: 'varchar', comment: '', usages: [], aggregates: [] },
    { name: 'bad-name', dataType: 'varchar', comment: '', usages: [], aggregates: [] },
    { name: 'name', dataType: 1, comment: '', usages: [], aggregates: [] },
    { name: 'name', dataType: 'bad-type', comment: '', usages: [], aggregates: [] },
    { name: 'name', dataType: 'varchar', comment: 1, usages: [], aggregates: [] },
    { name: 'name', dataType: 'varchar', comment: '', usages: 'select', aggregates: [] },
    { name: 'name', dataType: 'varchar', comment: '', usages: [1], aggregates: [] },
    { name: 'name', dataType: 'varchar', comment: '', usages: ['write'], aggregates: [] },
    { name: 'name', dataType: 'varchar', comment: '', usages: [], aggregates: 'count' },
    { name: 'name', dataType: 'varchar', comment: '', usages: [], aggregates: [1] },
    { name: 'name', dataType: 'varchar', comment: '', usages: [], aggregates: ['avg'] },
  ])('rejects invalid field policy %#', (field) => {
    expect(() => loadCatalog(files([table({ fields: [field] })]))).toThrow(/invalid or duplicate field policy/u)
  })

  it('rejects duplicate field and table policies case-insensitively', () => {
    const duplicateField = table({
      fields: [table().fields[0]!, { ...table().fields[0]!, name: 'CARD_NAME' }],
    })
    expect(() => loadCatalog(files([duplicateField]))).toThrow(/duplicate field policy/u)
    expect(() => loadCatalog(files([table(), table({ table: 'USER_CARD' })]))).toThrow(/duplicate table policy/u)
  })

  it.each([
    null,
    [],
    relation({ dataSource: 'archive' }),
    relation({ leftTable: 1 }),
    relation({ leftTable: 'bad-name' }),
    relation({ leftColumn: 1 }),
    relation({ leftColumn: 'bad-name' }),
    relation({ rightTable: 1 }),
    relation({ rightTable: 'bad-name' }),
    relation({ rightColumn: 1 }),
    relation({ rightColumn: 'bad-name' }),
    relation({ occurrences: '3' }),
    relation({ occurrences: 1.5 }),
    relation({ occurrences: 0 }),
    relation({ leftTable: 'missing' }),
    relation({ rightTable: 'missing' }),
  ])('rejects invalid relation policy %#', (value) => {
    const users = table({ table: 'users' })
    expect(() => loadCatalog(files([table(), users], [value]))).toThrow(/invalid relation policy/u)
  })

  it('accepts finance relation policies when both finance tables exist', () => {
    const left = table({ dataSource: 'finance', table: 'ledger' })
    const right = table({ dataSource: 'finance', table: 'ledger_item' })
    const value = relation({
      dataSource: 'finance',
      leftTable: 'ledger',
      rightTable: 'ledger_item',
    })

    expect(loadCatalog(files([left, right], [value])).relations).toEqual([value])
  })
})

describe('searchCatalog', () => {
  const userCard = table({
    table: 'user_card',
    comment: 'membership',
    fields: [
      ...table().fields,
      { name: 'balance', dataType: 'decimal', comment: 'remaining value', usages: ['select'], aggregates: ['sum'] },
    ],
  })
  const users = table({ table: 'users', comment: 'membership', fields: table().fields })
  const ledger = table({ dataSource: 'finance', table: 'ledger', domain: 'payment', comment: 'payment record' })
  const catalog: QueryCatalog = {
    tables: [users, userCard, ledger],
    relations: [relation()],
  }

  it('requires a term and validates an optional source', () => {
    expect(() => searchCatalog(catalog, '   ', undefined, 3)).toThrow(/at least one/u)
    expect(() => searchCatalog(catalog, 'member', 'archive', 3)).toThrow(/main or finance/u)
  })

  it('ranks table and field matches, returns selected relations, and reports truncation', () => {
    const result = searchCatalog(catalog, 'membership balance', '', 1)

    expect(result.matches).toHaveLength(1)
    expect(result.matches[0]?.table).toBe('user_card')
    expect(result.matches[0]?.fields.map(field => field.name)).toEqual(['balance'])
    expect(result.totalMatches).toBe(2)
    expect(result.truncated).toBe(true)
    expect(result.relations).toEqual([])
  })

  it('uses all fields for a table-only match and sorts equal scores by table name', () => {
    const result = searchCatalog(catalog, 'membership', undefined, 5)

    expect(result.matches.map(match => match.table)).toEqual(['user_card', 'users'])
    expect(result.matches[0]?.fields).toHaveLength(2)
    expect(result.relations).toEqual([relation()])
    expect(result.truncated).toBe(false)
  })

  it('filters the requested source and accepts normalized source text', () => {
    expect(searchCatalog(catalog, 'payment', ' FINANCE ', 5).matches.map(match => match.table)).toEqual(['ledger'])
    expect(searchCatalog(catalog, 'missing', 'main', 5)).toEqual({
      matches: [], relations: [], totalMatches: 0, truncated: false,
    })
  })
})
