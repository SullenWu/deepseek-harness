/** Real Loader composition for the model-visible customer-service database tools. */

import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'
import { afterEach, describe, expect, it } from 'vitest'
import { Context } from '@deepseek-ai/cordis'
import Include from '@deepseek-ai/cordis-plugin-include'
import Loader from '@deepseek-ai/cordis-plugin-loader'
import SystemPrompt from '@deepseek-ai/dsh-system-prompt'
import ToolRuntime from '@deepseek-ai/dsh-tools'
import * as CustomerServiceDatabase from '../src/index.ts'

let root: string | undefined
let context: Context | undefined

afterEach(async () => {
  await context?.fiber.dispose()
  context = undefined
  if (root !== undefined) await rm(root, { recursive: true, force: true })
  root = undefined
})

async function boot(): Promise<Context> {
  root = await mkdtemp(join(tmpdir(), 'dsh-customer-database-loader-'))
  const skillRoot = join(root, 'skills')
  const skill = join(skillRoot, 'kexiaomi-product-agent')
  const runtime = join(skill, 'runtime')
  const catalog = join(skill, 'references', 'database')
  await mkdir(runtime, { recursive: true })
  await mkdir(catalog, { recursive: true })
  await writeFile(join(runtime, 'data-access.local.json'), JSON.stringify({
    schemaVersion: 1,
    productCode: 'kexiaomi',
    mainConnectionName: 'MainReadOnly',
    connections: [{
      name: 'MainReadOnly',
      providerName: 'MySql',
      connectionString: 'Server=127.0.0.1;Database=customer_test;User Id=readonly;Password=test-only;',
    }],
    tenantRoutes: [],
    financeFallback: null,
    executionPolicy: {
      readOnly: true,
      commandTimeoutSeconds: 5,
      maxRows: 20,
      maxFields: 16,
      maxJoins: 4,
      maxSerializedCharacters: 12000,
    },
  }))
  await writeFile(join(catalog, 'database-agent-query-catalog.jsonl'), `${JSON.stringify({
    policyVersion: 2,
    scopeVersion: 2,
    dataSource: 'main',
    table: 'store_course',
    domain: 'course',
    businessGroup: 'course-schedule',
    audience: 'merchant-customer-service',
    authority: 'primary-business-source',
    fieldPolicy: 'reviewed-business-fields',
    comment: 'course',
    scopeColumns: ['store_id', 'tenant_id'],
    rowCountAggregates: ['count'],
    fields: [],
  })}\n`)
  await writeFile(join(catalog, 'database-agent-query-relations.jsonl'), '')

  const configPath = join(root, 'cordis.yml')
  await writeFile(configPath, [
    "- name: '@deepseek-ai/dsh-system-prompt'",
    "- name: '@deepseek-ai/dsh-tools'",
    "- name: '@deepseek-ai/dsh-customer-service-database'",
    '  config:',
    `    skillRoot: ${JSON.stringify(skillRoot)}`,
    '    productCode: kxm_pc',
    '    storeId: 12',
    '    operatorUid: 34',
    '    merchantProfileVerified: true',
    '',
  ].join('\n'))

  const ctx = new Context()
  context = ctx
  ctx.baseUrl = pathToFileURL(root).href + '/'
  await ctx.plugin(Loader)
  ctx.loader.builtins.include = Include
  const modules = new Map<string, unknown>([
    ['@deepseek-ai/dsh-system-prompt', SystemPrompt],
    ['@deepseek-ai/dsh-tools', ToolRuntime],
    ['@deepseek-ai/dsh-customer-service-database', CustomerServiceDatabase],
  ])
  ctx.loader.internal = {
    version: 'v2',
    async import(specifier: string) {
      if (!modules.has(specifier)) throw new Error(`unexpected Loader import: ${specifier}`)
      return modules.get(specifier)
    },
  } as unknown as NonNullable<typeof ctx.loader.internal>
  await ctx.loader.create({ name: 'cordis:include', config: { path: pathToFileURL(configPath).href } })
  await ctx.loader.await()
  return ctx
}

describe('customer-service database real Loader composition through cordis.yml', () => {
  it('preserves the namespace plugin shape and publishes only the reviewed tool pair', async () => {
    expect('default' in CustomerServiceDatabase).toBe(false)
    const ctx = await boot()

    expect(ctx.tools.schemas().map(schema => schema.name).sort()).toEqual([
      'query_business_data',
      'search_business_schema',
    ])
  }, 30_000)
})
