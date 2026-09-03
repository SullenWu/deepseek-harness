# Agent Note: 客服 HTTP SDK 集成

Status: implemented

[English](2026-09-03-customer-service-http-sdk-integration.md) | 中文

## Problem

企业聊天适配器需要一个同步 HTTP 入口来执行完整 Harness 轮次。适配器不能选择检索查询、工具、证据、回复、追问或转人工结果。

## Decision

仓库在 `integrations/customer-service-api` 提供部署集成。其 HTTP 进程接收通道转发的消息事实，通过 Python SDK 启动 `dsh --profile sdk`，挂载客服 patch，等待完整轮次结束，并返回模型决定的 `answer`、`ask` 或 `handoff` 结果。

每个请求使用请求专属的 MCP 请求头启动一个运行时进程。共享同一 Harness home 和会话存储时，请求串行执行。调用方持续使用同一个 `conversationId`，即可跨运行时进程恢复同一个持久 Harness 会话。

该 profile 暴露产品 skill、只读工作区工具和一个 Streamable HTTP MCP 服务。客服组合不提供编码、后台任务、子 Agent、工作流、Web 和面向修改的工具。模型最终响应必须是严格的三字段 JSON 对象；格式错误会令 HTTP 请求失败，适配器不会接管客服判断。

模型路由选择、端点、凭据、上下文与输出上限、推理强度和供应方超时统一保存在服务器本地 JSON 文件中。DuckAI 不接收这些字段。仓库只跟踪密钥为空的示例并忽略真实文件；唯一可选环境变量只负责改变该文件的位置。

## Alternatives considered

**在 DuckAI 中保留客服决策。** 这会继续由通道服务选择工具和校验证据。此方案被拒绝，因为完整的客服调查必须由 Harness 负责。

**使用一个长期运行且可变更 MCP 请求头的运行时。** 当前 MCP 客户端配置持有进程级请求头，因此按 HTTP 请求修改可能导致不同会话共享状态。在具备会话级 MCP 上下文之前，每次请求独立启动进程可以隔离每轮配置。

**使用 webhook 子系统。** Webhook 在请求进入后即返回，不等待 Agent 空闲，也不返回助手结果，因此无法提供这个同步响应 API。

## Consequences

该集成无需修改 Agent Loop 或 SDK 协议，即可验证端到端职责划分。进程启动和串行执行会增加延迟并限制吞吐量；生产加固只有在保留请求级 MCP 上下文和持久会话续接后才能替换此部署适配器。首版部署不内置 HTTP 身份验证或 TLS，附件仅支持 SDK 协议可接收的栅格图片。运维人员必须在每台服务器单独提供被忽略的模型文件，并把读取权限限制给 Harness 服务账号。
