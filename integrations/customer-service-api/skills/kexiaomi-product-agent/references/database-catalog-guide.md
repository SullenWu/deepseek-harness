# 课小秘数据库目录使用说明

数据库目录用于让产品 Agent 理解“有哪些业务事实、字段属于哪个数据域、实体怎样关联”，并由 DuckAI 本地通用编译器生成受控 SQL；目录本身不直接授予数据库权限。

## 目录文件

- `database/database-schema.jsonl`：每张表或视图一条记录，包含完整字段、类型、默认值、注释、索引、物理外键、隔离字段、敏感等级和候选查询策略。
- `database/database-dictionary.md`：同一物理目录的完整人工可读版本，体积较大，只在人工审阅具体表时打开。
- `database/database-logical-relations.jsonl`：从仓库 SQL 等值关联中提取的逻辑关系证据。旧库没有声明物理外键，因此任何关系在进入 Agent 运行白名单前仍需业务复核。
- `database/database-enums.jsonl`：从数据库字段注释提取的状态和类型枚举；标记为 `review-required` 的冲突或错误注释不能直接作为最终业务结论。
- `database/database-routing.json`：财务分库的显式区间和 `tenantId % 10` 回退规则，不包含连接地址或凭据。
- `database/database-dictionary-validation.json`：结构覆盖、实时连接结果和失败目标。`structuralCoverageComplete` 表示结构是否齐全，`liveCollectionComplete` 表示每个配置目标是否都已实时采集，二者不能混为一谈。
- `database/database-semantic-validation.json`：逻辑关系和枚举提取数量；`runtimeAuthorizationGranted` 永远为 false。
- `database-customer-service-scope.json`：人工审核的客服数据受众映射。软件订购、餐饮、商城、分销、短信和企微等商家可使用模块属于客服业务范围；内部销售运营、行为跟踪、凭据、历史副本及未归组新表默认排除。
- `database/database-agent-query-catalog.jsonl`：从物理目录和客服数据受众映射共同生成的运行字段白名单，只包含有门店/租户隔离路径、明确客服业务分组及按 `fieldPolicy` 保守筛选后的安全字段用法。
- `database/database-agent-query-relations.jsonl`：进入运行层的高置信度源码关联；关联两侧表仍会分别注入门店/租户条件。
- `database/database-query-policy-validation.json`：运行白名单计数和安全不变量，包括拒绝原始 SQL、服务端注入隔离范围和最多返回 20 行。

会员数据的实体口径和手机号解析链路见 [会员身份与持卡链路](member-card-identity-chain.md)。该链路属于业务语义约束；物理字段和关联仍必须同时存在于本轮运行查询目录中。

数据库连接、租户路由和执行策略随 Skill 部署在 `runtime/data-access.local.json`。该文件属于运行时私有配置，不是知识引用，不得进入 Agent 提示词、评测轨迹、日志或 Git；仓库只保留 `runtime/data-access.example.json`。旧配置迁移使用 `scripts/migrate_database_connections.py`，脚本只复制主库和财务分库所需连接。

## 当前覆盖边界

本次已实时采集课小秘主库 `nutbooking` 和包含 `TenantData9` 别名的财务模板库。根据运维方明确确认，`TenantData0`～`TenantData9` 只有数据库名不同、表结构完全一致，因此未实时连通的财务目标从该模板生成结构目录。结构目录已经覆盖这些分片，但每个目标的实时连接结果仍以 `database-dictionary-validation.json` 为准；模板继承不能证明目标库存在或当前可连接。

只有下列条件同时满足后，才能把某个字段或关联加入动态 SQL 运行白名单：

1. 目标数据库已实时采集，或属于运维方明确确认且通过结构指纹校验的同构分片；实际查询时目标连接仍必须可用。
2. 表具有可信 `store_id` 或 `tenant_id` 隔离路径；缺少隔离路径的全局表需要单独审核。
3. 输出字段不是 `restricted`、`sensitive-unstructured`，敏感字段只能作为服务端参数化过滤条件或经过明确脱敏。
4. 逻辑关系有实际 DAO SQL 或服务端业务代码证据，并确认没有把同名 ID 错接到其他实体。
5. 状态枚举与当前服务端规则一致；数据库注释、Model 注释和现行业务冲突时，以现行服务端规则为准并记录冲突。
6. 表已在 `database-customer-service-scope.json` 中归入商家客服业务分组；判断依据是数据是否服务当前商家业务，而不是表属于哪个技术模块。内部销售运营、行为跟踪、凭据、历史副本及尚未分类的新表一律不进入运行目录。

## 生成边界

`scripts/build_database_dictionary.py` 只查询 `information_schema` 和 `SELECT VERSION()/DATABASE()`，不读取业务行。脚本运行时可读取 Skill 私有连接配置，但生成物中不得出现主机、端口、账号、密码或完整连接串。

只有获得同构分片的明确运维确认时，才可使用 `--inherit-finance-template-on-failure`。该参数只覆盖 `TenantData0`～`TenantData9` 的结构目录，不改变实时连接失败记录，也不允许运行时回退到其他分片。

`scripts/build_database_semantics.py` 只读取生成目录和仓库源码，不连接数据库。它产生的是待审查证据，不是运行时 SQL 权限。

`scripts/build_database_query_policy.py` 从物理目录、逻辑关系和 `database-customer-service-scope.json` 生成保守运行白名单：只允许明确归入商家客服业务分组且有隔离字段的表、经分组字段策略审核的短字段、受控手机号过滤、当前操作人过滤，以及至少出现三次的高置信度源码关系。字段会显式输出 `usages` 与 `aggregates`；没有安全输出字段的已授权表只保留 `COUNT(*)`，不会因此开放具体列。表行数统计只能使用 `column="*"`、`aggregate="count"`。物理字典、关系或客服范围变化后必须重新生成，并运行 `scripts/validate_database_dictionary.py --require-complete`。
