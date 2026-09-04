---
description: "Catalog-constrained MySQL tools for deployments that let a customer-service agent discover schema and query current business facts directly."
kind: "package-reference"
---

# @deepseek-ai/dsh-customer-service-database

English | [中文](README.zh.md)

## Summary

This package lets a customer-service agent search a reviewed schema catalog and execute one structured read-only query against current MySQL data. Choose it when Harness connects directly to product databases instead of API-MCP. The model chooses tables, fields, relations, filters, and aggregates; the package revalidates the operator/store relationship and owns tenant injection, parameterized SQL compilation, shard selection, limits, and execution. It does not accept raw SQL, connection names, credentials, StoreId, TenantId, UID, or mobile numbers as tool arguments.

## Table of Contents

- [Use this package](#use-this-package)
- [Understand the implementation](#understand-the-implementation)
- [Further Exploration](#further-exploration)
- [Model Experience](#model-experience)
- [Known Limitations and Deferred Work](#known-limitations-and-deferred-work)
- [Dev Note](#dev-note)

-----

<a id="use-this-package"></a>
## Use this package

Mount one instance in a request-local process after the transport has selected a product and verified a merchant profile.

### When to choose it

Choose this package for direct read-only MySQL access with a reviewed product catalog and least-privilege database accounts. Choose `@deepseek-ai/dsh-mcp-client` with its capability broker when the deployment uses API-MCP. Do not mount both tool families for the same customer-service process.

### Minimal configuration

The integration supplies these values from request-local environment variables; a model never writes this configuration.

```yaml
- name: '@deepseek-ai/dsh-customer-service-database'
  config:
    skillRoot: /srv/customer-service/skills
    productCode: kxm_pc
    storeId: 12
    operatorUid: 34
    merchantProfileVerified: true
```

| Field | Default | Meaning |
|---|---|---|
| `skillRoot` | required | Server-owned root containing product skill directories and private runtime configuration |
| `productCode` | required | Trusted transport product code used to select one product data domain |
| `storeId` | required | Trusted current store, revalidated against MySQL for every query |
| `operatorUid` | required | Trusted current operator, revalidated against the store for every query |
| `merchantProfileVerified` | required | Load-time gate proving the transport completed merchant-profile verification |
| `memberMobile` | absent | Request-local mobile extracted by the transport and available only through the `member-mobile` value source |
| `maxCatalogTables` | `8` | Maximum table matches returned by one schema search; valid range 1–20 |

The generated [configuration catalog](../../../docs/config-catalog.md#deepseek-aidsh-customer-service-database) is the exhaustive source for every accepted field. The selected product skill must contain `runtime/data-access.local.json`; the tracked `data-access.example.json` documents its server-local format and contains no production credential.

-----

<a id="understand-the-implementation"></a>
## Understand the implementation

<details>
<summary>Implementation internals — click to expand</summary>

The schema tool searches reviewed JSONL records without deciding which business question maps to which table. The query tool first revalidates the current operator and store in the main database, resolves the tenant and store time, validates every plan identifier and usage against the catalog, injects scope for every alias, and compiles one parameterized `SELECT`. The MySQL provider opens an explicit read-only transaction, selects only the configured main database or deterministic tenant shard, normalizes bounded cells, and rolls the transaction back.

| File | Role |
|---|---|
| [`src/catalog.ts`](src/catalog.ts) | Loads and searches reviewed table, field, usage, scope, and relation records |
| [`src/compiler.ts`](src/compiler.ts) | Rejects unknown plan elements and compiles parameterized SQL |
| [`src/config.ts`](src/config.ts) | Loads private product connections, shard routes, and execution limits |
| [`src/mysql.ts`](src/mysql.ts) | Revalidates live scope and executes one read-only query |
| [`src/index.ts`](src/index.ts) | Publishes the two model-facing tools for one request |

**Runtime invariant:** No companion is published. The request-local plugin retains no mutable cross-plugin relationship: each query re-reads authoritative main-database scope, while catalog validation, compilation, provider execution, and Loader composition are covered directly by behavior tests.

</details>

-----

<a id="further-exploration"></a>
## Further Exploration

- [Database group map](../README.md) — package-family ownership.
- [Customer-service API integration](../../../integrations/customer-service-api/README.md) — request transport and mutually exclusive data-source selection.
- [Tool authoring reference](../../../docs/cookbook/adding-a-tool.md) — tool validation and canonical result rules.
- [Capability seams](../../../docs/architecture.md) — Service Definition, Provider, and Consumer roles.

-----

<a id="model-experience"></a>
## Model Experience

### `search_business_schema` tool

#### What the model sees

The [generated tool catalog](../../../docs/tool-catalog.md#search_business_schema) records the exhaustive argument and result schema. The description states that results are reviewed schema policy rather than live facts, and that the model chooses search terms without fixed question-to-table routing.

#### Token effect

The tool schema is fixed while the plugin is mounted. Each result adds a capped table-and-field subset plus relations among the returned tables.

#### KV Cache effect

The tool schema is prefix-stable for the request-local process. Tool results append after the reusable request prefix.

### `query_business_data` tool

#### What the model sees

The [generated tool catalog](../../../docs/tool-catalog.md#query_business_data) records the exhaustive structured-plan and result schema. The description forbids SQL and identity arguments. A successful result contains only the logical data source, bounded business rows, row count, and evidence boundary; it never contains compiled SQL, connection information, or injected scope values unless an allowlisted selected business field independently contains the same value.

#### Token effect

The tool schema is fixed while the plugin is mounted. Each call appends one bounded result whose serialized size is limited by the product's private execution policy.

#### KV Cache effect

The tool schema is prefix-stable for the request-local process. Query results append after the reusable request prefix.

## Known Limitations and Deferred Work

<a id="known-limitations-and-deferred-work"></a>

These limits determine when the direct database source is unsuitable.

- **Merchant requests only** — the package requires a verified merchant store and operator; it does not implement customer-subject grants.
- **Catalog availability** — both product domains currently use the reviewed query catalog stored in the kexiaomi product skill, while each domain keeps separate private connections.
- **Transport trust** — the package revalidates operator/store membership but relies on the caller's loopback or protected transport for the initial product, operator, store, and merchant-verification claims.
- **MySQL only** — connection parsing and read-only transaction behavior target MySQL-compatible servers.

<a id="dev-note"></a>
### Dev Note

<details>
<summary>Working context for maintainers — click to expand</summary>

None.

</details>
