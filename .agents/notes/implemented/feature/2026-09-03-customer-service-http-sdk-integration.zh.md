# Agent Note: 客服 HTTP SDK 集成

Status: implemented

[English](2026-09-03-customer-service-http-sdk-integration.md) | 中文

## Problem

企业聊天适配器需要一个同步 HTTP 入口来执行完整 Harness 轮次。适配器不能选择检索查询、工具、证据、回复、追问或转人工结果。

## Decision

仓库在 `integrations/customer-service-api` 提供部署集成。其 HTTP 进程接收通道转发的消息事实，通过 Python SDK 启动 `dsh --profile sdk`，挂载客服 patch，等待完整轮次结束，并返回模型决定的 `answer`、`ask` 或 `handoff` 结果。

每个请求使用请求专属的 MCP 请求头启动一个运行时进程。共享同一 Harness home 和会话存储时，请求串行执行。调用方持续使用的 `conversationId` 会成为 SDK `sessionId`；每个运行时首次使用该标识时，SDK 服务器会恢复已有持久会话，或在会话不存在时创建。恢复要求已存会话的 `cwd` 与 SDK 初始化 `cwd` 一致，因此同一标识不会静默接入其他工作区的历史。

该 profile 暴露产品 skill、只读工作区工具、一个 `Asia/Shanghai` 时间上下文提供方和一个 Streamable HTTP MCP 服务。客服组合不提供编码、后台任务、子 Agent、工作流、Web 和面向修改的工具。模型最终响应必须是严格的三字段 JSON 对象；格式错误会令 HTTP 请求失败，适配器不会接管客服判断。

MCP 客户端 capability broker 管理配置的 `search_capabilities` 与 `invoke_capability` 工具对。搜索工具保持全局可见；只有返回有效候选结果后，调用工具才注册到执行搜索的 Agent 作用域。Broker 从模型可见输出中移除 `capabilityToken`，在 Agent 作用域世代内保留令牌，根据返回候选项的参数 schema 生成调用 JSON schema，并在执行时注入令牌。对象参数是声明接口；包含一个 JSON 对象的字符串仅作为兼容兜底解码。传输层继续直接传递客户消息和上下文，不引入主体引用存储。

模型路由选择、端点、凭据、上下文与输出上限、推理强度和供应方超时统一保存在服务器本地 JSON 文件中。DuckAI 不接收这些字段。仓库只跟踪密钥为空的示例并忽略真实文件；唯一可选环境变量只负责改变该文件的位置。

Windows 原生发布脚本会把客服集成组装为一个带版本号的 ZIP。它构建官方 `node24-win-x64` 两个 EXE 和两个 Python wheel，下载 CPython 3.10 至 3.14 x64 的二进制依赖闭包，并生成离线安装与启动脚本。启动脚本把 `DCS_DSH_BIN` 明确指向发布包中可见的 `runtime` 主程序。所有可执行 PowerShell 文件只使用 ASCII 字符，避免 Windows PowerShell 5.1 按旧代码页错误解析 UTF-8 源码。压缩包排除被忽略的真实模型配置，同时包含构建信息和逐文件 SHA-256 校验值。

## Alternatives considered

**在 DuckAI 中保留客服决策。** 这会继续由通道服务选择工具和校验证据。此方案被拒绝，因为完整的客服调查必须由 Harness 负责。

**使用一个长期运行且可变更 MCP 请求头的运行时。** 当前 MCP 客户端配置持有进程级请求头，因此按 HTTP 请求修改可能导致不同会话共享状态。在具备会话级 MCP 上下文之前，每次请求独立启动进程可以隔离每轮配置。

**使用 webhook 子系统。** Webhook 在请求进入后即返回，不等待 Agent 空闲，也不返回助手结果，因此无法提供这个同步响应 API。

**通过 skill 提示词教授相对日期与 capability token。** 提示词无法提供可信的当前时钟、强制对象 schema，也无法阻止秘密进入模型可见历史。这些事实改由运行时上下文和工具桥接层管理。

**在搜索前发布原始调用工具。** 这会要求模型复制不透明令牌、选择无约束工具 id，并从说明文字重建嵌套参数对象。按候选项限定的作用域注册让这些协议机制不再成为模型任务。

## Consequences

该集成无需修改 Agent Loop 或 SDK 协议，即可验证端到端职责划分。模型会收到明确的当前时钟和候选项专属对象 schema，capability token 则不会进入模型输入、模型生成的工具参数或持久搜索结果。新的有效非空搜索只替换该 Agent 之前的调用 schema 与令牌；合法的零候选搜索会移除它们，但不会变成技术失败。Agent dispose、MCP 重新同步、重连预算耗尽和插件 dispose 也会移除作用域调用工具。字符串对象兜底有意只解码一层，并会在联系 MCP 前拒绝数组、标量、格式错误的 JSON、未知调用字段和过期候选 id。SDK 服务器现在会区分持久会话恢复与新会话创建，因此完整重启运行时后仍能保留对话历史，不再把已有会话当作网关故障。进程启动和串行执行会增加延迟并限制吞吐量；生产加固只有在保留请求级 MCP 上下文和持久会话续接后才能替换此部署适配器。首版部署不内置 HTTP 身份验证或 TLS，附件仅支持 SDK 协议可接收的栅格图片。运维人员必须在每台服务器单独提供被忽略的模型文件，并把读取权限限制给 Harness 服务账号。

因为运行时包含 Windows 原生模块，所以发布包仍必须在 Windows 主机上构建。macOS 工作副本可以编辑和检查发布定义，但不能产出受支持的 Windows 构件。目标服务器只需要受支持的 x64 Python，不需要 Node.js、pnpm 或联网安装依赖。
