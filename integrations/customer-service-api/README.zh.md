# 客服 API 集成

[English](README.md) | 中文

此集成通过 `POST /v1/customer-service/run` 对外提供一个 DeepSeek Harness 轮次。调用方传输企业聊天消息、上下文、图像和可选 API-MCP 请求头。Harness 负责加载 skill、检索、选择和调用业务数据工具、解读证据、追问、回答以及决定是否转人工。

该服务使用 Python SDK 配合 [`customer-service.cordis.patch.yml`](customer-service.cordis.patch.yml) 启动受支持的 `dsh --profile sdk` 运行时。每个 HTTP 请求独占一个运行时进程，因此该请求的 MCP 请求头不会泄漏到其他请求。由于所有进程共享一个 Harness 主目录和持久会话存储，服务会串行执行；复用 `conversationId` 会继续该 Harness 会话。

## 配置

在启动服务前，将已跟踪的模型模板复制到 Git 忽略的服务器本地文件，并填写其内容：

```sh
cp integrations/customer-service-api/customer-service.model.example.json \
  integrations/customer-service-api/customer-service.model.json
```

该 JSON 文件保存此集成使用的完整模型和业务数据源设置：

| 字段 | 用途 |
| --- | --- |
| `provider` | Harness 提供方路由。此 profile 要求使用 `qwen-standard-cn`。 |
| `model` | Harness 运行时公布并选择的模型 ID。 |
| `displayName` | 适配器目录中的人类可读模型名称。 |
| `baseUrl` | 通义千问 OpenAI 兼容端点。 |
| `apiKey` | 服务器本地的模型凭据。Git 会忽略实际文件。 |
| `businessDataMode` | 只能选择一项业务数据源：`Database` 或 `ApiMcp`。 |
| `apiMcpUrl` | `ApiMcp` 模式使用的可流式 HTTP 端点。 |
| `apiMcpToolCallTimeoutMilliseconds` | 单次 API-MCP 工具调用超时，范围为 1,000 至 300,000 毫秒。 |
| `apiMcpFailOnStartupError` | API-MCP 连接失败时是否阻止 Harness 运行时启动。 |
| `databaseMaxCatalogTables` | 单次 Database 结构检索最多返回的表摘要数量，范围为 1 至 20。 |
| `contextWindow` | 已声明的模型上下文窗口。 |
| `maxOutputTokens` | 已声明的模型最大输出量。 |
| `reasoningEffort` | 每次运行的推理强度：`low`、`medium`、`high` 或 `null`。 |
| `requestMaxTokens` | 单次客服请求的根 agent 输出上限，或者为 `null`。 |
| `timeoutMilliseconds` | 提供方请求超时时间。 |

服务启动时会拒绝缺失、未知、空、不受支持或非正数的配置值。它绝不会在 HTTP 响应或对象表示中返回 API 密钥。

在启动服务前设置以下基础设施环境变量：

| 变量 | 用途 |
| --- | --- |
| `DCS_DSH_HOME` | 包含 profile 和持久会话的隔离 Harness 主目录。必填。 |
| `DCS_SKILL_DIR` | 目录，其直接子目录是包含 `SKILL.md` 的产品 skill 组合包。必填。 |
| `DCS_WORKSPACE` | 只读文件工具可访问的工作区。默认为 `DCS_SKILL_DIR`。 |
| `DCS_MODEL_CONFIG_FILE` | 可选的模型 JSON 路径。默认为服务器旁边的 `customer-service.model.json`。 |
| `DCS_DSH_BIN` | `dsh` 可执行文件。源码检出默认使用 `apps/cli/lib/bin.js`。 |
| `DCS_NODE_BIN_DIR` | 当 `dsh` 可执行文件使用 Node shebang 时，在 `PATH` 前追加的可选 Node.js bin 目录。 |
| `DCS_HOST`, `DCS_PORT` | HTTP 监听器。默认为 `127.0.0.1:8765`。 |

安装 Python SDK 依赖项后，运行源码集成：

```sh
PYTHONPATH=python/sdk/src python integrations/customer-service-api/server.py
```

`GET /health/live` 检查 HTTP 进程。它不会调用模型或 MCP 服务器。

### 选择一项业务数据源

在 `customer-service.model.json` 中设置 `businessDataMode` 及对应的数据源参数。`ApiMcp` 使用 `apiMcpUrl`、`apiMcpToolCallTimeoutMilliseconds` 和 `apiMcpFailOnStartupError`，并且只挂载 `search_capabilities` 和 `invoke_capability`。`Database` 使用 `databaseMaxCatalogTables`，并且只挂载 `search_business_schema` 和 `query_business_data`。profile 绝不会同时发布两组工具，也不会在请求内从一项数据源自动回退到另一项。

Database 模式加载选中产品 skill 中被 Git 忽略的 `runtime/data-access.local.json`；复制已跟踪的 `data-access.example.json`，只填写只读 MySQL 账号，并确保本地文件不进入 Git。每项请求必须携带 `context.storeId`、`context.operatorUid` 和 `context.merchantProfileVerified=true`。数据库插件会在每次结构化查询前重新核验当前操作人／门店关系，并从该实时记录解析 TenantId。模型不能通过工具参数提交 SQL、数据库名、连接名、StoreId、TenantId、UID 或手机号。

## 构建 Windows 部署组合包

从 Windows x64 源码检出中运行一键发布构建器。它要求 Windows 开发人员模式、
Node.js 24 x64、pnpm 11.7.0，以及配有 `py` 启动器的 Python 3.10 x64：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-customer-service-windows-release.ps1
```

构建器安装不可变工作区依赖项，创建两个原生 Windows 可执行文件，
构建 SDK 和运行时 wheel 包，下载离线 Python 3.10-3.14 x64 依赖闭包，
并在 `dist-customer-service-windows` 中写入一个带版本的 ZIP。归档文件会特意排除
服务器本地的 `customer-service.model.json`；目标服务器会在安装时使用空密钥
示例创建该文件。

仅当锁定文件依赖项已安装时才使用 `-SkipInstall`。仅当
`dist-exe` 中已存在当前恰好两个 Windows 可执行文件时才使用 `-SkipRuntimeBuild`。

## 请求和响应

调用方发送传输事实；它不发送预期使用的工具、答案或证据结论。

```json
{
  "conversationId": "opaque-conversation-id",
  "messageId": "wecom-message-id",
  "message": "会员卡为什么看不到？",
  "productCode": "kxm_pc",
  "entryPoint": "merchant",
  "context": {
    "storeId": 12,
    "operatorUid": 34,
    "merchantProfileVerified": true
  },
  "mcp": {
    "callerId": "duckai",
    "conversationId": "mcp-conversation-id",
    "perspective": "merchant",
    "secureContext": "base64url-json",
    "serviceKey": ""
  },
  "attachments": []
}
```

Harness 返回一项决策。对于 `answer` 和 `ask`，传输调用方发送 `replyText`；对于 `handoff`，调用方按固定规则执行转人工。

```json
{
  "action": "answer",
  "replyText": "……",
  "reason": "",
  "sessionId": "customer-service-v2-opaque-conversation-id",
  "traceId": "dcs_...",
  "finishReason": "completed"
}
```

适配器在构造模型输入前，会把当前消息和通道上下文中可识别的会员手机号替换为 `[已提供会员手机号]`。未脱敏的当前消息值仅供可信数据提供方在本次请求内绑定，不会写入模型可见的会话历史。模型最终负载必须且只能包含 `action`、`replyText` 和 `reason`；字段缺失或多余都会令本次运行失败，不会被静默丢弃。

持久对话只提供上下文，不提供持久工具权限。每个 HTTP 请求都会启动新运行时并取得新的工具世代。API-MCP 模式下，模型必须在当前请求内先完成搜索，受候选项约束的调用工具才会出现；先前请求的工具名、引用、令牌和结果都不能授权当前调用。当前私有事实必须来自本次请求中成功的观察，而且该观察必须绑定所声称的对象、属性、值以及适用范围或时间。无关记录或未过滤列表不能证明身份、唯一性或不存在。

SDK 接受内联 PNG、JPEG、WebP 和 GIF 图像。此集成会拒绝其他附件类型，而不是在 Harness 外部对它们进行摘要。

## 对话 episode 与保留策略

DuckAI 提供一个不透明的 `v2-<sha256>` 对话 ID，它由客服账号、
外部客户、归一化产品、门店范围和一个由 Redis 持久化的随机 episode 派生。重复
消息和重试会复用该 episode。新的企业微信入口、DuckAI 上下文的 48 小时过期、
显式结束会话或者产品／门店范围变化会创建另一个 episode。仅操作员变化
不会轮换它；API 授权仍会使用当前请求上下文重新验证。

JSONL 持久化后端不删除会话。仅对此集成的隔离
`DCS_DSH_HOME` 使用随附的清理工具。该工具默认执行试运行：

```sh
python integrations/customer-service-api/cleanup_sessions.py --older-than-days 90
```

在应用已审核的结果前停止客服 API。持久化后端没有跨进程写入者租约或删除 API，
因此必须显式确认：

```sh
python integrations/customer-service-api/cleanup_sessions.py \
  --older-than-days 90 --apply --confirm-service-stopped
```

该工具仅匹配 ID 以 `customer-service-` 开头的会话目录中的固定 Harness 日志产物；
它会拒绝文件系统根目录和用户主目录目标。绝不要用递归删除
`DCS_DSH_HOME` 替代它。

## 当前局限

- 监听器没有身份验证或 TLS。任一数据模式绑定到非回环地址时，都必须在服务前增加网络访问控制以及 TLS／身份验证网关。
- 运行会串行执行，并且每个请求都会启动一个 Harness 运行时进程。首个功能部署优先保证请求隔离，而不是低延迟。
- SDK 协议接受光栅图像，但不接受 PDF、音频或视频提示词块。
- `health/live` 仅能证明 HTTP 进程正在监听。必须执行一次真实运行，才能验证模型、skill 目录和 MCP 端点。
- 当前检出尚未完成 Database 模式的生产数据库验收；本地测试在不使用凭据的情况下覆盖目录校验与 SQL 编译。
