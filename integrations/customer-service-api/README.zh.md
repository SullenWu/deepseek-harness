# 客服 API 集成

[English](README.md) | 中文

此集成通过 `POST /v1/customer-service/run` 对外提供一个 DeepSeek Harness 轮次。调用方传输企业聊天消息、上下文、图像和 MCP 请求头。Harness 负责加载 skill、检索、选择和调用 MCP、解读证据、追问、回答以及决定是否转人工。

该服务使用 Python SDK 配合 [`customer-service.cordis.patch.yml`](customer-service.cordis.patch.yml) 启动受支持的 `dsh --profile sdk` 运行时。每个 HTTP 请求独占一个运行时进程，因此该请求的 MCP 请求头不会泄漏到其他请求。由于所有进程共享一个 Harness 主目录和持久会话存储，服务会串行执行；复用 `conversationId` 会继续该 Harness 会话。

## 配置

在启动服务前，将已跟踪的模型模板复制到 Git 忽略的服务器本地文件，并填写其内容：

```sh
cp integrations/customer-service-api/customer-service.model.example.json \
  integrations/customer-service-api/customer-service.model.json
```

该 JSON 文件保存此集成使用的完整模型选择：

| 字段 | 用途 |
| --- | --- |
| `provider` | Harness 提供方路由。此 profile 要求使用 `qwen-standard-cn`。 |
| `model` | Harness 运行时公布并选择的模型 ID。 |
| `displayName` | 适配器目录中的人类可读模型名称。 |
| `baseUrl` | 通义千问 OpenAI 兼容端点。 |
| `apiKey` | 服务器本地的模型凭据。Git 会忽略实际文件。 |
| `contextWindow` | 已声明的模型上下文窗口。 |
| `maxOutputTokens` | 已声明的模型最大输出量。 |
| `reasoningEffort` | 每次运行的推理强度：`low`、`medium`、`high` 或 `null`。 |
| `requestMaxTokens` | 单次客服请求的根 agent 输出上限，或者为 `null`。 |
| `timeoutMilliseconds` | 提供方请求超时时间。 |

服务启动时会拒绝缺失、未知、空、不受支持或非正数的模型值。它绝不会在 HTTP 响应或对象表示中返回 API 密钥。

在启动服务前设置以下基础设施环境变量：

| 变量 | 用途 |
| --- | --- |
| `DCS_DSH_HOME` | 包含 profile 和持久会话的隔离 Harness 主目录。必填。 |
| `DCS_SKILL_DIR` | 目录，其直接子目录是包含 `SKILL.md` 的产品 skill 组合包。必填。 |
| `DCS_WORKSPACE` | 只读文件工具可访问的工作区。默认为 `DCS_SKILL_DIR`。 |
| `DCS_MCP_URL` | 客服 MCP 服务器的可流式 HTTP 端点。默认为 `http://127.0.0.1:5301/mcp`。 |
| `DCS_MODEL_CONFIG_FILE` | 可选的模型 JSON 路径。默认为服务器旁边的 `customer-service.model.json`。 |
| `DCS_DSH_BIN` | `dsh` 可执行文件。源码检出默认使用 `apps/cli/lib/bin.js`。 |
| `DCS_NODE_BIN_DIR` | 当 `dsh` 可执行文件使用 Node shebang 时，在 `PATH` 前追加的可选 Node.js bin 目录。 |
| `DCS_HOST`, `DCS_PORT` | HTTP 监听器。默认为 `127.0.0.1:8765`。 |

安装 Python SDK 依赖项后，运行源码集成：

```sh
PYTHONPATH=python/sdk/src python integrations/customer-service-api/server.py
```

`GET /health/live` 检查 HTTP 进程。它不会调用模型或 MCP 服务器。

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
    "operatorUid": 34
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

- 监听器没有身份验证或 TLS。验证功能流程时，请将它绑定到回环地址或测试网络。
- 运行会串行执行，并且每个请求都会启动一个 Harness 运行时进程。首个功能部署优先保证请求隔离，而不是低延迟。
- SDK 协议接受光栅图像，但不接受 PDF、音频或视频提示词块。
- `health/live` 仅能证明 HTTP 进程正在监听。必须执行一次真实运行，才能验证模型、skill 目录和 MCP 端点。
