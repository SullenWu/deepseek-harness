/** MySQL provider for live scope validation and one read-only compiled SELECT. */

import mysql, { type Connection, type ConnectionOptions, type RowDataPacket } from 'mysql2/promise'
import type { CompiledQuery } from './types.ts'

/** Live identity and tenancy facts resolved from the main database. */
export interface VerifiedDatabaseScope {
  /** Current store id. */
  storeId: number
  /** Current tenant id. */
  tenantId: number
  /** Current operator uid. */
  operatorUid: number
  /** Store UTC offset in hours. */
  utcOffsetHours: number
}

async function withConnection<T>(
  options: ConnectionOptions,
  signal: AbortSignal,
  run: (connection: Connection) => Promise<T>,
): Promise<T> {
  if (signal.aborted) throw new Error('database call aborted before connection')
  const connection = await mysql.createConnection(options)
  const abort = (): void => {
    connection.destroy()
  }
  signal.addEventListener('abort', abort, { once: true })
  try {
    return await run(connection)
  } finally {
    signal.removeEventListener('abort', abort)
    await connection.end().catch(() => undefined)
  }
}

/**
 * Revalidate the trusted transport's operator/store relationship for every query.
 * @param options - Main MySQL connection options.
 * @param operatorUid - Transport-verified operator id.
 * @param storeId - Transport-verified store id.
 * @param timeoutMs - Query timeout.
 * @param signal - Tool cancellation signal.
 * @returns Exactly one current tenant/store/operator scope.
 */
export async function verifyDatabaseScope(
  options: ConnectionOptions,
  operatorUid: number,
  storeId: number,
  timeoutMs: number,
  signal: AbortSignal,
): Promise<VerifiedDatabaseScope> {
  return withConnection(options, signal, async (connection) => {
    const [rows] = await connection.query<RowDataPacket[]>({
      sql: `SELECT staff.user_id AS operatorUid,
                   store.id AS storeId,
                   store.tenant_id AS tenantId,
                   COALESCE(NULLIF(setting.time_zone, 0), 8) AS utcOffsetHours
            FROM tenant_user AS staff
            INNER JOIN users AS account
                    ON account.id = staff.user_id AND account.state = 1
            INNER JOIN store
                    ON store.id = staff.store_id AND store.state = 1
            LEFT JOIN store_custom_seting AS setting
                   ON setting.store_id = store.id AND setting.tenant_id = store.tenant_id
            WHERE staff.user_id = ?
              AND staff.store_id = ?
              AND staff.state = 1
            LIMIT 2`,
      values: [operatorUid, storeId],
      timeout: timeoutMs,
    })
    if (rows.length !== 1) throw new Error('current operator and store relationship is missing or ambiguous')
    const row = rows[0]
    if (row === undefined) throw new Error('current operator and store relationship disappeared')
    const tenantId = Number(row.tenantId)
    const resolvedStoreId = Number(row.storeId)
    const resolvedOperatorUid = Number(row.operatorUid)
    let utcOffsetHours = Number(row.utcOffsetHours)
    if (!Number.isFinite(utcOffsetHours) || utcOffsetHours < -12 || utcOffsetHours > 14) utcOffsetHours = 8
    if (tenantId < 1 || resolvedStoreId !== storeId || resolvedOperatorUid !== operatorUid) {
      throw new Error('current database scope is invalid')
    }
    return { tenantId, storeId, operatorUid, utcOffsetHours }
  })
}

function normalizeCell(value: unknown): string | number | boolean | null {
  if (value === null || value === undefined) return null
  if (Buffer.isBuffer(value)) return '[binary value hidden]'
  if (value instanceof Date) return value.toISOString().replace('T', ' ').replace(/\.\d{3}Z$/u, '')
  if (typeof value === 'string') {
    const normalized = value.replace(/[\u0000-\u001f\u007f]/gu, ' ')
    return normalized.length <= 300 ? normalized : normalized.slice(0, 300)
  }
  if (typeof value === 'number' || typeof value === 'boolean') return value
  if (typeof value === 'bigint') return value.toString()
  return '[unsupported value hidden]'
}

/**
 * Execute one compiled SELECT inside an explicit read-only transaction.
 * @param options - Selected MySQL connection options.
 * @param compiled - Catalog-constrained SELECT.
 * @param timeoutMs - Query timeout.
 * @param signal - Tool cancellation signal.
 * @returns Normalized model-safe rows.
 */
export async function executeReadOnly(
  options: ConnectionOptions,
  compiled: CompiledQuery,
  timeoutMs: number,
  signal: AbortSignal,
): Promise<Array<Record<string, string | number | boolean | null>>> {
  return withConnection(options, signal, async (connection) => {
    await connection.query({ sql: 'START TRANSACTION READ ONLY', timeout: timeoutMs })
    try {
      const [rows] = await connection.query<RowDataPacket[]>({
        sql: compiled.sql,
        values: compiled.parameters,
        timeout: timeoutMs,
        rowsAsArray: false,
      })
      return rows.map(row => Object.fromEntries(
        Object.entries(row).map(([key, value]) => [key, normalizeCell(value)]),
      ))
    } finally {
      await connection.query({ sql: 'ROLLBACK', timeout: timeoutMs }).catch(() => undefined)
    }
  })
}
