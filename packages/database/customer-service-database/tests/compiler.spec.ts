/** Catalog-constrained SQL compiler behavior. */

import { describe, expect, it } from 'vitest'
import { compileQuery } from '../src/compiler.ts'
import type { DynamicQueryPlan, QueryCatalog, QueryScope } from '../src/types.ts'

const catalog: QueryCatalog = {
  tables: [
    {
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
      fields: [
        { name: 'card_name', dataType: 'varchar', comment: 'name', usages: ['select', 'literal-filter', 'order'], aggregates: ['count', 'min', 'max'] },
        { name: 'uid', dataType: 'int', comment: 'member', usages: ['select'], aggregates: [] },
        { name: 'amount', dataType: 'decimal', comment: 'amount', usages: ['select', 'literal-filter', 'order'], aggregates: ['count', 'sum', 'min', 'max'] },
        { name: 'created_at', dataType: 'datetime', comment: 'created', usages: ['select', 'literal-filter', 'order'], aggregates: ['min', 'max'] },
        { name: 'starts_at', dataType: 'time', comment: 'time', usages: ['literal-filter'], aggregates: [] },
        { name: 'mobile', dataType: 'varchar', comment: 'mobile', usages: ['member-mobile-filter'], aggregates: [] },
        { name: 'operator_uid', dataType: 'int', comment: 'operator', usages: ['operator-uid-filter'], aggregates: [] },
        { name: 'claimed_uid', dataType: 'int', comment: 'claimed', usages: ['unclaimed-member-filter'], aggregates: [] },
      ],
    },
    {
      policyVersion: 2,
      scopeVersion: 2,
      dataSource: 'main',
      table: 'users',
      domain: 'member',
      businessGroup: 'member-card',
      audience: 'merchant-customer-service',
      authority: 'primary-business-source',
      fieldPolicy: 'reviewed-business-fields',
      comment: 'member',
      scopeColumns: ['tenant_id'],
      rowCountAggregates: ['count'],
      fields: [
        { name: 'id', dataType: 'int', comment: 'id', usages: [], aggregates: [] },
        { name: 'user_name', dataType: 'varchar', comment: 'name', usages: ['select', 'literal-filter'], aggregates: ['count'] },
      ],
    },
  ],
  relations: [
    {
      dataSource: 'main',
      leftTable: 'user_card',
      leftColumn: 'uid',
      rightTable: 'users',
      rightColumn: 'id',
      occurrences: 8,
    },
  ],
}

const scope: QueryScope = {
  storeId: 12,
  tenantId: 34,
  operatorUid: 56,
  memberMobile: '13800138000',
  storeNow: new Date('2026-09-04T12:34:56Z'),
}

function plan(overrides: Partial<DynamicQueryPlan> = {}): DynamicQueryPlan {
  return {
    dataSource: 'main',
    root: { table: 'user_card', alias: 'card' },
    select: [{ tableAlias: 'card', column: 'card_name', outputName: 'cardName' }],
    ...overrides,
  }
}

function compile(overrides: Partial<DynamicQueryPlan> = {}, queryScope = scope, queryCatalog = catalog) {
  return compileQuery(queryCatalog, plan(overrides), queryScope)
}

describe('compileQuery', () => {
  it('injects store and tenant scope into every table alias', () => {
    const compiled = compileQuery(catalog, {
      dataSource: 'main',
      root: { table: 'user_card', alias: 'card' },
      select: [
        { tableAlias: 'card', column: 'card_name', outputName: 'cardName' },
        { tableAlias: 'member', column: 'user_name', outputName: 'memberName' },
      ],
      joins: [{
        type: 'inner',
        table: 'users',
        alias: 'member',
        leftAlias: 'card',
        leftColumn: 'uid',
        rightAlias: 'member',
        rightColumn: 'id',
      }],
      filters: [{
        tableAlias: 'card',
        column: 'card_name',
        operator: 'contains',
        valueSource: 'literal',
        value: '瑜伽',
      }],
      limit: 5,
    }, {
      storeId: 12,
      tenantId: 34,
      operatorUid: 56,
      storeNow: new Date('2026-09-04T12:00:00Z'),
    })

    expect(compiled.sql).toContain('`card`.`store_id` = ?')
    expect(compiled.sql).toContain('`card`.`tenant_id` = ?')
    expect(compiled.sql).toContain('`member`.`tenant_id` = ?')
    expect(compiled.sql).toContain('`card`.`card_name` LIKE ?')
    expect(compiled.parameters).toEqual([12, 34, 34, '%瑜伽%'])
    expect(compiled.sql).toMatch(/^SELECT /u)
    expect(compiled.sql).not.toContain('瑜伽')
  })

  it('rejects fields and joins not authorized by the catalog', () => {
    expect(() => compileQuery(catalog, {
      dataSource: 'main',
      root: { table: 'user_card', alias: 'card' },
      select: [{ tableAlias: 'card', column: 'password', outputName: 'secret' }],
    }, {
      storeId: 12,
      tenantId: 34,
      operatorUid: 56,
      storeNow: new Date('2026-09-04T12:00:00Z'),
    })).toThrow(/catalog rejects/u)
  })

  it('binds member identity only through the server-owned value source', () => {
    const mobileCatalog: QueryCatalog = {
      tables: [{
        ...catalog.tables[1]!,
        fields: [{
          name: 'user_mobile',
          dataType: 'varchar',
          comment: 'member mobile',
          usages: ['member-mobile-filter'],
          aggregates: [],
        }],
      }],
      relations: [],
    }
    const compiled = compileQuery(mobileCatalog, {
      dataSource: 'main',
      root: { table: 'users', alias: 'member' },
      select: [{ tableAlias: 'member', column: '*', outputName: 'matches', aggregate: 'count' }],
      filters: [{
        tableAlias: 'member',
        column: 'user_mobile',
        operator: 'eq',
        valueSource: 'member-mobile',
      }],
    }, {
      storeId: 12,
      tenantId: 34,
      operatorUid: 56,
      memberMobile: '13800138000',
      storeNow: new Date('2026-09-04T12:00:00Z'),
    })

    expect(compiled.parameters).toEqual([34, '13800138000'])
    expect(compiled.sql).not.toContain('13800138000')
  })

  it('rejects missing catalog, scope, source, table, and identifier inputs', () => {
    expect(() => compile({}, scope, { tables: [], relations: [] })).toThrow(/catalog is empty/u)
    expect(() => compile({}, { ...scope, storeId: 0 })).toThrow(/scope is missing/u)
    expect(() => compile({}, { ...scope, tenantId: 0 })).toThrow(/scope is missing/u)
    expect(() => compile({}, { ...scope, operatorUid: 0 })).toThrow(/scope is missing/u)
    expect(() => compile({ dataSource: 'archive' })).toThrow(/dataSource must be main or finance/u)
    expect(() => compile({ dataSource: 'finance' })).toThrow(/table is not present/u)
    expect(() => compile({ root: { table: 'missing', alias: 'card' } })).toThrow(/table is not present/u)
    expect(() => compile({ root: { table: 'bad-name', alias: 'card' } })).toThrow(/table name has an invalid/u)
    expect(() => compile({ root: { table: 'user_card', alias: '' } })).toThrow(/root alias/u)
    expect(() => compile({ root: { table: 'user_card', alias: 'bad-name' } })).toThrow(/root alias/u)
  })

  it('compiles normalized finance source with a distinct default-limit projection', () => {
    const financeCatalog: QueryCatalog = {
      tables: [{ ...catalog.tables[0]!, dataSource: 'finance', table: 'ledger' }],
      relations: [],
    }
    const compiled = compileQuery(financeCatalog, plan({
      dataSource: ' FINANCE ',
      root: { table: 'ledger', alias: 'ledger' },
      select: [{ tableAlias: 'ledger', column: 'card_name', outputName: 'name' }],
      distinct: true,
      limit: 0,
    }), scope)

    expect(compiled.dataSource).toBe('finance')
    expect(compiled.limit).toBe(10)
    expect(compiled.sql).toMatch(/^SELECT DISTINCT/u)
  })

  it('rejects join-count, identifiers, aliases, table, relationship, and type violations', () => {
    const validJoin = {
      type: 'inner',
      table: 'users',
      alias: 'member',
      leftAlias: 'card',
      leftColumn: 'uid',
      rightAlias: 'member',
      rightColumn: 'id',
    }
    expect(() => compile({ joins: Array.from({ length: 5 }, () => validJoin) })).toThrow(/at most four joins/u)
    expect(() => compile({ joins: [{ ...validJoin, alias: 'bad-name', rightAlias: 'bad-name' }] })).toThrow(/join alias/u)
    expect(() => compile({ joins: [{ ...validJoin, leftAlias: 'bad-name' }] })).toThrow(/left join alias/u)
    expect(() => compile({ joins: [{ ...validJoin, rightAlias: 'bad-name' }] })).toThrow(/right join alias/u)
    expect(() => compile({ joins: [{ ...validJoin, rightAlias: 'other' }] })).toThrow(/rightAlias/u)
    expect(() => compile({ joins: [{ ...validJoin, alias: 'card', rightAlias: 'card' }] })).toThrow(/duplicate/u)
    expect(() => compile({ joins: [{ ...validJoin, leftAlias: 'missing' }] })).toThrow(/leftAlias/u)
    expect(() => compile({ joins: [{ ...validJoin, table: 'missing' }] })).toThrow(/table is not present/u)
    expect(() => compile({ joins: [{ ...validJoin, leftColumn: 'bad-name' }] })).toThrow(/left join column/u)
    expect(() => compile({ joins: [{ ...validJoin, rightColumn: 'bad-name' }] })).toThrow(/right join column/u)
    expect(() => compile({ joins: [{ ...validJoin, leftColumn: 'missing' }] })).toThrow(/relationship is not present/u)
    expect(() => compile({ joins: [{ ...validJoin, type: 'outer' }] })).toThrow(/join type/u)
  })

  it('accepts default, left, and reverse catalog joins', () => {
    const reverseCatalog: QueryCatalog = {
      ...catalog,
      relations: [{
        ...catalog.relations[0]!,
        leftTable: 'users',
        leftColumn: 'id',
        rightTable: 'user_card',
        rightColumn: 'uid',
      }],
    }
    const join = {
      table: 'users', alias: 'member', leftAlias: 'card', leftColumn: 'uid', rightAlias: 'member', rightColumn: 'id',
    }
    expect(compile({ joins: [join] }).sql).toContain('INNER JOIN')
    expect(compile({ joins: [{ ...join, type: 'left' }] }).sql).toContain('LEFT JOIN')
    expect(compile({}, scope, reverseCatalog)).toBeDefined()
    expect(compile({ joins: [join] }, scope, reverseCatalog).sql).toContain('JOIN `users`')
  })

  it('exercises every relationship mismatch before rejecting a join', () => {
    const join = {
      table: 'users', alias: 'member', leftAlias: 'card', leftColumn: 'uid', rightAlias: 'member', rightColumn: 'id',
    }
    const mismatches = [
      { dataSource: 'finance' },
      { leftTable: 'other' },
      { leftColumn: 'other' },
      { rightTable: 'other' },
      { rightColumn: 'other' },
      { leftTable: 'other', rightTable: 'other' },
      { leftTable: 'users', leftColumn: 'other', rightTable: 'user_card', rightColumn: 'uid' },
      { leftTable: 'users', leftColumn: 'id', rightTable: 'other', rightColumn: 'uid' },
      { leftTable: 'users', leftColumn: 'id', rightTable: 'user_card', rightColumn: 'other' },
    ]
    for (const mismatch of mismatches) {
      const queryCatalog = { ...catalog, relations: [{ ...catalog.relations[0]!, ...mismatch }] }
      expect(() => compile({ joins: [join] }, scope, queryCatalog)).toThrow(/relationship/u)
    }
  })

  it('validates selection count, aliases, outputs, fields, and aggregates', () => {
    expect(() => compile({ select: [] })).toThrow(/select must contain/u)
    expect(() => compile({ select: Array.from({ length: 17 }, () => plan().select[0]!) })).toThrow(/select must contain/u)
    expect(() => compile({ select: [{ tableAlias: 'missing', column: 'card_name', outputName: 'name' }] })).toThrow(/unknown table alias/u)
    expect(() => compile({ select: [{ tableAlias: 'bad-name', column: 'card_name', outputName: 'name' }] })).toThrow(/table alias/u)
    expect(() => compile({ select: [{ tableAlias: 'card', column: 'card_name', outputName: 'bad-name' }] })).toThrow(/output name/u)
    expect(() => compile({ select: [
      { tableAlias: 'card', column: 'card_name', outputName: 'Name' },
      { tableAlias: 'card', column: 'card_name', outputName: 'name' },
    ] })).toThrow(/output names must be unique/u)
    expect(() => compile({ select: [{ tableAlias: 'card', column: 'uid', outputName: 'uid', aggregate: 'count' }] })).toThrow(/catalog rejects count/u)
    const invalidSumCatalog: QueryCatalog = {
      ...catalog,
      tables: [{
        ...catalog.tables[0]!,
        fields: catalog.tables[0]!.fields.map(field => field.name === 'card_name'
          ? { ...field, aggregates: [...field.aggregates, 'sum'] }
          : field),
      }, catalog.tables[1]!],
    }
    expect(() => compile({ select: [{ tableAlias: 'card', column: 'card_name', outputName: 'name', aggregate: 'sum' }] }, scope, invalidSumCatalog)).toThrow(/sum requires a numeric/u)
    expect(() => compile({ select: [{ tableAlias: 'card', column: 'amount', outputName: 'amount', aggregate: 'average' }] })).toThrow(/aggregate must be/u)
    const noCount = { ...catalog, tables: [{ ...catalog.tables[0]!, rowCountAggregates: [] }, catalog.tables[1]!] }
    expect(() => compile({ select: [{ tableAlias: 'card', column: '*', outputName: 'count', aggregate: 'count' }] }, scope, noCount)).toThrow(/rejects count/u)
  })

  it.each(['count', 'sum', 'min', 'max'])('compiles the %s aggregate', (aggregate) => {
    const compiled = compile({
      select: [{ tableAlias: 'card', column: 'amount', outputName: 'value', aggregate }],
    })
    expect(compiled.sql).toContain(`${aggregate.toLocaleUpperCase()}(`)
  })

  it('groups non-aggregate selections mixed with aggregates and de-duplicates group fields', () => {
    const compiled = compile({
      select: [
        { tableAlias: 'card', column: 'card_name', outputName: 'firstName' },
        { tableAlias: 'card', column: 'card_name', outputName: 'secondName' },
        { tableAlias: 'card', column: 'amount', outputName: 'total', aggregate: 'sum' },
      ],
      distinct: true,
    })

    expect(compiled.sql).toContain('GROUP BY `card`.`card_name`')
    expect(compiled.sql).not.toContain('DISTINCT')
  })

  it('requires each table to declare store or tenant scope', () => {
    const noScope = { ...catalog, tables: [{ ...catalog.tables[0]!, scopeColumns: [] }, catalog.tables[1]!] }
    expect(() => compile({}, scope, noScope)).toThrow(/has no scope column/u)
  })

  it('supports a store-only table scope', () => {
    const storeOnly = {
      ...catalog,
      tables: [{ ...catalog.tables[0]!, scopeColumns: ['store_id'] }, catalog.tables[1]!],
    }
    const compiled = compile({}, scope, storeOnly)

    expect(compiled.parameters).toEqual([12])
    expect(compiled.sql).not.toContain('tenant_id')
  })

  it('validates filter count, aliases, fields, and value-source contracts', () => {
    const literal = { tableAlias: 'card', column: 'card_name', operator: 'eq', valueSource: 'literal', value: 'name' }
    expect(() => compile({ filters: Array.from({ length: 17 }, () => literal) })).toThrow(/sixteen filters/u)
    expect(() => compile({ filters: [{ ...literal, tableAlias: 'bad-name' }] })).toThrow(/filter table alias/u)
    expect(() => compile({ filters: [{ ...literal, tableAlias: 'missing' }] })).toThrow(/unknown table alias/u)
    expect(() => compile({ filters: [{ ...literal, column: 'uid' }] })).toThrow(/catalog rejects/u)
    expect(() => compile({ filters: [{ ...literal, valueSource: 'unknown' }] })).toThrow(/valueSource/u)
    expect(() => compile({ filters: [{ ...literal, values: ['extra'] }] })).toThrow(/only in may carry values/u)
  })

  it.each([
    [{ tableAlias: 'card', column: 'claimed_uid', operator: 'neq', valueSource: 'unclaimed-member' }, /unclaimed-member only supports/u],
    [{ tableAlias: 'card', column: 'claimed_uid', operator: 'eq', valueSource: 'unclaimed-member', value: '1' }, /unclaimed-member only supports/u],
    [{ tableAlias: 'card', column: 'claimed_uid', operator: 'eq', valueSource: 'unclaimed-member', values: ['1'] }, /unclaimed-member only supports/u],
    [{ tableAlias: 'card', column: 'card_name', operator: 'is-null', valueSource: 'literal' }, /null comparisons cannot/u],
    [{ tableAlias: 'card', column: 'card_name', operator: 'is-null', value: 'x' }, /null comparisons cannot/u],
    [{ tableAlias: 'card', column: 'card_name', operator: 'is-null', values: ['x'] }, /null comparisons cannot/u],
    [{ tableAlias: 'card', column: 'operator_uid', operator: 'in', valueSource: 'operator-uid', values: ['x'] }, /in requires/u],
    [{ tableAlias: 'card', column: 'card_name', operator: 'in', valueSource: 'literal', values: [] }, /in requires/u],
    [{ tableAlias: 'card', column: 'card_name', operator: 'in', valueSource: 'literal', values: Array(21).fill('x') }, /in requires/u],
  ])('rejects invalid special filter %#', (filter, message) => {
    expect(() => compile({ filters: [filter] })).toThrow(message)
  })

  it('compiles null, in, member, operator, unclaimed, and time-derived filters', () => {
    const compiled = compile({ filters: [
      { tableAlias: 'card', column: 'card_name', operator: 'is-null' },
      { tableAlias: 'card', column: 'card_name', operator: 'is-not-null' },
      { tableAlias: 'card', column: 'amount', operator: 'in', valueSource: 'literal', values: ['1', '+2.5', '.5'] },
      { tableAlias: 'card', column: 'mobile', operator: 'eq', valueSource: 'member-mobile' },
      { tableAlias: 'card', column: 'operator_uid', operator: 'eq', valueSource: 'operator-uid' },
      { tableAlias: 'card', column: 'claimed_uid', operator: 'eq', valueSource: 'unclaimed-member' },
      { tableAlias: 'card', column: 'created_at', operator: 'gte', valueSource: 'store-today' },
      { tableAlias: 'card', column: 'created_at', operator: 'lte', valueSource: 'store-now' },
    ] })

    expect(compiled.sql).toContain('IS NULL')
    expect(compiled.sql).toContain('IS NOT NULL')
    expect(compiled.sql).toContain('IN (?, ?, ?)')
    expect(compiled.parameters).toContain('13800138000')
    expect(compiled.parameters).toContain(56)
    expect(compiled.parameters).toContain(0)
    expect(compiled.parameters).toContain('2026-09-04')
    expect(compiled.parameters).toContain('2026-09-04 12:34:56')
  })

  it.each([undefined, ''])('requires a current member mobile when it is %s', (memberMobile) => {
    const queryScope: QueryScope = {
      storeId: scope.storeId,
      tenantId: scope.tenantId,
      operatorUid: scope.operatorUid,
      storeNow: scope.storeNow,
      ...(memberMobile === undefined ? {} : { memberMobile }),
    }
    expect(() => compile({ filters: [{
      tableAlias: 'card', column: 'mobile', operator: 'eq', valueSource: 'member-mobile',
    }] }, queryScope)).toThrow(/contains no member mobile/u)
  })

  it('validates and converts safe literal data types', () => {
    const filters = [
      { tableAlias: 'card', column: 'amount', operator: 'gt', valueSource: 'literal', value: '-1.5' },
      { tableAlias: 'card', column: 'created_at', operator: 'gte', valueSource: 'literal', value: '2026-09-04' },
      { tableAlias: 'card', column: 'created_at', operator: 'lte', valueSource: 'literal', value: '2026-09-04 12:34:56' },
      { tableAlias: 'card', column: 'starts_at', operator: 'eq', valueSource: 'literal', value: '123:45:56' },
    ]
    expect(compile({ filters }).parameters).toEqual([12, 34, '-1.5', '2026-09-04', '2026-09-04 12:34:56', '123:45:56'])
  })

  it.each([
    ['card_name', undefined, /literal must contain/u],
    ['card_name', '', /literal must contain/u],
    ['card_name', 'x'.repeat(201), /literal must contain/u],
    ['card_name', 'bad\u0000value', /literal must contain/u],
    ['amount', 'one', /numeric literal/u],
    ['created_at', 'today', /date literal/u],
    ['starts_at', 'soon', /time literal/u],
  ])('rejects invalid %s literal %s', (column, value, message) => {
    expect(() => compile({ filters: [{
      tableAlias: 'card', column, operator: 'eq', valueSource: 'literal',
      ...(value === undefined ? {} : { value }),
    }] })).toThrow(message)
  })

  it('escapes contains and prefix patterns and rejects non-literal pattern values', () => {
    const compiled = compile({ filters: [
      { tableAlias: 'card', column: 'card_name', operator: 'contains', valueSource: 'literal', value: String.raw`a%b_c\d` },
      { tableAlias: 'card', column: 'card_name', operator: 'prefix', valueSource: 'literal', value: 'start' },
    ] })
    expect(compiled.parameters).toEqual([12, 34, String.raw`%a\%b\_c\\d%`, 'start%'])
    expect(() => compile({ filters: [{
      tableAlias: 'card', column: 'operator_uid', operator: 'contains', valueSource: 'operator-uid',
    }] })).toThrow(/require a string literal/u)
  })

  it.each(['eq', 'neq', 'gt', 'gte', 'lt', 'lte'])('compiles comparison operator %s', (operator) => {
    expect(compile({ filters: [{
      tableAlias: 'card', column: 'amount', operator, valueSource: 'literal', value: '1',
    }] }).sql).toContain('?')
  })

  it('rejects an unknown comparison operator', () => {
    expect(() => compile({ filters: [{
      tableAlias: 'card', column: 'card_name', operator: 'between', valueSource: 'literal', value: 'a',
    }] })).toThrow(/filter operator/u)
  })

  it('validates ordering count, alias, field usage, and direction', () => {
    const order = { tableAlias: 'card', column: 'card_name', direction: 'asc' }
    expect(() => compile({ orderBy: Array.from({ length: 5 }, () => order) })).toThrow(/four order fields/u)
    expect(() => compile({ orderBy: [{ ...order, tableAlias: 'missing' }] })).toThrow(/unknown table alias/u)
    expect(() => compile({ orderBy: [{ ...order, column: 'uid' }] })).toThrow(/catalog rejects/u)
    expect(() => compile({ orderBy: [{ ...order, direction: 'sideways' }] })).toThrow(/direction must/u)
    expect(compile({ orderBy: [order, { ...order, column: 'amount', direction: 'DESC' }] }).sql).toContain('ORDER BY `card`.`card_name` ASC, `card`.`amount` DESC')
  })

  it.each([1.5, -1, 21])('rejects invalid limit %s', (limit) => {
    expect(() => compile({ limit })).toThrow(/limit must be/u)
  })
})
