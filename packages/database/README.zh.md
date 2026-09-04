---
description: "database 包组：经审核的结构发现与只读业务数据访问，供选择数据库直连工具的 Agent 和部署人员阅读。"
kind: "package-group"
---

# database/ — 受控业务数据访问

[English](README.md) | 中文

## 概述

database 组让 Agent 在不接触数据库凭据或租户标识的前提下，发现经审核的业务结构并执行有界只读查询。客服包拥有从目录搜索、实时授权、参数化编译到 MySQL 执行的完整请求内路径。它是 API-MCP 的替代数据源，不是额外的推理 Agent。

## 目录

- [包](#packages)
- [相关文档](#related-documentation)
- [开发备注](#dev-note)

-----

<a id="packages"></a>
## 包

该组目前包含一个客服专用组合插件。

| 包 | 职责 |
|---|---|
| [`customer-service-database/`](customer-service-database/README.zh.md) | 为一项已核验客服请求发布经审核的结构发现与结构化只读查询工具 |

<a id="related-documentation"></a>
## 相关文档

- [客服数据库子系统](../../docs/subsystems/customer-service-database.zh.md)——请求作用域、审核目录、结构化编译与只读执行。
- [工具编写参考](../../docs/cookbook/adding-a-tool.zh.md)——模型可见工具与结果约定。
- [客服 API 集成](../../integrations/customer-service-api/README.zh.md)——为每个服务进程选择 Database 或 ApiMcp。

<a id="dev-note"></a>
## 开发备注

无。
