/** Request-local plugin composition without a live database connection. */

import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { Context } from '@deepseek-ai/cordis'
import SystemPrompt from '@deepseek-ai/dsh-system-prompt'
import ToolRuntime from '@deepseek-ai/dsh-tools'
import { describe, expect, it } from 'vitest'
import * as CustomerServiceDatabase from '../src/index.ts'

function skillFixture(): string {
  const root = mkdtempSync(join(tmpdir(), 'dsh-customer-database-'))
  const skill = join(root, 'kexiaomi-product-agent')
  const runtime = join(skill, 'runtime')
  const catalog = join(skill, 'references', 'database')
  mkdirSync(runtime, { recursive: true })
  mkdirSync(catalog, { recursive: true })
  writeFileSync(join(runtime, 'data-access.local.json'), JSON.stringify({
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
  writeFileSync(join(catalog, 'database-agent-query-catalog.jsonl'), `${JSON.stringify({
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
  writeFileSync(join(catalog, 'database-agent-query-relations.jsonl'), '')
  return root
}

describe('customer-service-database plugin', () => {
  it('publishes only schema search and structured query tools', async () => {
    const ctx = new Context()
    await ctx.plugin(SystemPrompt)
    await ctx.plugin(ToolRuntime)
    await ctx.plugin(CustomerServiceDatabase, {
      skillRoot: skillFixture(),
      productCode: 'kxm_pc',
      storeId: 12,
      operatorUid: 34,
      merchantProfileVerified: true,
    })

    expect(ctx.tools.schemas().map(schema => schema.name).sort()).toEqual([
      'query_business_data',
      'search_business_schema',
    ])
  })

  it('rejects an unverified merchant profile before reading database config', async () => {
    const ctx = new Context()
    await ctx.plugin(SystemPrompt)
    await ctx.plugin(ToolRuntime)
    await expect(ctx.plugin(CustomerServiceDatabase, {
      skillRoot: '/does/not/matter',
      productCode: 'kxm_pc',
      storeId: 12,
      operatorUid: 34,
      merchantProfileVerified: false,
    })).rejects.toThrow(/verified merchant/u)
  })
})
