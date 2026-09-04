/**
 * Tool bridge: discovers MCP tools, registers them on the harness ToolRuntime
 * under deterministic server-qualified public names, and handles re-sync when
 * the server's tool list changes.
 *
 * Naming contract (see the mcp-client Agent Note "Naming invariants"): every MCP tool
 * has the stable identity `(serverName, rawName)`; the model-facing public name
 * is `mcp__<serverName>__<rawName>`, normalized to the DeepSeek function-name
 * constraints. The raw name is only ever sent on the wire (`tools/call`); the
 * public name is never parsed to recover it.
 *
 * @module
 */

import { createHash } from 'node:crypto'
import { isDeepStrictEqual } from 'node:util'
import type { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { ListToolsResultSchema } from '@modelcontextprotocol/sdk/types.js'
import { z } from 'zod'
import type { Context } from '@deepseek-ai/cordis'
import { isImageAdmissionError } from '@deepseek-ai/dsh-attachment'
import type { AttachmentStore, ImageAttachmentRef, ImageMediaType, SaveImageAttachment } from '@deepseek-ai/dsh-attachment'
import type { ContentBlock } from '@deepseek-ai/dsh-llm'
import type { ToolDefinition, ToolExecution, ToolExecutionResult } from '@deepseek-ai/dsh-tools'
import { assertSupportedJsonSchema } from '@deepseek-ai/dsh-tools'
import type { JsonSchemaNode } from '@deepseek-ai/dsh-tools'
import type { JsonValue } from '@deepseek-ai/dsh-util-values'
import type { CapabilityBrokerConfig } from './index.ts'

/** Resolved options relevant to tool bridging. */
export interface ToolBridgeOptions {
  /** Optional paired search/invoke protocol with host-owned capability tokens. */
  capabilityBroker?: CapabilityBrokerConfig
  /** Whether a registry conflict is contained or rejects this synchronization. */
  registrationFailure: 'contain' | 'throw'
  serverName: string
  toolCallTimeoutMs: number
}

/** State for one sync generation: the current set of disposers keyed by public name. */
export type ToolDisposers = Map<string, () => void>

/** Canonical MCP result exposed to PTC mode without discarding protocol blocks. */
export type McpResult<Structured extends JsonValue = JsonValue> = {
  content: JsonValue[]
  structuredContent?: Structured
}

/**
 * DeepSeek function-name contract: at most 64 characters. Wire-protocol
 * constant, not configuration.
 */
const MAX_PUBLIC_NAME_LENGTH = 64

/** DeepSeek function-name contract: only `[A-Za-z0-9_-]` is allowed. */
const INVALID_NAME_CHARS = /[^A-Za-z0-9_-]/g

/** Hex chars of the SHA-256 identity hash appended on lossy normalization. */
const HASH_LENGTH = 12

/** Raw result record: the bridge owns JSON-value validation after transport. */
const RawCallToolResultSchema = z.record(z.string(), z.unknown())

/** Raster formats supported by the durable attachment vocabulary. */
const IMAGE_MEDIA_TYPES: readonly ImageMediaType[] = [
  'image/png',
  'image/jpeg',
  'image/webp',
  'image/gif',
]

/** Canonical RFC 4648 base64, excluding whitespace and URL-safe aliases. */
const CANONICAL_BASE64 = /^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/

/** List without mutating the SDK's per-page output-validator cache. */
function listToolsUncached(client: Client, cursor?: string) {
  return client.request(
    { method: 'tools/list', ...cursor === undefined ? {} : { params: { cursor } } },
    ListToolsResultSchema,
  )
}

/** Call without the SDK pre-validating an output schema the bridge may not support. */
function callToolUncached(
  client: Client,
  rawName: string,
  args: Record<string, unknown>,
  exec: ToolExecution,
  opts: ToolBridgeOptions,
) {
  return client.request(
    { method: 'tools/call', params: { name: rawName, arguments: args } },
    RawCallToolResultSchema,
    {
      signal: exec.signal,
      timeout: opts.toolCallTimeoutMs,
    },
  )
}

/**
 * Derive the model-facing public name for one MCP tool.
 *
 * Deterministic pure function of `(serverName, rawName)`: the clean case is
 * `mcp__<serverName>__<rawName>` verbatim. When character replacement or
 * truncation to the DeepSeek function-name contract (64 chars,
 * `[A-Za-z0-9_-]`) changes the name, a 12-hex-char SHA-256 hash of the
 * identity is appended so distinct MCP identities never collapse into the
 * same public name.
 *
 * @param serverName - Stable local namespace from plugin config.
 * @param rawName - The MCP server's own tool name.
 * @returns The globally unique, model-facing ToolRuntime name.
 */
export function publicToolName(serverName: string, rawName: string): string {
  const joined = `mcp__${serverName}__${rawName}`
  const normalized = joined.replace(INVALID_NAME_CHARS, '_')
  if (normalized === joined && normalized.length <= MAX_PUBLIC_NAME_LENGTH) return normalized
  const hash = createHash('sha256').update(`${serverName}\0${rawName}`).digest('hex').slice(0, HASH_LENGTH)
  return `${normalized.slice(0, MAX_PUBLIC_NAME_LENGTH - HASH_LENGTH - 1)}_${hash}`
}

/**
 * Sync the MCP server's tool list into the harness ToolRuntime.
 *
 * Two phases keep the swap safe:
 *
 * 1. Fetch: drain uncached `tools/list` pagination and build the full next
 *    generation of `ToolDefinition`s under public names. Any failure here
 *    (network error, duplicate raw name in the server's list) rejects and
 *    leaves the previous generation registered untouched.
 * 2. Swap: dispose the previous generation, register the new one. A registry
 *    conflict here can only mean a foreign registration squats on this
 *    server's `mcp__<serverName>__` namespace — the partial generation is
 *    rolled back (zero tools from this server) and logged. Initial strict
 *    synchronization may propagate the conflict so its parent transaction
 *    rejects; ordinary clients and later re-syncs return an empty map.
 *
 * @param client - Connected MCP Client instance used to list and call tools.
 * @param ctx - Cordis context providing the `tools` service for registration.
 * @param opts - Bridge options: server namespace and per-call timeout.
 * @param previous - Disposer map from the prior sync generation; disposed
 *   during the swap phase (only after the fetch phase succeeded).
 * @returns A map of registered public tool names to their unregister
 *   disposers — the exact set of live registrations owned by this server.
 */
export async function syncTools(
  client: Client,
  ctx: Context,
  opts: ToolBridgeOptions,
  previous: ToolDisposers,
): Promise<ToolDisposers> {
  // Phase 1: fetch and build the next generation without touching the registry.
  const listedTools: ListedTool[] = []
  const publicNames = new Set<string>()
  let cursor: string | undefined
  do {
    const response = await listToolsUncached(client, cursor)
    for (const tool of response.tools) {
      const publicName = publicToolName(opts.serverName, tool.name)
      if (publicNames.has(publicName)) {
        throw new Error(
          `mcp-client(${opts.serverName}): server listed tool "${tool.name}" more than once — invalid tool list`,
        )
      }
      publicNames.add(publicName)
      listedTools.push(tool as ListedTool)
    }
    cursor = response.nextCursor
  } while (cursor)

  const broker = opts.capabilityBroker === undefined
    ? undefined
    : createCapabilityBroker(client, ctx, opts, listedTools, opts.capabilityBroker)
  const definitions = new Map<string, ToolDefinition>()
  for (const tool of listedTools) {
    if (broker?.skipsInitialRegistration(tool.name)) continue
    const publicName = publicToolName(opts.serverName, tool.name)
    const adapter = broker?.adapterFor(tool.name)
    definitions.set(publicName, createDefinition(
      client,
      ctx,
      publicName,
      tool.name,
      tool.description ?? '',
      tool.inputSchema,
      adapter?.suppressOutputSchema === true ? undefined : supportedOutputSchema(tool.outputSchema),
      tool.execution?.taskSupport === 'required',
      opts,
      adapter,
    ))
  }

  // Phase 2: swap generations.
  for (const dispose of previous.values()) dispose()
  const disposers: ToolDisposers = new Map()
  try {
    for (const [publicName, definition] of definitions) {
      disposers.set(publicName, ctx.tools.register(definition))
    }
    if (broker !== undefined) disposers.set('\0capability-broker', () => { broker.dispose() })
  } catch (error) {
    // A conflict on an `mcp__<serverName>__`-qualified name means a foreign
    // registration occupies this server's namespace. Roll back so the model
    // sees either the full generation or none of it — never a partial set.
    for (const dispose of disposers.values()) dispose()
    broker?.dispose()
    ctx.logger.error(`mcp-client(${opts.serverName}): tool registration failed, no tools registered: ${String(error)}`)
    if (opts.registrationFailure === 'throw') throw error
    return new Map()
  }
  return disposers
}

/**
 * The shape we read from each MCP content block. Intentionally looser than the
 * SDK's `ContentBlock` type: we're at a network trust boundary (data arrives
 * from an external MCP server process via JSON-RPC), so fields that the SDK
 * declares required may be absent at runtime if the server is buggy.
 */
interface McpContentBlock {
  type: string
  text?: string
  mimeType?: string
  data?: string
  name?: string
  uri?: string
}

/** Async rich projection staged for one exact ToolRuntime execution. */
interface PreparedProjection {
  /** Canonical MCP value returned by execute before registry materialization. */
  value: McpResult
  /** Synchronous output.render projection expected before finalization. */
  fallback: ContentBlock[]
  /** Image-enriched or explicit-refusal projection prepared during execute. */
  content: ContentBlock[]
}

/** One MCP tool-list entry retained until the complete generation is available. */
interface ListedTool {
  name: string
  description?: string
  inputSchema: Record<string, unknown>
  outputSchema?: Record<string, unknown>
  execution?: { taskSupport?: 'optional' | 'required' | 'forbidden' }
}

/** Candidate fields required by the optional search/invoke broker protocol. */
interface CapabilityCandidate {
  capability?: string
  toolId: string
  argumentSchema: Record<string, unknown>
}

/** Execution hooks owned by a model-facing wrapper around one raw MCP tool. */
interface ToolExecutionAdapter {
  prepareArguments?(args: unknown, exec: ToolExecution): Record<string, unknown>
  /** Whether transformed results intentionally omit fields from the server output schema. */
  suppressOutputSchema?: true
  transformResult?(value: McpResult, exec: ToolExecution): McpResult
}

/** One generation of the optional host-owned search/invoke protocol. */
interface CapabilityBrokerGeneration {
  adapterFor(rawName: string): ToolExecutionAdapter | undefined
  skipsInitialRegistration(rawName: string): boolean
  dispose(): void
}

/** Keep a supported advertised schema; unsupported MCP vocabulary falls back to JsonValue. */
function supportedOutputSchema(candidate: unknown): JsonSchemaNode | undefined {
  if (candidate === undefined) return undefined
  try {
    assertSupportedJsonSchema(candidate)
    return candidate
  } catch {
    return undefined
  }
}

/** Whether an unknown value is a non-array object suitable for MCP arguments. */
function isUnknownRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

/** Remove a nullable type arm while preserving the server's object annotations and properties. */
function objectOnlySchema(candidate: unknown): Record<string, unknown> {
  if (!isUnknownRecord(candidate)) {
    return { type: 'object', properties: {}, additionalProperties: false }
  }
  const normalized: Record<string, unknown> = { ...candidate, type: 'object' }
  if (normalized.default === null) delete normalized.default
  return normalized
}

/** Build a candidate-bound invoke schema without exposing the trusted token field. */
function brokeredInvokeSchema(
  invokeSchema: Record<string, unknown>,
  candidates: readonly CapabilityCandidate[],
): Record<string, unknown> {
  const rawProperties = isUnknownRecord(invokeSchema.properties) ? invokeSchema.properties : {}
  const rawToolId = isUnknownRecord(rawProperties.toolId) ? rawProperties.toolId : {}
  const references = {
    ...objectOnlySchema(rawProperties.references),
    description: 'Opaque references returned by earlier capability results.',
  }
  const variants = candidates.map((candidate): Record<string, unknown> => ({
    type: 'object',
    properties: {
      toolId: {
        ...rawToolId,
        type: 'string',
        const: candidate.toolId,
        ...candidate.capability === undefined ? {} : { description: candidate.capability },
      },
      arguments: objectOnlySchema(candidate.argumentSchema),
      references,
    },
    required: ['toolId', 'arguments'],
    additionalProperties: false,
  }))
  const only = variants[0]
  if (variants.length === 1 && only !== undefined) return only
  return { oneOf: variants }
}

/** Parse and validate the broker fields returned inside one text content block. */
function parseCapabilitySearch(value: McpResult, rawName: string): {
  candidates: CapabilityCandidate[]
  sanitized: McpResult
  token?: string
} {
  const index = value.content.findIndex(block => isRecord(block) && block.type === 'text' && typeof block.text === 'string')
  const block = value.content[index]
  if (!isUnknownRecord(block) || typeof block.text !== 'string') {
    throw new Error(`CAPABILITY_BROKER_RESULT_INVALID: ${rawName} returned no JSON text block`)
  }
  let parsed: unknown
  try {
    parsed = JSON.parse(block.text)
  } catch {
    throw new Error(`CAPABILITY_BROKER_RESULT_INVALID: ${rawName} returned invalid JSON`)
  }
  if (!isUnknownRecord(parsed) || !Array.isArray(parsed.candidates)) {
    throw new Error(`CAPABILITY_BROKER_RESULT_INVALID: ${rawName} omitted candidates`)
  }
  const candidates: CapabilityCandidate[] = []
  const toolIds = new Set<string>()
  for (const candidate of parsed.candidates) {
    if (!isUnknownRecord(candidate) || typeof candidate.toolId !== 'string' || candidate.toolId.length === 0
      || !isUnknownRecord(candidate.argumentSchema)) {
      throw new Error(`CAPABILITY_BROKER_RESULT_INVALID: ${rawName} returned a malformed candidate`)
    }
    if (toolIds.has(candidate.toolId)) {
      throw new Error(`CAPABILITY_BROKER_RESULT_INVALID: ${rawName} returned duplicate toolId ${JSON.stringify(candidate.toolId)}`)
    }
    toolIds.add(candidate.toolId)
    candidates.push({
      toolId: candidate.toolId,
      argumentSchema: candidate.argumentSchema,
      ...typeof candidate.capability === 'string' ? { capability: candidate.capability } : {},
    })
  }
  const token = parsed.capabilityToken
  if (candidates.length > 0 && (typeof token !== 'string' || token.length === 0)) {
    throw new Error(`CAPABILITY_BROKER_RESULT_INVALID: ${rawName} omitted capabilityToken for non-empty candidates`)
  }
  if (token !== undefined && typeof token !== 'string') {
    throw new Error(`CAPABILITY_BROKER_RESULT_INVALID: ${rawName} returned a malformed capabilityToken`)
  }
  const { capabilityToken: _token, ...safePayload } = parsed
  const content = [...value.content]
  content[index] = { ...block, text: JSON.stringify(safePayload) }
  const structuredContent = isUnknownRecord(value.structuredContent)
    ? Object.fromEntries(Object.entries(value.structuredContent).filter(([key]) => key !== 'capabilityToken')) as JsonValue
    : value.structuredContent
  return {
    candidates,
    ...typeof token === 'string' && token.length > 0 ? { token } : {},
    sanitized: {
      content,
      ...structuredContent === undefined ? {} : { structuredContent },
    },
  }
}

/** Convert one broker field's compatibility string into an object without recursive decoding. */
function normalizeBrokerObject(
  value: unknown,
  field: 'arguments' | 'references',
  ctx: Context,
  opts: ToolBridgeOptions,
  toolId: string,
): Record<string, unknown> {
  if (isUnknownRecord(value)) return value
  if (typeof value !== 'string') {
    throw new Error(`INVALID_TOOL_ARGUMENTS: ${field} must be a JSON object`)
  }
  let parsed: unknown
  try {
    parsed = JSON.parse(value)
  } catch {
    throw new Error(`INVALID_TOOL_ARGUMENTS: ${field} string must contain valid JSON`)
  }
  if (!isUnknownRecord(parsed)) {
    throw new Error(`INVALID_TOOL_ARGUMENTS: ${field} string must contain one JSON object`)
  }
  ctx.logger.warn(`mcp-client(${opts.serverName}): normalized stringified ${field} for ${toolId}`)
  return parsed
}

/** Prepare one brokered invocation and inject only the token captured from its search. */
function prepareBrokerInvocation(
  args: unknown,
  token: string,
  candidates: ReadonlyMap<string, CapabilityCandidate>,
  ctx: Context,
  opts: ToolBridgeOptions,
): Record<string, unknown> {
  if (!isUnknownRecord(args)) throw new Error('INVALID_TOOL_ARGUMENTS: invoke arguments must be a JSON object')
  const extra = Object.keys(args).filter(key => !['toolId', 'arguments', 'references'].includes(key))
  if (extra.length > 0) {
    throw new Error(`INVALID_TOOL_ARGUMENTS: unsupported invoke fields ${extra.map(key => JSON.stringify(key)).join(', ')}`)
  }
  const toolId = args.toolId
  if (typeof toolId !== 'string' || !candidates.has(toolId)) {
    throw new Error('INVALID_TOOL_ARGUMENTS: toolId must name one candidate from the latest search')
  }
  const ordinaryArguments = normalizeBrokerObject(args.arguments, 'arguments', ctx, opts, toolId)
  const references = args.references === undefined || args.references === null
    ? undefined
    : normalizeBrokerObject(args.references, 'references', ctx, opts, toolId)
  return {
    toolId,
    capabilityToken: token,
    arguments: ordinaryArguments,
    ...references === undefined ? {} : { references },
  }
}

/** Create one generation-local search/invoke broker after complete tool discovery. */
function createCapabilityBroker(
  client: Client,
  ctx: Context,
  opts: ToolBridgeOptions,
  tools: readonly ListedTool[],
  config: CapabilityBrokerConfig,
): CapabilityBrokerGeneration {
  if (config.searchToolName === config.invokeToolName) {
    throw new Error(`mcp-client(${opts.serverName}): capabilityBroker tool names must be distinct`)
  }
  const search = tools.find(tool => tool.name === config.searchToolName)
  const invoke = tools.find(tool => tool.name === config.invokeToolName)
  if (search === undefined || invoke === undefined) {
    throw new Error(
      `mcp-client(${opts.serverName}): capabilityBroker requires tools ${JSON.stringify(config.searchToolName)} and ${JSON.stringify(config.invokeToolName)}`,
    )
  }
  const scopedDisposers = new Map<object, () => void>()
  let disposed = false

  const replaceInvoke = (token: string | undefined, candidates: CapabilityCandidate[], exec: ToolExecution): void => {
    const agent = exec.agent
    if (agent === undefined) throw new Error('CAPABILITY_BROKER_AGENT_REQUIRED: search must run for an Agent')
    scopedDisposers.get(agent)?.()
    if (disposed) throw new Error('CAPABILITY_BROKER_UNAVAILABLE: MCP generation was disposed')
    if (candidates.length === 0) return
    const trustedToken = token as string
    const byToolId = new Map(candidates.map(candidate => [candidate.toolId, candidate]))
    const definition = createDefinition(
      client,
      ctx,
      publicToolName(opts.serverName, invoke.name),
      invoke.name,
      invoke.description ?? '',
      brokeredInvokeSchema(invoke.inputSchema, candidates),
      supportedOutputSchema(invoke.outputSchema),
      invoke.execution?.taskSupport === 'required',
      opts,
      {
        prepareArguments: args => prepareBrokerInvocation(args, trustedToken, byToolId, ctx, opts),
      },
    )
    const unregister = agent.ctx.tools.register(definition)
    const forgetScopeEffect = agent.ctx.effect(() => () => {
      scopedDisposers.delete(agent)
    }, 'mcp-client capability broker scope cleanup')
    const dispose = (): void => {
      void forgetScopeEffect()
      unregister()
      scopedDisposers.delete(agent)
    }
    scopedDisposers.set(agent, dispose)
  }

  return {
    skipsInitialRegistration: rawName => rawName === invoke.name,
    adapterFor(rawName) {
      if (rawName !== search.name) return undefined
      return {
        suppressOutputSchema: true,
        transformResult(value, exec) {
          const parsed = parseCapabilitySearch(value, search.name)
          replaceInvoke(parsed.token, parsed.candidates, exec)
          return parsed.sanitized
        },
      }
    },
    dispose() {
      if (disposed) return
      disposed = true
      for (const dispose of [...scopedDisposers.values()]) dispose()
      scopedDisposers.clear()
    },
  }
}

/**
 * Build one generation-local tool definition and its execution-local rich projections.
 * @param client - connected MCP client used for calls.
 * @param ctx - plugin context carrying optional attachment and model services.
 * @param publicName - registry-qualified public tool name.
 * @param rawName - MCP wire tool name.
 * @param description - model-facing tool description.
 * @param parameters - MCP input schema.
 * @param structuredSchema - supported structured-output schema, when advertised.
 * @param taskRequired - whether this MCP tool requires unsupported task execution.
 * @param opts - bridge timeout and namespace options.
 * @param adapter - optional model/wire argument and result adapter.
 * @returns a complete ToolRuntime definition.
 */
function createDefinition(
  client: Client,
  ctx: Context,
  publicName: string,
  rawName: string,
  description: string,
  parameters: Record<string, unknown>,
  structuredSchema: JsonSchemaNode | undefined,
  taskRequired: boolean,
  opts: ToolBridgeOptions,
  adapter?: ToolExecutionAdapter,
): ToolDefinition {
  const projections = new WeakMap<ToolExecution, PreparedProjection>()
  return {
    name: publicName,
    description,
    parameters,
    output: createOutput(rawName, structuredSchema),
    execute: createExecutor(client, ctx, rawName, taskRequired, opts, projections, adapter),
    finalizeContent(exec: Readonly<ToolExecution>, result: Readonly<ToolExecutionResult>) {
      const projection = projections.get(exec)
      if (projection === undefined) return undefined
      projections.delete(exec)
      if (result.isError) return undefined
      if (!isDeepStrictEqual(result.value, projection.value)) return undefined
      if (!isDeepStrictEqual(result.content, projection.fallback)) return undefined
      return projection.content
    },
  }
}

/** Build the canonical result schema and existing Native text projection. */
function createOutput(rawName: string, structuredSchema: JsonSchemaNode | undefined): ToolDefinition['output'] {
  return {
    schema: {
      type: 'object',
      properties: {
        content: { type: 'array', items: {} },
        structuredContent: structuredSchema ?? {},
      },
      required: structuredSchema === undefined ? ['content'] : ['content', 'structuredContent'],
      additionalProperties: false,
    },
    render(_args: unknown, value: JsonValue) {
      const result = value as unknown as McpResult
      return [{ type: 'text', text: extractText(result.content, rawName) }]
    },
  }
}

/**
 * Create an execute function for one MCP tool. The executor closes over the
 * raw MCP tool name and sends an uncached `tools/call` request with it (never
 * the public name), with abort signal and timeout, then maps the result to
 * harness ContentBlocks. Owning the raw request prevents the SDK's internal
 * per-page schema cache from pre-validating a different contract.
 *
 * When the MCP server returns `isError: true`, the executor throws so that
 * the ToolRuntime's catch path produces an `isError` result for the model.
 */
function createExecutor(
  client: Client,
  ctx: Context,
  rawName: string,
  taskRequired: boolean,
  opts: ToolBridgeOptions,
  projections: WeakMap<ToolExecution, PreparedProjection>,
  adapter?: ToolExecutionAdapter,
): ToolDefinition['execute'] {
  return async (args: unknown, exec: ToolExecution) => {
    if (taskRequired) {
      throw new Error(`Tool "${rawName}" requires task-based execution, which this bridge does not support`)
    }
    // The agent loop passes `JSON.parse(model_arguments)` which is usually an
    // object, but can be any JSON value if the model misbehaves (outputs a bare
    // string/number/null). Fallback to {} lets the MCP server produce a
    // specific "missing required param" error the model can learn from.
    const argsObj = adapter?.prepareArguments?.(args, exec)
      ?? (typeof args === 'object' && args !== null ? args : {}) as Record<string, unknown>
    const result = await callToolUncached(client, rawName, argsObj, exec, opts)

    // The SDK may return a legacy `toolResult` shape; normalize to content array.
    let value: McpResult
    if (!Array.isArray(result.content)) {
      const rendered: unknown = 'toolResult' in result
        ? JSON.stringify(result.toolResult)
        : '(no output)'
      const text = typeof rendered === 'string' ? rendered : '(no output)'
      if (result.isError === true) throw new Error(text)
      value = {
        content: [{ type: 'text', text }],
        ...result.structuredContent !== undefined
          ? { structuredContent: result.structuredContent as JsonValue }
          : {},
      }
    } else {
      // Trust boundary: the SDK's return type erases to `any[]` due to the
      // union of CallToolResult | CompatibilityCallToolResult; extractText
      // validates each element.
      const content = result.content as unknown as JsonValue[]
      const text = extractText(content, rawName)

      // MCP isError → throw so ToolRuntime produces an isError result for the model.
      if (result.isError === true) {
        throw new Error(text)
      }

      value = {
        content,
        ...result.structuredContent !== undefined
          ? { structuredContent: result.structuredContent as JsonValue }
          : {},
      }
    }
    value = adapter?.transformResult?.(value, exec) ?? value
    if (containsImage(value.content)) {
      const fallback: ContentBlock[] = [{ type: 'text', text: extractText(value.content, rawName) }]
      const projected = await prepareImageProjection(ctx, exec, value.content, rawName)
      projections.set(exec, { value, fallback, content: projected })
    }
    return value
  }
}

/** Whether an untrusted MCP content array contains a declared image block. */
function containsImage(content: JsonValue[]): boolean {
  return content.some(value => isRecord(value) && value.type === 'image')
}

/** Narrow one JSON value to a string-keyed object. */
function isRecord(value: JsonValue): value is { [key: string]: JsonValue } {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

/** Narrow a declared MIME string to the durable image vocabulary. */
function isImageMediaType(value: string): value is ImageMediaType {
  return IMAGE_MEDIA_TYPES.includes(value as ImageMediaType)
}

/** Decode one untrusted MCP image block without accepting base64 aliases. */
function decodeImage(block: McpContentBlock): SaveImageAttachment {
  if (block.mimeType === undefined || !isImageMediaType(block.mimeType)) {
    throw new Error('the declared media type is not PNG, JPEG, WebP, or GIF')
  }
  if (block.data === undefined || !CANONICAL_BASE64.test(block.data)) {
    throw new Error('the image data is not canonical base64')
  }
  const data = Buffer.from(block.data, 'base64')
  if (data.toString('base64') !== block.data) {
    throw new Error('the image data is not canonical base64')
  }
  return { data, mediaType: block.mimeType }
}

/**
 * Resolve the active model route and durable store for an image-bearing result.
 * @param ctx - plugin context with optional services.
 * @param exec - exact tool execution whose agent supplies the latest route.
 * @returns the attachment store after exact positive image-capability proof.
 */
async function resolveImageAdmission(ctx: Context, exec: ToolExecution): Promise<AttachmentStore> {
  const attachments = ctx.get('attachments')
  if (attachments === undefined) throw new Error('no attachment store is mounted')
  const routed = exec.agent?.session.requestHeader()?.config
  const provider = routed?.provider ?? exec.agent?.options.provider
  const model = routed?.model ?? exec.agent?.options.model
  const llm = ctx.get('llm')
  if (provider === undefined || model === undefined || llm === undefined) {
    throw new Error('the current model route could not be resolved')
  }
  let info: Awaited<ReturnType<typeof llm.resolveModelInfo>>
  try {
    info = await llm.resolveModelInfo(provider, model, exec.signal)
  } catch {
    throw new Error('the current model route could not be verified')
  }
  if (info.inputModalities === undefined || !info.inputModalities.includes('image')) {
    throw new Error(`model "${model}" does not declare image input`)
  }
  if (exec.signal.aborted) throw new Error('the tool call was canceled before image storage')
  return attachments
}

/** Stable diagnostic text for an image block that was not admitted. */
function imageDiagnostic(block: McpContentBlock, reason: string): string {
  const mediaType = block.mimeType ?? 'unknown media type'
  return `[image unavailable: ${mediaType}; ${reason}; raw image data remains available to programmatic callers]`
}

/**
 * Decode, preflight, and durably save one MCP result's ordered image batch.
 * Any refusal projects every image as text while retaining the canonical raw
 * value for programmatic callers.
 */
async function prepareImageProjection(
  ctx: Context,
  exec: ToolExecution,
  content: JsonValue[],
  toolName: string,
): Promise<ContentBlock[]> {
  const decoded: SaveImageAttachment[] = []
  const validationErrors = new Map<number, string>()
  const imageIndexes: number[] = []
  for (const [index, value] of content.entries()) {
    if (!isRecord(value) || value.type !== 'image') continue
    imageIndexes.push(index)
    try {
      decoded.push(decodeImage(value as unknown as McpContentBlock))
    } catch (error: unknown) {
      // decodeImage owns every throw above and always produces Error.
      validationErrors.set(index, (error as Error).message)
    }
  }
  if (validationErrors.size > 0) {
    return projectContent(content, toolName, (block, index) => ({
      type: 'text',
      text: imageDiagnostic(
        block,
        validationErrors.get(index) ?? 'another image in the same result was invalid',
      ),
    }))
  }

  let attachments: AttachmentStore
  try {
    attachments = await resolveImageAdmission(ctx, exec)
  } catch (error: unknown) {
    // resolveImageAdmission contains provider failures and throws Error only.
    const reason = (error as Error).message
    return projectContent(content, toolName, block => ({ type: 'text', text: imageDiagnostic(block, reason) }))
  }

  try {
    const refs = await attachments.saveImages(decoded)
    const byIndex = new Map(imageIndexes.map((index, offset) => [index, refs[offset] as ImageAttachmentRef] as const))
    return projectContent(content, toolName, (_block, index) => ({
      type: 'image',
      attachment: byIndex.get(index) as ImageAttachmentRef,
    }))
  } catch (error: unknown) {
    const reason = isImageAdmissionError(error)
      ? `image admission rejected the result: ${error.message}`
      : 'durable image storage rejected the result'
    return projectContent(content, toolName, block => ({
      type: 'text',
      text: imageDiagnostic(block, reason),
    }))
  }
}

/**
 * Extract text from an MCP content array into a single string.
 * - text blocks: join with '\n'
 * - image/audio/resource blocks: replaced with a placeholder
 *
 * Defensive: fields that the MCP spec declares required (mimeType, text) are
 * guarded with fallbacks because this is a network trust boundary.
 */
function extractText(mcpContent: JsonValue[], toolName: string): string {
  const content = projectContent(mcpContent, toolName)
  // The default image projector below also returns text, so this local call
  // cannot produce a core image block.
  return content.map(block => (block as Extract<ContentBlock, { type: 'text' }>).text).join('\n')
}

/**
 * Project ordered MCP blocks into the core content vocabulary.
 * Text-like runs are newline-coalesced; admitted images split those runs at
 * their original position.
 */
function projectContent(
  mcpContent: JsonValue[],
  toolName: string,
  image: (block: McpContentBlock, index: number) => ContentBlock = block => ({
    type: 'text',
    text: imageDiagnostic(block, 'this result was not admitted to durable model context'),
  }),
): ContentBlock[] {
  const projected: ContentBlock[] = []
  const text: string[] = []
  const flushText = (): void => {
    if (text.length === 0) return
    projected.push({ type: 'text', text: text.splice(0).join('\n') })
  }

  for (const [index, value] of mcpContent.entries()) {
    if (!isRecord(value)) {
      text.push('[unsupported MCP content block: expected an object]')
      continue
    }
    const block = value as unknown as McpContentBlock
    switch (block.type) {
      case 'text':
        if (block.text !== undefined) text.push(block.text)
        break
      case 'image':
        flushText()
        projected.push(image(block, index))
        break
      case 'resource_link':
        if (block.name === undefined || block.uri === undefined) {
          text.push('[resource link unavailable: the MCP block is missing its name or URI]')
        } else {
          text.push(`Resource link: ${block.name} (${block.uri})`)
        }
        break
      case 'audio':
        text.push(`[audio result unsupported: ${block.mimeType ?? 'unknown media type'}; raw audio data remains available to programmatic callers]`)
        break
      case 'resource':
        text.push('[embedded resource unsupported; raw resource data remains available to programmatic callers]')
        break
      default:
        text.push(`[unsupported MCP content type: ${block.type}]`)
    }
  }
  flushText()
  return projected.length > 0
    ? projected
    : [{ type: 'text', text: `(${toolName} returned no model-visible content)` }]
}
