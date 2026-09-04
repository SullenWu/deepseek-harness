---
description: "受目录约束的 MySQL 工具，供客服 Agent 发现结构并直接查询当前业务事实的部署使用。"
kind: "package-reference"
---

# @deepseek-ai/dsh-customer-service-database

[English](README.md) | 中文

## 概述

本包让客服 Agent 搜索经审核的结构目录，并针对当前 MySQL 数据执行一条结构化只读查询。当 Harness 直接连接产品数据库而不使用 API-MCP 时选择它。模型选择表、字段、关系、过滤与聚合；本包重新核验操作人／门店关系，并负责租户注入、参数化 SQL 编译、分库选择、限制与执行。工具参数不接受原始 SQL、连接名、凭据、StoreId、TenantId、UID 或手机号。

## 目录

- [使用本包](#use-this-package)
- [理解实现](#understand-the-implementation)
- [进一步探索](#further-exploration)
- [模型体验](#model-experience)
- [已知限制与延期工作](#known-limitations-and-deferred-work)
- [开发备注](#dev-note)

-----

<a id="use-this-package"></a>
## 使用本包

传输层选定产品并核验商家档案后，在请求独占的进程中挂载一个实例。

### 何时选择

当部署使用经审核的产品目录和最小权限数据库账号直连只读 MySQL 时选择本包。当部署使用 API-MCP 时，选择带 capability broker 的 `@deepseek-ai/dsh-mcp-client`。同一客服进程不得同时挂载两组工具。

### 最小配置

集成从请求本地环境变量提供这些值；模型绝不会编写此配置。

```yaml
- name: '@deepseek-ai/dsh-customer-service-database'
  config:
    skillRoot: /srv/customer-service/skills
    productCode: kxm_pc
    storeId: 12
    operatorUid: 34
    merchantProfileVerified: true
```

| 字段 | 默认值 | 含义 |
|---|---|---|
| `skillRoot` | 必填 | 包含产品 skill 目录与私有运行配置的服务端根目录 |
| `productCode` | 必填 | 用于选择一个产品数据域的可信传输产品编码 |
| `storeId` | 必填 | 可信当前门店，每次查询都会对 MySQL 重新核验 |
| `operatorUid` | 必填 | 可信当前操作人，每次查询都会重新核验其门店关系 |
| `merchantProfileVerified` | 必填 | 证明传输层已完成商家档案核验的加载期闸门 |
| `memberMobile` | 缺省 | 由传输层从当前请求提取、仅能通过 `member-mobile` 值来源使用的手机号 |
| `maxCatalogTables` | `8` | 单次结构搜索最多返回的匹配表数；有效范围 1–20 |

生成的[配置目录](../../../docs/config-catalog.zh.md#deepseek-aidsh-customer-service-database)是全部受支持字段的穷尽式真源。选中的产品 skill 必须包含 `runtime/data-access.local.json`；已跟踪的 `data-access.example.json` 说明其服务端本地格式，且不包含生产凭据。

-----

<a id="understand-the-implementation"></a>
## 理解实现

<details>
<summary>实现细节——点击展开</summary>

结构工具搜索经审核的 JSONL 记录，不决定业务问题应该映射到哪张表。查询工具先在主库重新核验当前操作人与门店，解析租户与门店时间，针对目录验证计划中的每个标识符和用法，为每个别名注入范围，并编译一条参数化 `SELECT`。MySQL 提供方开启显式只读事务，只选择已配置的主库或确定性租户分库，归一化有界单元格，并回滚事务。

| 文件 | 职责 |
|---|---|
| [`src/catalog.ts`](src/catalog.ts) | 加载并搜索经审核的表、字段、用法、范围与关系记录 |
| [`src/compiler.ts`](src/compiler.ts) | 拒绝未知计划元素并编译参数化 SQL |
| [`src/config.ts`](src/config.ts) | 加载私有产品连接、分库路由与执行限制 |
| [`src/mysql.ts`](src/mysql.ts) | 重新核验实时范围并执行一条只读查询 |
| [`src/index.ts`](src/index.ts) | 为一个请求发布两个模型可见工具 |

**运行时不变量：** 不发布伴随检查。该请求本地插件不保留可变的跨插件关系：每次查询都会重新读取主库的权威范围，目录校验、编译、提供方执行与 Loader 组合由行为测试直接覆盖。

</details>

-----

<a id="further-exploration"></a>
## 进一步探索

- [Database 组地图](../README.zh.md)——包族职责。
- [客服 API 集成](../../../integrations/customer-service-api/README.zh.md)——请求传输与互斥数据源选择。
- [工具编写参考](../../../docs/cookbook/adding-a-tool.zh.md)——工具校验与规范结果规则。
- [能力接缝](../../../docs/architecture.zh.md)——Service Definition、Provider 与 Consumer 职责。

-----

<a id="model-experience"></a>
## 模型体验

### `search_business_schema` 工具

#### 模型看到什么

[生成的工具目录](../../../docs/tool-catalog.zh.md#search_business_schema)记录穷尽的参数与结果结构。描述会说明结果是经审核的结构策略而不是实时事实，模型自行选择搜索词，不使用固定的问题到表路由。

#### Token 影响

插件挂载期间工具结构固定。每个结果追加一个受上限约束的表与字段子集，以及返回表之间的关系。

#### KV Cache 影响

工具结构在请求独占进程内保持前缀稳定。工具结果追加在可复用请求前缀之后。

### `query_business_data` 工具

#### 模型看到什么

[生成的工具目录](../../../docs/tool-catalog.zh.md#query_business_data)记录穷尽的结构化计划与结果结构。描述禁止 SQL 与身份参数。成功结果仅包含逻辑数据源、有界业务行、行数和证据边界；它绝不包含编译后 SQL、连接信息或注入的范围值，除非某个已授权选择的业务字段独立包含相同值。

#### Token 影响

插件挂载期间工具结构固定。每次调用追加一项有界结果，其序列化大小由产品私有执行策略限制。

#### KV Cache 影响

工具结构在请求独占进程内保持前缀稳定。查询结果追加在可复用请求前缀之后。

## 已知限制与延期工作

<a id="known-limitations-and-deferred-work"></a>

以下限制决定数据库直连源何时不适用。

- **仅商家请求**——本包要求已核验的商家门店与操作人；它不实现顾客主体授权。
- **目录可用性**——两个产品数据域目前共用课小秘产品 skill 中经审核的查询目录，但各自保留独立私有连接。
- **传输信任**——本包重新核验操作人／门店成员关系，但初始产品、操作人、门店与商家核验声明依赖调用方的回环或受保护传输。
- **仅 MySQL**——连接解析与只读事务行为面向 MySQL 兼容服务器。

<a id="dev-note"></a>
### 开发备注

<details>
<summary>维护者的工作上下文——点击展开</summary>

无。

</details>
