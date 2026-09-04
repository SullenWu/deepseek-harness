/** Compile a model-authored structured plan into one catalog-constrained SELECT. */

import type {
  CatalogField,
  CatalogRelation,
  CatalogTable,
  CompiledQuery,
  DynamicQueryPlan,
  QueryCatalog,
  QueryFilter,
  QueryScope,
} from './types.ts'

const IDENTIFIER = /^[A-Za-z_][A-Za-z0-9_]{0,63}$/u
const NUMERIC_TYPES = new Set([
  'bit', 'bool', 'boolean', 'tinyint', 'smallint', 'mediumint', 'int', 'integer', 'bigint',
  'decimal', 'numeric', 'float', 'double', 'real', 'year',
])
const DATE_TYPES = new Set(['date', 'datetime', 'timestamp'])

function identifier(value: string, label: string): string {
  const normalized = value.trim()
  if (!IDENTIFIER.test(normalized)) throw new Error(`${label} has an invalid identifier`)
  return normalized
}

function quote(value: string): string {
  return `\`${identifier(value, 'SQL identifier')}\``
}

function qualified(alias: string, column: string): string {
  return `${quote(alias)}.${quote(column)}`
}

function tableByName(tables: Map<string, CatalogTable>, name: string): CatalogTable {
  const normalized = identifier(name, 'table name').toLocaleLowerCase()
  const table = tables.get(normalized)
  if (table === undefined) throw new Error('query table is not present in the reviewed catalog')
  return table
}

function tableByAlias(aliases: Map<string, CatalogTable>, alias: string): CatalogTable {
  const normalized = identifier(alias, 'table alias').toLocaleLowerCase()
  const table = aliases.get(normalized)
  if (table === undefined) throw new Error('query references an unknown table alias')
  return table
}

function fieldFor(table: CatalogTable, name: string, usage: string): CatalogField {
  const normalized = identifier(name, 'field name').toLocaleLowerCase()
  const field = table.fields.find(candidate => candidate.name.toLocaleLowerCase() === normalized)
  if (field === undefined || !field.usages.some(candidate => candidate.toLocaleLowerCase() === usage)) {
    const allowed = field === undefined ? 'field is not authorized' : field.usages.join(',')
    const countHint = usage === 'select'
      ? '; use column="*" and aggregate="count" for an authorized row count'
      : ''
    throw new Error(`catalog rejects ${table.table}.${name} for ${usage}; allowed=${allowed}${countHint}`)
  }
  return field
}

function hasRelation(
  relations: CatalogRelation[],
  source: string,
  leftTable: string,
  leftColumn: string,
  rightTable: string,
  rightColumn: string,
): boolean {
  const equals = (left: string, right: string): boolean => left.toLocaleLowerCase() === right.toLocaleLowerCase()
  return relations.some(relation => relation.dataSource.toLocaleLowerCase() === source
    && ((equals(relation.leftTable, leftTable)
      && equals(relation.leftColumn, leftColumn)
      && equals(relation.rightTable, rightTable)
      && equals(relation.rightColumn, rightColumn))
      || (equals(relation.leftTable, rightTable)
        && equals(relation.leftColumn, rightColumn)
        && equals(relation.rightTable, leftTable)
        && equals(relation.rightColumn, leftColumn))))
}

function normalizeSource(value: string): 'main' | 'finance' {
  const normalized = value.trim().toLocaleLowerCase()
  if (normalized !== 'main' && normalized !== 'finance') throw new Error('dataSource must be main or finance')
  return normalized
}

function normalizeAggregate(value: string | undefined): '' | 'COUNT' | 'SUM' | 'MIN' | 'MAX' {
  const normalized = value?.trim().toLocaleLowerCase() ?? ''
  if (normalized === '') return ''
  if (normalized === 'count') return 'COUNT'
  if (normalized === 'sum') return 'SUM'
  if (normalized === 'min') return 'MIN'
  if (normalized === 'max') return 'MAX'
  throw new Error('aggregate must be count, sum, min, or max')
}

function convertLiteral(value: string | undefined, dataType: string): unknown {
  const text = value?.trim() ?? ''
  if (text.length === 0 || text.length > 200 || /[\u0000-\u001f\u007f]/u.test(text)) {
    throw new Error('literal must contain 1 to 200 safe characters')
  }
  const type = dataType.toLocaleLowerCase()
  if (NUMERIC_TYPES.has(type)) {
    if (!/^[+-]?(?:\d+(?:\.\d+)?|\.\d+)$/u.test(text)) throw new Error('numeric literal has an invalid format')
    return text
  }
  if (DATE_TYPES.has(type)) {
    if (!/^\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?$/u.test(text)) {
      throw new Error('date literal has an invalid format')
    }
    return text
  }
  if (type === 'time' && !/^\d{1,3}:\d{2}(?::\d{2})?$/u.test(text)) {
    throw new Error('time literal has an invalid format')
  }
  return text
}

function addParameter(parameters: unknown[], value: unknown): string {
  parameters.push(value)
  return '?'
}

function escapeLike(value: string): string {
  return value.replaceAll('\\', '\\\\').replaceAll('%', '\\%').replaceAll('_', '\\_')
}

function compileFilter(
  filter: QueryFilter,
  aliases: Map<string, CatalogTable>,
  scope: QueryScope,
  parameters: unknown[],
): string {
  const alias = identifier(filter.tableAlias, 'filter table alias')
  const table = tableByAlias(aliases, alias)
  const operator = filter.operator.trim().toLocaleLowerCase()
  const valueSource = filter.valueSource?.trim().toLocaleLowerCase() ?? ''
  const usage = valueSource === 'member-mobile'
    ? 'member-mobile-filter'
    : valueSource === 'operator-uid'
      ? 'operator-uid-filter'
      : valueSource === 'unclaimed-member'
        ? 'unclaimed-member-filter'
        : 'literal-filter'
  const field = fieldFor(table, filter.column, usage)
  const column = qualified(alias, field.name)
  const values = filter.values ?? []

  if (valueSource === 'unclaimed-member'
    && (operator !== 'eq' || (filter.value?.trim().length ?? 0) > 0 || values.length > 0)) {
    throw new Error('unclaimed-member only supports eq without an explicit value')
  }
  if (operator === 'is-null' || operator === 'is-not-null') {
    if (valueSource !== '' || (filter.value?.trim().length ?? 0) > 0 || values.length > 0) {
      throw new Error('null comparisons cannot carry a value')
    }
    return `${column}${operator === 'is-null' ? ' IS NULL' : ' IS NOT NULL'}`
  }
  if (operator === 'in') {
    if (valueSource !== 'literal' || values.length === 0 || values.length > 20) {
      throw new Error('in requires 1 to 20 literal values')
    }
    const placeholders = values.map(value => addParameter(parameters, convertLiteral(value, field.dataType)))
    return `${column} IN (${placeholders.join(', ')})`
  }

  let value: unknown
  if (valueSource === 'member-mobile') {
    if (scope.memberMobile === undefined || scope.memberMobile === '') {
      throw new Error('the current message contains no member mobile available to the database tool')
    }
    value = scope.memberMobile
  } else if (valueSource === 'operator-uid') {
    value = scope.operatorUid
  } else if (valueSource === 'unclaimed-member') {
    value = 0
  } else if (valueSource === 'store-today') {
    value = scope.storeNow.toISOString().slice(0, 10)
  } else if (valueSource === 'store-now') {
    value = scope.storeNow.toISOString().slice(0, 19).replace('T', ' ')
  } else if (valueSource === 'literal') {
    value = convertLiteral(filter.value, field.dataType)
  } else {
    throw new Error('valueSource is not present in the reviewed catalog contract')
  }
  if (values.length > 0) throw new Error('only in may carry values')
  if (operator === 'contains' || operator === 'prefix') {
    if (valueSource !== 'literal' || typeof value !== 'string') {
      throw new Error('contains and prefix require a string literal')
    }
    const pattern = operator === 'contains' ? `%${escapeLike(value)}%` : `${escapeLike(value)}%`
    return `${column} LIKE ${addParameter(parameters, pattern)} ESCAPE '\\\\'`
  }
  const sqlOperator = new Map([
    ['eq', '='], ['neq', '<>'], ['gt', '>'], ['gte', '>='], ['lt', '<'], ['lte', '<='],
  ]).get(operator)
  if (sqlOperator === undefined) throw new Error('filter operator is not present in the reviewed contract')
  return `${column} ${sqlOperator} ${addParameter(parameters, value)}`
}

/**
 * Validate and compile a structured query plan.
 * @param catalog - Reviewed table, field, usage, scope, and relation catalog.
 * @param plan - Model-authored structured plan without SQL or identity scope.
 * @param scope - Server-owned live scope.
 * @returns One parameterized SELECT and ordered parameter list.
 */
export function compileQuery(catalog: QueryCatalog, plan: DynamicQueryPlan, scope: QueryScope): CompiledQuery {
  if (catalog.tables.length === 0) throw new Error('query catalog is empty')
  if (scope.storeId < 1 || scope.tenantId < 1 || scope.operatorUid < 1) {
    throw new Error('trusted store, tenant, or operator scope is missing')
  }
  const dataSource = normalizeSource(plan.dataSource)
  const tables = new Map(catalog.tables
    .filter(table => table.dataSource.toLocaleLowerCase() === dataSource)
    .map(table => [table.table.toLocaleLowerCase(), table]))
  const aliases = new Map<string, CatalogTable>()
  const scopedAliases: Array<{ alias: string; table: CatalogTable }> = []
  const rootAlias = identifier(plan.root.alias, 'root alias')
  const rootTable = tableByName(tables, plan.root.table)
  aliases.set(rootAlias.toLocaleLowerCase(), rootTable)
  scopedAliases.push({ alias: rootAlias, table: rootTable })

  const joins = plan.joins ?? []
  if (joins.length > 4) throw new Error('query supports at most four joins')
  const joinSql: string[] = []
  for (const join of joins) {
    const alias = identifier(join.alias, 'join alias')
    const leftAlias = identifier(join.leftAlias, 'left join alias')
    const rightAlias = identifier(join.rightAlias, 'right join alias')
    if (alias.toLocaleLowerCase() !== rightAlias.toLocaleLowerCase()) {
      throw new Error('rightAlias must equal the new join alias')
    }
    const leftTable = aliases.get(leftAlias.toLocaleLowerCase())
    if (aliases.has(alias.toLocaleLowerCase()) || leftTable === undefined) {
      throw new Error('join alias is duplicate or leftAlias has not been added')
    }
    const rightTable = tableByName(tables, join.table)
    const leftColumn = identifier(join.leftColumn, 'left join column')
    const rightColumn = identifier(join.rightColumn, 'right join column')
    if (!hasRelation(catalog.relations, dataSource, leftTable.table, leftColumn, rightTable.table, rightColumn)) {
      throw new Error('join relationship is not present in the reviewed catalog')
    }
    const type = join.type?.trim().toLocaleLowerCase() ?? 'inner'
    if (type !== 'inner' && type !== 'left') throw new Error('join type must be inner or left')
    joinSql.push(`${type.toLocaleUpperCase()} JOIN ${quote(rightTable.table)} AS ${quote(alias)} ON ${qualified(leftAlias, leftColumn)} = ${qualified(alias, rightColumn)}`)
    aliases.set(alias.toLocaleLowerCase(), rightTable)
    scopedAliases.push({ alias, table: rightTable })
  }

  if (plan.select.length === 0 || plan.select.length > 16) throw new Error('select must contain 1 to 16 fields')
  const outputNames = new Set<string>()
  const outputNameList: string[] = []
  const selectSql: string[] = []
  const groupBySql: string[] = []
  let hasAggregate = false
  for (const selection of plan.select) {
    const table = tableByAlias(aliases, selection.tableAlias)
    const alias = identifier(selection.tableAlias, 'select table alias')
    const outputName = identifier(selection.outputName, 'output name')
    const outputKey = outputName.toLocaleLowerCase()
    if (outputNames.has(outputKey)) throw new Error('output names must be unique')
    outputNames.add(outputKey)
    outputNameList.push(outputName)
    const aggregate = normalizeAggregate(selection.aggregate)
    let expression: string
    if (aggregate === 'COUNT' && selection.column === '*') {
      if (!table.rowCountAggregates.some(value => value.toLocaleLowerCase() === 'count')) {
        throw new Error(`catalog rejects count(*) on ${table.table}`)
      }
      expression = 'COUNT(*)'
      hasAggregate = true
    } else {
      const field = fieldFor(table, selection.column, 'select')
      expression = qualified(alias, field.name)
      if (aggregate !== '') {
        if (!field.aggregates.some(value => value.toLocaleLowerCase() === aggregate.toLocaleLowerCase())) {
          throw new Error(`catalog rejects ${aggregate.toLocaleLowerCase()} on ${table.table}.${field.name}`)
        }
        if (aggregate === 'SUM' && !NUMERIC_TYPES.has(field.dataType.toLocaleLowerCase())) {
          throw new Error('sum requires a numeric field')
        }
        expression = `${aggregate}(${expression})`
        hasAggregate = true
      } else {
        groupBySql.push(expression)
      }
    }
    selectSql.push(`${expression} AS ${quote(outputName)}`)
  }

  const parameters: unknown[] = []
  const whereSql: string[] = []
  for (const { alias, table } of scopedAliases) {
    if (table.scopeColumns.length === 0) throw new Error(`table ${table.table} has no scope column`)
    if (table.scopeColumns.some(column => column.toLocaleLowerCase() === 'store_id')) {
      whereSql.push(`${qualified(alias, 'store_id')} = ${addParameter(parameters, scope.storeId)}`)
    }
    if (table.scopeColumns.some(column => column.toLocaleLowerCase() === 'tenant_id')) {
      whereSql.push(`${qualified(alias, 'tenant_id')} = ${addParameter(parameters, scope.tenantId)}`)
    }
  }
  const filters = plan.filters ?? []
  if (filters.length > 16) throw new Error('query supports at most sixteen filters')
  for (const filter of filters) whereSql.push(compileFilter(filter, aliases, scope, parameters))

  const orderBy = plan.orderBy ?? []
  if (orderBy.length > 4) throw new Error('query supports at most four order fields')
  const orderSql = orderBy.map((order) => {
    const table = tableByAlias(aliases, order.tableAlias)
    const field = fieldFor(table, order.column, 'order')
    const direction = order.direction.trim().toLocaleLowerCase()
    if (direction !== 'asc' && direction !== 'desc') throw new Error('order direction must be asc or desc')
    return `${qualified(order.tableAlias, field.name)} ${direction.toLocaleUpperCase()}`
  })

  const mixedAggregate = hasAggregate && plan.select.some(selection => normalizeAggregate(selection.aggregate) === '')
  const groupSql = mixedAggregate ? [...new Set(groupBySql)] : []
  const limit = plan.limit === undefined || plan.limit === 0 ? 10 : plan.limit
  if (!Number.isSafeInteger(limit) || limit < 1 || limit > 20) throw new Error('limit must be an integer from 1 to 20')
  const distinct = plan.distinct === true && !hasAggregate ? 'DISTINCT ' : ''
  const sql = [
    `SELECT ${distinct}${selectSql.join(', ')} FROM ${quote(rootTable.table)} AS ${quote(rootAlias)}`,
    ...joinSql,
    `WHERE ${whereSql.join(' AND ')}`,
    ...(groupSql.length > 0 ? [`GROUP BY ${groupSql.join(', ')}`] : []),
    ...(orderSql.length > 0 ? [`ORDER BY ${orderSql.join(', ')}`] : []),
    `LIMIT ${limit}`,
  ].join(' ')
  return { sql, parameters, dataSource, outputNames: outputNameList, limit }
}
