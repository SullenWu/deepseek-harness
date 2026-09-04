# Customer-service database

English | [中文](customer-service-database.zh.md)

The [database package family](../../packages/database) gives a customer-service Agent a direct, read-only business-data source without turning the database plugin into another Agent. The model chooses search terms and authors a structured query plan; the plugin owns configuration validation, live request scope, catalog enforcement, parameterized SQL compilation, and bounded MySQL execution. A deployment selects this source or API-MCP for a service process, never both tool pairs and never an implicit fallback between them.

Source: [`packages/database/customer-service-database/src/index.ts`](../../packages/database/customer-service-database/src/index.ts), [`config.ts`](../../packages/database/customer-service-database/src/config.ts), [`catalog.ts`](../../packages/database/customer-service-database/src/catalog.ts), [`compiler.ts`](../../packages/database/customer-service-database/src/compiler.ts), and [`mysql.ts`](../../packages/database/customer-service-database/src/mysql.ts).

## Model-facing workflow

`search_business_schema` searches the reviewed table and field catalog using terms supplied by the model. Its result is schema policy rather than a current customer fact. `query_business_data` accepts only a structured selection, joins, filters, ordering, and row limit. It does not accept raw SQL, database or connection names, or store, tenant, operator, and member identity values.

The two-step design keeps semantic choice with the Agent while keeping authorization and SQL construction deterministic. No fixed customer-question-to-table mapping exists in the plugin or product skill.

## Request scope and configuration

The customer-service HTTP integration mounts the plugin once for each verified request. `storeId`, `operatorUid`, `merchantProfileVerified`, optional `memberMobile`, and the product code come from the trusted transport. Before each live query, the plugin checks the current operator and store relationship in the main database and resolves the tenant from that row. The model cannot replace these values.

Each product skill keeps its deployment-local connection catalog in ignored `runtime/data-access.local.json`, created from the tracked example. That file names only reviewed connections and execution limits. The loader rejects unsupported products, symbolic-link escapes, invalid connection options, overlapping finance routes, writable policy, and limits outside the hard safety bounds.

## Catalog and compiler

The tracked JSONL catalog is an allowlist. Every table declares a logical source, business semantics, tenant/store scope columns, fields, permitted usages, and aggregates. Relations explicitly authorize equality joins. The compiler accepts at most four joins, sixteen selected fields, sixteen filters, four order fields, and twenty result rows; the deployment policy may reduce those limits further.

Identifiers come only from validated catalog entries. Filter values become positional parameters. Server-owned value sources cover the current member mobile, operator uid, unclaimed-member sentinel, store date, and store time. Every table alias receives its declared store and tenant predicates, so a join cannot silently escape the verified request scope.

## Read-only execution and evidence

MySQL execution opens an explicit read-only transaction, runs one compiled `SELECT`, and rolls back. Cancellation destroys the active connection, query timeouts are bounded, returned fields and rows are capped, strings are sanitized and truncated, binary or unsupported values are hidden, and the serialized result has a configured maximum size.

A successful result is evidence only for that one current read query inside the verified product, store, and tenant scope. It does not prove a write, submission, payment, notification, or another downstream business effect.
