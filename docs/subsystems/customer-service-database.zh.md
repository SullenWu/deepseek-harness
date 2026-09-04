# 客服数据库

[English](customer-service-database.md) | 中文

[`database` 包族](../../packages/database)为客服 Agent 提供一项数据库直连的只读业务数据源，但不会把数据库插件变成另一个 Agent。模型选择搜索词并编写结构化查询计划；插件拥有配置校验、实时请求作用域、目录约束、参数化 SQL 编译和有界 MySQL 执行。部署为一个服务进程选择该数据源或 API-MCP，绝不同时发布两组工具，也绝不在两者之间隐式回退。

源码：[`packages/database/customer-service-database/src/index.ts`](../../packages/database/customer-service-database/src/index.ts)、[`config.ts`](../../packages/database/customer-service-database/src/config.ts)、[`catalog.ts`](../../packages/database/customer-service-database/src/catalog.ts)、[`compiler.ts`](../../packages/database/customer-service-database/src/compiler.ts) 和 [`mysql.ts`](../../packages/database/customer-service-database/src/mysql.ts)。

## 模型可见工作流

`search_business_schema` 使用模型提供的词语搜索经审核的表和字段目录。它的结果是结构策略，而不是当前客户事实。`query_business_data` 只接受结构化的选择、关联、过滤、排序和行数上限。它不接受原始 SQL、数据库或连接名称，也不接受门店、租户、操作员和会员身份值。

两步设计把语义选择留给 Agent，同时让授权和 SQL 构造保持确定。插件和产品 Skill 中都不存在固定的“客户问题到表”映射。

## 请求作用域与配置

客服 HTTP 集成为每个已核验请求挂载一次插件。`storeId`、`operatorUid`、`merchantProfileVerified`、可选的 `memberMobile` 和产品代码来自可信传输层。在每次实时查询之前，插件都会在主数据库中检查当前操作员与门店关系，并从该行解析租户。模型无法替换这些值。

每个产品 Skill 都在被 Git 忽略的 `runtime/data-access.local.json` 中保存其部署本地连接目录，该文件由受跟踪的示例创建。此文件只命名经审核的连接和执行限制。加载器会拒绝不支持的产品、符号链接逃逸、无效连接选项、重叠的财务路由、可写策略和超出强制安全限制的配置。

## 目录与编译器

受跟踪的 JSONL 目录是一份允许列表。每张表声明逻辑数据源、业务语义、租户/门店作用域列、字段、允许的用法和聚合。关系显式授权等值关联。编译器最多接受四个关联、十六个选择字段、十六个过滤条件、四个排序字段和二十行结果；部署策略可以进一步降低这些限制。

标识符只来自经校验的目录项。过滤值会变为位置参数。服务端所有的值来源包括当前会员手机号、操作员 uid、未认领会员标记、门店日期和门店时间。每个表别名都会获得其声明的门店和租户谓词，因此关联无法默默逃离已核验的请求作用域。

## 只读执行与证据

MySQL 执行会打开显式的只读事务，运行一条编译后的 `SELECT`，然后回滚。取消会销毁活动连接，查询超时受到限制，返回字段和行数受到限制，字符串会清理并截断，二进制或不支持的值会被隐藏，且序列化结果具有配置的最大大小。

成功结果只是该次当前只读查询在已核验产品、门店和租户作用域内的证据。它不能证明写入、提交、支付、通知或其他下游业务效果已成功。
