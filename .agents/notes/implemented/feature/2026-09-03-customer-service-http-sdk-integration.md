# Agent Note: Customer-service HTTP SDK integration

Status: implemented

English | [中文](2026-09-03-customer-service-http-sdk-integration.zh.md)

## Problem

An enterprise-chat adapter needs a synchronous HTTP entry point into a full Harness turn. The adapter must not choose retrieval queries, tools, evidence, replies, follow-up questions, or handoff outcomes.

## Decision

The repository carries a deployment integration under `integrations/customer-service-api`. Its HTTP process accepts transported message facts, starts `dsh --profile sdk` through the Python SDK, mounts a customer-service patch, waits for the complete turn, and returns the model-owned `answer`, `ask`, or `handoff` result.

Each request starts one runtime process with request-specific MCP headers. Requests are serialized while they share one Harness home and session store. A stable caller `conversationId` becomes the SDK `sessionId`; on first use in each runtime, the SDK server resumes an existing persisted session or creates it when absent. Resume requires the stored session `cwd` to match the SDK initialization `cwd`, so an identifier cannot silently attach to history from another workspace.

The profile exposes product skills, read-only workspace tools, and one Streamable HTTP MCP server. It removes coding, background-job, subagent, workflow, web, and mutation-oriented tools from the customer-service composition. The final model response is a strict three-field JSON object; malformed results fail the HTTP request instead of moving customer-service judgment into the adapter.

Model route selection, endpoint, credential, context and output limits, reasoning effort, and provider timeout live in one server-local JSON file. DuckAI never receives those fields. The repository tracks an empty-key example and ignores the real file; one optional environment variable only relocates that file.

A Windows-native release builder assembles the customer-service integration into one versioned ZIP. It builds the official `node24-win-x64` executables and both Python wheels, downloads binary Python dependency closures for CPython 3.10 through 3.14 x64, and emits offline installer and launcher scripts. The launcher points `DCS_DSH_BIN` at the visible release `runtime` executable. Executable PowerShell files contain ASCII only so Windows PowerShell 5.1 does not reinterpret UTF-8 source text using a legacy code page. The archive excludes the ignored real model configuration and includes build metadata and per-file SHA-256 hashes.

## Alternatives considered

**Embed customer-service decisions in DuckAI.** This keeps the existing split where the channel service chooses tools and validates evidence. It was rejected because Harness must own the complete customer-service investigation.

**Keep one long-lived runtime with mutable MCP headers.** The shipped MCP client configuration owns process-level headers, so mutating them per HTTP request risks cross-conversation state. Per-request processes give each turn an isolated configuration until a session-scoped MCP context exists.

**Use the webhook subsystem.** Webhooks acknowledge admission without waiting for idle or returning the assistant result, so they cannot provide this synchronous response API.

## Consequences

The integration proves the end-to-end ownership split without changing the agent loop or SDK protocol. The SDK server now distinguishes persisted resume from new-session creation, so complete runtime restarts preserve conversation history without treating an existing session as a gateway failure. Process startup and serialized execution add latency and cap throughput; production hardening can replace this deployment adapter only after preserving request-specific MCP context and durable session continuation. The first deployment has no built-in HTTP authentication or TLS and is limited to raster image attachments supported by the SDK protocol. Operators must provision the ignored model file separately on every server and keep its read permissions scoped to the Harness service account.

Windows release construction remains host-native because the runtime contains Windows native modules. A macOS checkout can edit and review the release definition but cannot produce the supported Windows artifact. Destination servers need only a supported x64 Python runtime; they do not need Node.js, pnpm, or network access for installation.
