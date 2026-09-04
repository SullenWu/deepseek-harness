/**
 * Data records shared by the customer-service query catalog, compiler, MySQL
 * executor, and model-facing Consumer.
 * @module @deepseek-ai/dsh-customer-service-database/types
 */

/** One model-authored reference to a catalog table. */
export interface QueryTableRef {
  /** Catalog table name. */
  table: string
  /** Query-local alias. */
  alias: string
}

/** One model-authored selected field or aggregate. */
export interface QuerySelect {
  /** Query-local table alias. */
  tableAlias: string
  /** Catalog field, or `*` for an authorized row count. */
  column: string
  /** Stable result key chosen by the model. */
  outputName: string
  /** Optional aggregate. */
  aggregate?: string
}

/** One model-authored catalog-authorized equality join. */
export interface QueryJoin {
  /** Join kind. */
  type?: string
  /** Catalog table to add. */
  table: string
  /** Query-local alias for the new table. */
  alias: string
  /** Existing alias on the left side. */
  leftAlias: string
  /** Left catalog column. */
  leftColumn: string
  /** Alias of the new table; must equal `alias`. */
  rightAlias: string
  /** Right catalog column. */
  rightColumn: string
}

/** One model-authored parameterized filter. */
export interface QueryFilter {
  /** Query-local table alias. */
  tableAlias: string
  /** Catalog field. */
  column: string
  /** Catalog-supported comparison. */
  operator: string
  /** Server or model value source. */
  valueSource?: string
  /** Single literal value. */
  value?: string
  /** Literal values for `in`. */
  values?: string[]
}

/** One model-authored ordering expression. */
export interface QueryOrder {
  /** Query-local table alias. */
  tableAlias: string
  /** Catalog field. */
  column: string
  /** `asc` or `desc`. */
  direction: string
}

/** Structured read-only query plan accepted from the model. */
export interface DynamicQueryPlan {
  /** Logical data source: `main` or `finance`. */
  dataSource: string
  /** Root catalog table. */
  root: QueryTableRef
  /** Returned fields and aggregates. */
  select: QuerySelect[]
  /** Catalog-authorized joins. */
  joins?: QueryJoin[]
  /** Parameterized filters. */
  filters?: QueryFilter[]
  /** Authorized ordering expressions. */
  orderBy?: QueryOrder[]
  /** Maximum rows. */
  limit?: number
  /** De-duplicate non-aggregate rows. */
  distinct?: boolean
}

/** Server-owned query scope that model arguments cannot override. */
export interface QueryScope {
  /** Verified current store. */
  storeId: number
  /** Live tenant resolved from the main database. */
  tenantId: number
  /** Verified current operator. */
  operatorUid: number
  /** Member mobile extracted from the current transport message, when present. */
  memberMobile?: string
  /** Current time used by server-owned temporal value sources. */
  storeNow: Date
}

/** One allowlisted field. */
export interface CatalogField {
  /** Physical field name. */
  name: string
  /** MySQL data type. */
  dataType: string
  /** Human-readable business meaning. */
  comment: string
  /** Explicit allowed usages. */
  usages: string[]
  /** Explicit allowed aggregates. */
  aggregates: string[]
}

/** One allowlisted table. */
export interface CatalogTable {
  /** Query policy version. */
  policyVersion: number
  /** Tenant/store scope policy version. */
  scopeVersion: number
  /** Logical data source. */
  dataSource: string
  /** Physical table name. */
  table: string
  /** Business domain. */
  domain: string
  /** Reviewed business group. */
  businessGroup: string
  /** Authorized audience. */
  audience: string
  /** Source authority. */
  authority: string
  /** Field review policy. */
  fieldPolicy: string
  /** Human-readable table meaning. */
  comment: string
  /** Scope columns injected for every alias. */
  scopeColumns: string[]
  /** Authorized aggregates that do not read a concrete field. */
  rowCountAggregates: string[]
  /** Allowlisted fields. */
  fields: CatalogField[]
}

/** One allowlisted equality relationship. */
export interface CatalogRelation {
  /** Logical data source. */
  dataSource: string
  /** Left table. */
  leftTable: string
  /** Left column. */
  leftColumn: string
  /** Right table. */
  rightTable: string
  /** Right column. */
  rightColumn: string
  /** Repository evidence count. */
  occurrences: number
}

/** Loaded immutable query catalog. */
export interface QueryCatalog {
  /** Allowlisted tables. */
  tables: CatalogTable[]
  /** Allowlisted relations. */
  relations: CatalogRelation[]
}

/** Parameterized SQL compiled exclusively from catalog identifiers. */
export interface CompiledQuery {
  /** Single SELECT statement with positional placeholders. */
  sql: string
  /** Values in placeholder order. */
  parameters: unknown[]
  /** Resolved logical data source. */
  dataSource: 'main' | 'finance'
  /** Output keys exposed to the model. */
  outputNames: string[]
  /** Enforced result limit. */
  limit: number
}
