# Customer-service API integration

This integration exposes one DeepSeek Harness turn through `POST /v1/customer-service/run`. The caller transports enterprise-chat messages, context, images, and MCP headers. Harness owns skill loading, retrieval, MCP selection and calls, evidence interpretation, follow-up questions, answers, and handoff decisions.

The service uses the Python SDK to start the supported `dsh --profile sdk` runtime with [`customer-service.cordis.patch.yml`](customer-service.cordis.patch.yml). Each HTTP request owns one runtime process so its MCP headers cannot leak into another request. The service serializes runs because all processes share one Harness home and durable session store; reusing `conversationId` continues that Harness session.

## Configuration

Copy the tracked model template to the ignored server-local file and fill it before starting the service:

```sh
cp integrations/customer-service-api/customer-service.model.example.json \
  integrations/customer-service-api/customer-service.model.json
```

The JSON file owns the complete model selection used by this integration:

| Field | Purpose |
| --- | --- |
| `provider` | Harness provider route. This profile currently requires `qwen-standard-cn`. |
| `model` | Model id advertised to and selected by the Harness runtime. |
| `displayName` | Human-readable model name in the adapter catalog. |
| `baseUrl` | Qwen OpenAI-compatible endpoint. |
| `apiKey` | Server-local model credential. The real file is ignored by Git. |
| `contextWindow` | Declared model context window. |
| `maxOutputTokens` | Declared maximum model output. |
| `reasoningEffort` | Per-run reasoning effort: `low`, `medium`, `high`, or `null`. |
| `requestMaxTokens` | Root-agent output cap for one customer-service request, or `null`. |
| `timeoutMilliseconds` | Provider request timeout. |

The service rejects missing, unknown, empty, unsupported, or non-positive model values during startup. It never returns the API key in an HTTP response or object representation.

Set these infrastructure environment variables before starting the service:

| Variable | Purpose |
| --- | --- |
| `DCS_DSH_HOME` | Isolated Harness home containing profiles and durable sessions. Required. |
| `DCS_SKILL_DIR` | Directory whose direct children are product skill bundles containing `SKILL.md`. Required. |
| `DCS_WORKSPACE` | Workspace available to the read-only file tools. Defaults to `DCS_SKILL_DIR`. |
| `DCS_MCP_URL` | Streamable HTTP endpoint for the customer-service MCP server. Defaults to `http://127.0.0.1:5301/mcp`. |
| `DCS_MODEL_CONFIG_FILE` | Optional model JSON path. Defaults to `customer-service.model.json` beside the server. |
| `DCS_DSH_BIN` | `dsh` executable. Source checkouts default to `apps/cli/lib/bin.js`. |
| `DCS_NODE_BIN_DIR` | Optional Node.js bin directory prepended to `PATH` when the `dsh` executable uses a Node shebang. |
| `DCS_HOST`, `DCS_PORT` | HTTP listener. Defaults to `127.0.0.1:8765`. |

Run the source integration with the Python SDK dependencies installed:

```sh
PYTHONPATH=python/sdk/src python integrations/customer-service-api/server.py
```

`GET /health/live` checks the HTTP process. It does not call the model or MCP server.

## Build a Windows deployment bundle

Run the one-click release builder from a Windows x64 checkout. It requires Windows Developer Mode,
Node.js 24 x64, pnpm 11.7.0, and Python 3.10 x64 with the `py` launcher:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-customer-service-windows-release.ps1
```

The builder installs immutable workspace dependencies, creates the two native Windows executables,
builds the SDK and runtime wheels, downloads the offline Python 3.10-3.14 x64 dependency closure,
and writes one versioned ZIP under `dist-customer-service-windows`. The archive deliberately omits
the server-local `customer-service.model.json`; the destination server creates it from the empty-key
example during installation.

Use `-SkipInstall` only when the lockfile dependencies are already installed. Use
`-SkipRuntimeBuild` only when the exact two current Windows executables already exist in `dist-exe`.

## Request and response

The caller sends transport facts; it does not send an intended tool, answer, or evidence conclusion.

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

Harness returns one decision. The transport caller sends `replyText` for `answer` and `ask`, or mechanically performs the handoff for `handoff`.

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

The SDK accepts inline PNG, JPEG, WebP, and GIF images. This integration rejects other attachment types instead of summarizing them outside Harness.

## Conversation episodes and retention

DuckAI supplies an opaque `v2-<sha256>` conversation id derived from the customer-service account,
external customer, normalized product, store scope, and one Redis-persisted random episode. Repeated
messages and retries reuse the episode. A new WeCom entry, the 48-hour DuckAI context expiring, an
explicit session end, or a product/store scope change creates another episode. Operator changes alone
do not rotate it; API authorization is still revalidated from the current request context.

The JSONL persistence backend does not delete sessions. Use the bundled cleanup tool only against this
integration's isolated `DCS_DSH_HOME`. It defaults to a dry-run:

```sh
python integrations/customer-service-api/cleanup_sessions.py --older-than-days 90
```

Stop the customer-service API before applying the reviewed result. The explicit confirmation is required
because the persistence backend has no cross-process writer lease or deletion API:

```sh
python integrations/customer-service-api/cleanup_sessions.py \
  --older-than-days 90 --apply --confirm-service-stopped
```

The tool only matches fixed Harness log artifacts inside session directories whose ids start with
`customer-service-`; it refuses filesystem roots and user-home targets. Never replace it with a recursive
removal of `DCS_DSH_HOME`.

## Current limitations

- The listener has no authentication or TLS. Bind it to loopback or a test network while proving the functional flow.
- Runs are serialized and start one Harness runtime process per request. This favors request isolation over latency for the first functional deployment.
- The SDK protocol accepts raster images but not PDF, audio, or video prompt blocks.
- `health/live` proves only that the HTTP process is listening. A real run is required to verify the model, skill directory, and MCP endpoint.
