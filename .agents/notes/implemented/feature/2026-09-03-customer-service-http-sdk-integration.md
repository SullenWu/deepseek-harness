# Agent Note: Customer-service HTTP SDK integration

Status: implemented

English | [中文](2026-09-03-customer-service-http-sdk-integration.zh.md)

## Problem

An enterprise-chat adapter needs a synchronous HTTP entry point into a full Harness turn. The adapter must not choose retrieval queries, tools, evidence, replies, follow-up questions, or handoff outcomes.

## Decision

The repository carries a deployment integration under `integrations/customer-service-api`. Its HTTP process accepts transported message facts, starts `dsh --profile sdk` through the Python SDK, mounts a customer-service patch, waits for the complete turn, and returns the model-owned `answer`, `ask`, or `handoff` result.

Each request starts one runtime process with request-specific MCP headers. Requests are serialized while they share one Harness home and session store. A stable caller `conversationId` becomes the SDK `sessionId`; on first use in each runtime, the SDK server resumes an existing persisted session or creates it when absent. Resume requires the stored session `cwd` to match the SDK initialization `cwd`, so an identifier cannot silently attach to history from another workspace.

The profile exposes product skills, read-only workspace tools, one `Asia/Shanghai` time-context provider, and exactly one business-data source selected at process startup. `ApiMcp` publishes the brokered capability pair; `Database` publishes reviewed-schema discovery and structured read-only query tools. It removes coding, background-job, subagent, workflow, web, and mutation-oriented tools from the customer-service composition. The adapter redacts recognized member mobile numbers recursively from model-visible message and context values while retaining the current raw message only for trusted request-local data binding. The final model response is an exact three-field JSON object; missing, additional, or malformed fields fail the HTTP request instead of being discarded or moving customer-service judgment into the adapter.

The source tree keeps reviewed product skill bundles under `integrations/customer-service-api/skills`. `DCS_SKILL_DIR` selects that directory or its deployed equivalent, and the profile disables default skill roots so repository-maintenance and user-local skills cannot enter a customer-service session. The Windows release archive creates an empty `skills` directory; deployment must provision the reviewed bundles separately.

The MCP client capability broker owns the configured `search_capabilities` and `invoke_capability` pair. Search remains globally visible, while invoke is registered only in the searching Agent scope after a valid candidate result. The broker removes `capabilityToken` from model-visible output, retains it in the Agent-scoped generation, derives the invoke JSON schema from the returned candidate argument schemas, and injects the token at execution. Objects are the declared `arguments` and optional `references` interfaces; one string containing a JSON object is decoded once as a compatibility fallback for either field. Persistent conversation history does not extend Agent-scoped tool authority into the next request.

The database plugin keeps query reasoning in the Harness Agent. `search_business_schema` searches the reviewed product catalog without fixed question-to-table routing, and `query_business_data` accepts a structured plan rather than SQL or identity scope. The plugin revalidates the trusted transport's operator/store membership for every query, resolves the live tenant, injects store and tenant predicates for every table alias, compiles one parameterized `SELECT`, chooses only the configured main database or deterministic tenant shard, executes inside a read-only transaction, and returns bounded business fields without SQL or credentials. The two source modes are mutually exclusive and do not fall back to each other inside a request.

Model route selection, endpoint, credential, context and output limits, reasoning effort, provider timeout, business-data mode, API-MCP endpoint and failure limits, and Database catalog limit live in one server-local JSON file. DuckAI never receives those fields. Product-specific read-only database connections and query policy remain in each skill's ignored data-access file. The repository tracks empty-key examples and ignores the real files; one optional environment variable only relocates the server-local JSON file.

A Windows-native release builder assembles the customer-service integration into one versioned ZIP. It builds the official `node24-win-x64` executables and both Python wheels, downloads binary Python dependency closures for CPython 3.10 through 3.14 x64, and emits offline installer and launcher scripts. The launcher points `DCS_DSH_BIN` at the visible release `runtime` executable. Executable PowerShell files contain ASCII only so Windows PowerShell 5.1 does not reinterpret UTF-8 source text using a legacy code page. The archive excludes the ignored real model configuration and includes build metadata and per-file SHA-256 hashes.

## Alternatives considered

**Embed customer-service decisions in DuckAI.** This keeps the existing split where the channel service chooses tools and validates evidence. It was rejected because Harness must own the complete customer-service investigation.

**Keep one long-lived runtime with mutable MCP headers.** The shipped MCP client configuration owns process-level headers, so mutating them per HTTP request risks cross-conversation state. Per-request processes give each turn an isolated configuration until a session-scoped MCP context exists.

**Use the webhook subsystem.** Webhooks acknowledge admission without waiting for idle or returning the assistant result, so they cannot provide this synchronous response API.

**Teach relative dates and capability tokens through a skill prompt.** Prompt instructions cannot supply a trustworthy current clock, enforce object schemas, or prevent secrets from entering model-visible history. Runtime context and the tool bridge own those facts instead.

**Publish the raw invoke tool before search.** This would require the model to copy opaque tokens, choose unbounded tool ids, and reconstruct nested argument objects from prose. Candidate-scoped registration keeps these protocol mechanics out of the model's task.

**Allow arbitrary model-authored SQL.** SQL validation after generation cannot reliably reconstruct the reviewed field, relation, and tenant policy. A structured plan preserves model choice while making every identifier, value source, relation, and scope predicate mechanically enforceable.

## Consequences

The integration proves the end-to-end ownership split without changing the agent loop or SDK protocol. In API-MCP mode, the model receives candidate-specific object schemas while capability tokens remain absent from model input, model-authored tool arguments, and durable search results. In Database mode, the model receives a reviewed schema subset while connections, tenant routing, compiled SQL, and injected identity values stay outside model context. A new valid non-empty MCP search replaces only that Agent's prior invoke schema and token; a valid zero-candidate search removes them without becoming a technical failure. Agent disposal, MCP re-sync, reconnect exhaustion, plugin disposal, and the next request process also remove the scoped invoke tool. The string-object fallback is intentionally one level deep and rejects arrays, scalars, malformed JSON, unknown invoke fields, and stale candidate ids before contacting MCP. The SDK server now distinguishes persisted resume from new-session creation, so complete runtime restarts preserve conversation history without treating an existing session as a gateway failure. The profile instructs the model to treat the current customer message as the active objective, minimize retrieval, require request-local object/property/value/scope-or-time evidence for private facts, and never turn these rules into question-specific routing. Process startup and serialized execution add latency and cap throughput; production hardening can replace this deployment adapter only after preserving request-specific tool context and durable session continuation. The first deployment has no built-in HTTP authentication or TLS and is limited to raster image attachments supported by the SDK protocol. Operators must provision the ignored model and database files separately on every server and keep their read permissions scoped to the Harness service account.

Windows release construction remains host-native because the runtime contains Windows native modules. A macOS checkout can edit and review the release definition but cannot produce the supported Windows artifact. Destination servers need only a supported x64 Python runtime; they do not need Node.js, pnpm, or network access for installation.
