---
description: "The database package group: reviewed-schema discovery and read-only business-data access for agents and deployments choosing direct database tools."
kind: "package-group"
---

# database/ — Controlled business-data access

English | [中文](README.zh.md)

## Summary

The database group lets an agent discover a reviewed business schema and execute bounded read-only queries without receiving database credentials or tenant identifiers. The customer-service package owns the complete request-local path from catalog search through live authorization, parameterized compilation, and MySQL execution. It is an alternative data source to API-MCP, not an additional reasoning agent.

## Table of Contents

- [Packages](#packages)
- [Related documentation](#related-documentation)
- [Dev Note](#dev-note)

-----

<a id="packages"></a>
## Packages

The group currently contains one customer-service-specific composition plugin.

| Package | Role |
|---|---|
| [`customer-service-database/`](customer-service-database/README.md) | Publishes reviewed schema discovery and structured read-only query tools for one verified customer-service request |

<a id="related-documentation"></a>
## Related documentation

- [Customer-service database subsystem](../../docs/subsystems/customer-service-database.md) — request scope, reviewed catalog, structured compilation, and read-only execution.
- [Tool authoring reference](../../docs/cookbook/adding-a-tool.md) — model-facing tool and result contracts.
- [Customer-service API integration](../../integrations/customer-service-api/README.md) — selects Database or ApiMcp for each service process.

<a id="dev-note"></a>
## Dev Note

None.
