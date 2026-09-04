/** Live MySQL adapter behavior with a fully isolated connection double. */

import { afterEach, describe, expect, it, vi } from 'vitest'
import type { CompiledQuery } from '../src/types.ts'

const mocks = vi.hoisted(() => ({
  createConnection: vi.fn(),
}))

vi.mock('mysql2/promise', () => ({
  default: { createConnection: mocks.createConnection },
}))

import { executeReadOnly, verifyDatabaseScope } from '../src/mysql.ts'

interface ConnectionDouble {
  query: ReturnType<typeof vi.fn>
  destroy: ReturnType<typeof vi.fn>
  end: ReturnType<typeof vi.fn>
}

function connection(...queryResults: unknown[]): ConnectionDouble {
  const value = {
    query: vi.fn(),
    destroy: vi.fn(),
    end: vi.fn().mockResolvedValue(undefined),
  }
  for (const result of queryResults) value.query.mockResolvedValueOnce(result)
  mocks.createConnection.mockResolvedValueOnce(value)
  return value
}

const options = { host: '127.0.0.1', database: 'test', user: 'readonly', password: 'test' }

afterEach(() => {
  vi.clearAllMocks()
})

describe('verifyDatabaseScope', () => {
  it('rejects cancellation before acquiring a connection', async () => {
    const controller = new AbortController()
    controller.abort()

    await expect(verifyDatabaseScope(options, 34, 12, 5_000, controller.signal)).rejects.toThrow(/aborted before connection/u)
    expect(mocks.createConnection).not.toHaveBeenCalled()
  })

  it.each([
    [8, 8],
    ['invalid', 8],
    [-13, 8],
    [15, 8],
  ])('returns one verified scope and normalizes timezone %s', async (databaseOffset, expectedOffset) => {
    const client = connection([[{
      operatorUid: 34,
      storeId: 12,
      tenantId: 56,
      utcOffsetHours: databaseOffset,
    }]])

    await expect(verifyDatabaseScope(options, 34, 12, 5_000, new AbortController().signal)).resolves.toEqual({
      operatorUid: 34,
      storeId: 12,
      tenantId: 56,
      utcOffsetHours: expectedOffset,
    })
    expect(client.query).toHaveBeenCalledWith(expect.objectContaining({ values: [34, 12], timeout: 5_000 }))
    expect(client.end).toHaveBeenCalledOnce()
  })

  it.each([
    [[], /missing or ambiguous/u],
    [[{}, {}], /missing or ambiguous/u],
    [Array(1), /disappeared/u],
    [[{ operatorUid: 34, storeId: 12, tenantId: 0, utcOffsetHours: 8 }], /scope is invalid/u],
    [[{ operatorUid: 34, storeId: 13, tenantId: 56, utcOffsetHours: 8 }], /scope is invalid/u],
    [[{ operatorUid: 35, storeId: 12, tenantId: 56, utcOffsetHours: 8 }], /scope is invalid/u],
  ])('rejects invalid live scope %#', async (rows, message) => {
    connection([rows])

    await expect(verifyDatabaseScope(options, 34, 12, 5_000, new AbortController().signal)).rejects.toThrow(message)
  })

  it('destroys an acquired connection when cancellation arrives and contains end failure', async () => {
    const controller = new AbortController()
    const client = connection()
    let resolveQuery!: (value: unknown) => void
    client.query.mockReturnValueOnce(new Promise((resolve) => { resolveQuery = resolve }))
    client.end.mockRejectedValueOnce(new Error('close failed'))

    const pending = verifyDatabaseScope(options, 34, 12, 5_000, controller.signal)
    await new Promise<void>((resolve) => { setImmediate(resolve) })
    controller.abort()
    resolveQuery([[{ operatorUid: 34, storeId: 12, tenantId: 56, utcOffsetHours: 8 }]])
    await expect(pending).resolves.toMatchObject({ tenantId: 56 })
    expect(client.destroy).toHaveBeenCalledOnce()
  })
})

describe('executeReadOnly', () => {
  const compiled: CompiledQuery = {
    sql: 'SELECT value FROM safe_table WHERE store_id = ?',
    parameters: [12],
    dataSource: 'main',
    outputNames: ['value'],
    limit: 10,
  }

  it('uses a read-only transaction and normalizes every model-visible value family', async () => {
    const long = 'x'.repeat(301)
    const client = connection(
      [[], []],
      [[{
        nullValue: null,
        undefinedValue: undefined,
        bufferValue: Buffer.from('secret'),
        dateValue: new Date('2026-09-04T12:34:56.789Z'),
        shortString: 'a\u0000b',
        longString: long,
        numberValue: 3,
        booleanValue: true,
        bigintValue: 4n,
        objectValue: { hidden: true },
      }]],
      [[], []],
    )

    await expect(executeReadOnly(options, compiled, 5_000, new AbortController().signal)).resolves.toEqual([{
      nullValue: null,
      undefinedValue: null,
      bufferValue: '[binary value hidden]',
      dateValue: '2026-09-04 12:34:56',
      shortString: 'a b',
      longString: 'x'.repeat(300),
      numberValue: 3,
      booleanValue: true,
      bigintValue: '4',
      objectValue: '[unsupported value hidden]',
    }])
    expect(client.query.mock.calls[0]?.[0]).toEqual({ sql: 'START TRANSACTION READ ONLY', timeout: 5_000 })
    expect(client.query.mock.calls[1]?.[0]).toEqual({
      sql: compiled.sql,
      values: compiled.parameters,
      timeout: 5_000,
      rowsAsArray: false,
    })
    expect(client.query.mock.calls[2]?.[0]).toEqual({ sql: 'ROLLBACK', timeout: 5_000 })
  })

  it('rolls back after query failure and contains rollback failure', async () => {
    const client = connection([[], []])
    client.query
      .mockRejectedValueOnce(new Error('select failed'))
      .mockRejectedValueOnce(new Error('rollback failed'))

    await expect(executeReadOnly(options, compiled, 5_000, new AbortController().signal)).rejects.toThrow('select failed')
    expect(client.query).toHaveBeenCalledTimes(3)
  })
})
