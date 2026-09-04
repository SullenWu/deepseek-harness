#!/usr/bin/env python3
"""Generate a credential-free 课小秘 physical database dictionary from MySQL information_schema.

The script reads the product Skill's private runtime/data-access.local.json only while collecting
metadata. It never writes connection strings, hosts, users, or passwords to generated artifacts.
Main and financial targets use the same connection aliases and tenant routing as DuckAI runtime.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


DEFAULT_DATA_ACCESS_CONFIG = Path(__file__).resolve().parent.parent / "runtime" / "data-access.local.json"


def load_json(path: Path) -> dict[str, Any]:
    """Read UTF-8 or UTF-8-BOM JSON without echoing its sensitive values."""
    return json.loads(path.read_text(encoding="utf-8-sig"))


def parse_connection_string(value: str) -> dict[str, str]:
    """Parse the simple semicolon-delimited MySQL connection strings used by this repository."""
    result: dict[str, str] = {}
    for part in (value or "").split(";"):
        if "=" not in part:
            continue
        key, item_value = part.split("=", 1)
        normalized_key = re.sub(r"\s+", "", key).lower()
        result[normalized_key] = item_value.strip()
    return result


def first_value(values: dict[str, str], *keys: str, default: str = "") -> str:
    """Return the first configured connection-string synonym."""
    for key in keys:
        value = values.get(key.lower(), "")
        if value:
            return value
    return default


def normalize_connection(item: dict[str, Any]) -> dict[str, Any]:
    """Convert a configured connection into a runtime-only structure containing credentials."""
    values = parse_connection_string(str(item.get("connectionString") or ""))
    return {
        "name": str(item.get("name") or "").strip(),
        "provider": str(item.get("providerName") or "").strip(),
        "host": first_value(values, "server", "datasource", "host"),
        "port": int(first_value(values, "port", default="3306") or "3306"),
        "database": first_value(values, "database", "initialcatalog"),
        "user": first_value(values, "userid", "uid", "user", "username"),
        "password": first_value(values, "password", "pwd"),
        "charset": first_value(values, "charset", default="utf8mb4"),
        "ssl": first_value(values, "sslmode", "ssl-mode", default="Preferred"),
    }


def discover_connections(data_access: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Select Skill-declared main and financial targets, then deduplicate identical physical endpoints."""
    if int(data_access.get("schemaVersion") or 0) != 1 or data_access.get("productCode") != "kexiaomi":
        raise RuntimeError("Skill 私有数据访问配置版本或产品域无效")
    raw_connections = data_access.get("connections", [])
    if not isinstance(raw_connections, list):
        raise RuntimeError("Skill 私有数据访问配置缺少 connections")
    connections = {item["name"]: item for item in map(normalize_connection, raw_connections) if item["name"]}
    routes = data_access.get("tenantRoutes", [])
    if not isinstance(routes, list):
        raise RuntimeError("Skill 私有数据访问配置缺少 tenantRoutes")

    main_name = str(data_access.get("mainConnectionName") or "").strip()
    if main_name not in connections:
        raise RuntimeError("Skill 私有数据访问配置缺少主库连接")

    fallback = data_access.get("financeFallback")
    if not isinstance(fallback, dict):
        raise RuntimeError("Skill 私有数据访问配置缺少 financeFallback")
    modulo = int(fallback.get("modulo") or 0)
    template = str(fallback.get("connectionNameTemplate") or "")
    if modulo < 1 or modulo > 100 or "{index}" not in template:
        raise RuntimeError("Skill 私有财务分库回退规则无效")

    fallback_names = [template.replace("{index}", str(index)) for index in range(modulo)]
    financial_names = set(fallback_names)
    financial_names.update(str(item.get("connectionName") or "").strip() for item in routes)
    missing_names = sorted(name for name in financial_names if name not in connections)
    if missing_names:
        raise RuntimeError("Skill 私有数据访问配置缺少财务目标连接: " + ",".join(missing_names))
    requested_names = [main_name] + sorted(financial_names)

    # TenantData9 may intentionally point to the same physical database as TenantData. Query each
    # unique endpoint/database once while preserving all logical connection aliases in the output.
    unique: dict[tuple[str, int, str, str], dict[str, Any]] = {}
    for name in requested_names:
        item = connections[name]
        if not item["host"] or not item["database"] or not item["user"]:
            raise RuntimeError(f"连接 {name} 缺少 server、database 或 user")
        key = (item["host"].lower(), item["port"], item["database"].lower(), item["user"].lower())
        if key not in unique:
            unique[key] = {**item, "aliases": [name], "roles": []}
        elif name not in unique[key]["aliases"]:
            unique[key]["aliases"].append(name)
        unique[key]["roles"].append("main" if name == main_name else "finance-shard")

    route_payload = {
        "algorithm": [
            "优先匹配 TenantId 精确配置",
            "其次匹配 MinTenantId <= tenantId <= MaxTenantId 的区间配置",
            f"仍未命中时使用 {template}，index = tenantId % {modulo}",
        ],
        "explicitRoutes": [
            {
                "tenantId": int(item.get("tenantId") or 0),
                "minTenantId": int(item.get("minTenantId") or 0),
                "maxTenantId": int(item.get("maxTenantId") or 0),
                "connectionName": str(item.get("connectionName") or "").strip(),
            }
            for item in routes
        ],
        "fallbackConnectionNames": fallback_names,
        "physicalTargets": [
            {
                "schema": item["database"],
                "connectionAliases": sorted(item["aliases"]),
                "roles": sorted(set(item["roles"])),
            }
            for item in sorted(unique.values(), key=lambda value: ("main" not in value["roles"], value["database"]))
        ],
    }
    return list(unique.values()), route_payload


def import_mysql_driver():
    """Load PyMySQL only when live metadata extraction starts and give a deterministic setup hint."""
    try:
        import pymysql  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "缺少 PyMySQL。请在临时目录安装后通过 PYTHONPATH 运行，禁止把依赖或凭据写入 Skill。"
        ) from exc
    return pymysql


def query_rows(cursor: Any, sql: str, parameters: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    """Execute one metadata-only SELECT and normalize every row to a plain dictionary."""
    cursor.execute(sql, parameters)
    return list(cursor.fetchall())


def classify_sensitivity(column_name: str, data_type: str) -> str:
    """Assign a conservative sensitivity level from stable column-name and type signals."""
    name = column_name.lower()
    restricted = (
        "password", "passwd", "pwd", "secret", "token", "union_id", "openid", "open_id",
        "id_card", "identity_card", "bank_card", "private_key", "access_key", "session_key",
    )
    sensitive = (
        "mobile", "phone", "email", "address", "real_name", "user_name", "username",
        "contact", "account_no", "card_number", "license", "latitude", "longitude",
    )
    unstructured = ("remark", "note", "content", "payload", "request", "response", "body", "message")
    if any(marker in name for marker in restricted):
        return "restricted"
    if any(marker in name for marker in sensitive):
        return "sensitive"
    if any(marker in name for marker in unstructured) or data_type.lower() in {"blob", "longblob", "mediumblob"}:
        return "sensitive-unstructured"
    return "internal"


def infer_scope_role(column_name: str) -> str:
    """Identify fields that must come from trusted server context rather than model-generated values."""
    name = column_name.lower()
    if name == "tenant_id":
        return "tenant-scope"
    if name == "store_id":
        return "store-scope"
    if name in {"uid", "user_id", "member_id", "card_id", "staff_id"}:
        return "subject-or-relation-key"
    if name == "id" or name.endswith("_id"):
        return "relation-key"
    return "business-field"


def infer_query_policy(column: dict[str, Any]) -> str:
    """Mark catalog candidates without treating the generated dictionary as runtime authorization."""
    sensitivity = column["sensitivity"]
    scope_role = column["scopeRole"]
    data_type = column["dataType"].lower()
    if sensitivity in {"restricted", "sensitive-unstructured"}:
        return "deny"
    if scope_role in {"tenant-scope", "store-scope", "subject-or-relation-key", "relation-key"}:
        return "server-filter-only"
    if sensitivity == "sensitive":
        return "masked-or-filter-only"
    if data_type in {"blob", "longblob", "mediumblob", "binary", "varbinary"}:
        return "deny"
    return "semantic-review-required"


def infer_domain(table_name: str) -> str:
    """Provide a broad discovery domain; product semantics are enriched later from code and manuals."""
    name = table_name.lower()
    rules = (
        ("reservation-waitlist", ("reservation", "wait", "lessons", "course", "class")),
        ("member-card", ("user_card", "prepaid_card", "member", "card_")),
        ("staff-binding", ("tenant_user", "staff", "user_open_login", "coach")),
        ("payment-finance", ("consumption", "payment", "pay_", "refund", "order", "trade", "bill")),
        ("coupon-marketing", ("coupon", "integral", "marketing", "activity", "promotion")),
        ("store-configuration", ("store_", "soft_", "tenant_", "setting", "config")),
        ("audit-log", ("log_", "record", "history", "request_log")),
    )
    return next((domain for domain, markers in rules if any(marker in name for marker in markers)), "other")


def collect_schema(connection: dict[str, Any]) -> dict[str, Any]:
    """Collect structural metadata only; no business rows, samples, or credential-bearing variables are queried."""
    pymysql = import_mysql_driver()
    ssl_mode = str(connection.get("ssl") or "").lower()
    connect_kwargs: dict[str, Any] = {
        "host": connection["host"],
        "port": connection["port"],
        "user": connection["user"],
        "password": connection["password"],
        "database": connection["database"],
        "charset": connection["charset"] or "utf8mb4",
        "connect_timeout": 10,
        "read_timeout": 30,
        "write_timeout": 10,
        "autocommit": True,
        "cursorclass": pymysql.cursors.DictCursor,
    }
    if ssl_mode not in {"none", "disabled", "false", "0"}:
        connect_kwargs["ssl"] = {}

    schema_name = connection["database"]
    with pymysql.connect(**connect_kwargs) as db:
        with db.cursor() as cursor:
            server = query_rows(cursor, "SELECT VERSION() AS version, DATABASE() AS current_database")[0]
            tables = query_rows(
                cursor,
                """SELECT TABLE_NAME, TABLE_TYPE, ENGINE, TABLE_COLLATION, TABLE_COMMENT
FROM information_schema.TABLES WHERE TABLE_SCHEMA=%s ORDER BY TABLE_NAME""",
                (schema_name,),
            )
            columns = query_rows(
                cursor,
                """SELECT TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION, COLUMN_DEFAULT, IS_NULLABLE,
DATA_TYPE, COLUMN_TYPE, CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE,
DATETIME_PRECISION, CHARACTER_SET_NAME, COLLATION_NAME, COLUMN_KEY, EXTRA,
COLUMN_COMMENT, GENERATION_EXPRESSION
FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=%s
ORDER BY TABLE_NAME, ORDINAL_POSITION""",
                (schema_name,),
            )
            indexes = query_rows(
                cursor,
                """SELECT TABLE_NAME, INDEX_NAME, NON_UNIQUE, SEQ_IN_INDEX, COLUMN_NAME,
COLLATION, SUB_PART, INDEX_TYPE, INDEX_COMMENT
FROM information_schema.STATISTICS WHERE TABLE_SCHEMA=%s
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX""",
                (schema_name,),
            )
            foreign_keys = query_rows(
                cursor,
                """SELECT CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION,
REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA=%s AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME, CONSTRAINT_NAME, ORDINAL_POSITION""",
                (schema_name,),
            )
            partitions = query_rows(
                cursor,
                """SELECT TABLE_NAME, PARTITION_METHOD, SUBPARTITION_METHOD,
COUNT(*) AS PARTITION_COUNT
FROM information_schema.PARTITIONS
WHERE TABLE_SCHEMA=%s AND PARTITION_NAME IS NOT NULL
GROUP BY TABLE_NAME, PARTITION_METHOD, SUBPARTITION_METHOD
ORDER BY TABLE_NAME""",
                (schema_name,),
            )
            triggers = query_rows(
                cursor,
                """SELECT TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_TABLE, ACTION_TIMING
FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA=%s ORDER BY TRIGGER_NAME""",
                (schema_name,),
            )
            routines = query_rows(
                cursor,
                """SELECT ROUTINE_NAME, ROUTINE_TYPE, DATA_TYPE
FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA=%s ORDER BY ROUTINE_NAME""",
                (schema_name,),
            )

    columns_by_table: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in columns:
        item = {
            "name": row["COLUMN_NAME"],
            "ordinal": int(row["ORDINAL_POSITION"]),
            "dataType": row["DATA_TYPE"],
            "columnType": row["COLUMN_TYPE"],
            "nullable": row["IS_NULLABLE"] == "YES",
            "default": row["COLUMN_DEFAULT"],
            "characterLength": row["CHARACTER_MAXIMUM_LENGTH"],
            "numericPrecision": row["NUMERIC_PRECISION"],
            "numericScale": row["NUMERIC_SCALE"],
            "datetimePrecision": row["DATETIME_PRECISION"],
            "charset": row["CHARACTER_SET_NAME"],
            "collation": row["COLLATION_NAME"],
            "key": row["COLUMN_KEY"],
            "extra": row["EXTRA"],
            "comment": row["COLUMN_COMMENT"] or "",
            "generationExpression": row["GENERATION_EXPRESSION"] or "",
        }
        item["sensitivity"] = classify_sensitivity(item["name"], item["dataType"])
        item["scopeRole"] = infer_scope_role(item["name"])
        item["queryPolicy"] = infer_query_policy(item)
        columns_by_table[row["TABLE_NAME"]].append(item)

    indexes_by_table: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in indexes:
        table_indexes = indexes_by_table[row["TABLE_NAME"]]
        index = table_indexes.setdefault(
            row["INDEX_NAME"],
            {
                "name": row["INDEX_NAME"],
                "unique": int(row["NON_UNIQUE"]) == 0,
                "type": row["INDEX_TYPE"],
                "comment": row["INDEX_COMMENT"] or "",
                "columns": [],
            },
        )
        index["columns"].append(
            {
                "name": row["COLUMN_NAME"],
                "sequence": int(row["SEQ_IN_INDEX"]),
                "prefixLength": row["SUB_PART"],
                "direction": row["COLLATION"],
            }
        )

    foreign_keys_by_table: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in foreign_keys:
        table_foreign_keys = foreign_keys_by_table[row["TABLE_NAME"]]
        foreign_key = table_foreign_keys.setdefault(
            row["CONSTRAINT_NAME"],
            {
                "name": row["CONSTRAINT_NAME"],
                "referencedTable": row["REFERENCED_TABLE_NAME"],
                "columns": [],
            },
        )
        foreign_key["columns"].append(
            {
                "column": row["COLUMN_NAME"],
                "referencedColumn": row["REFERENCED_COLUMN_NAME"],
                "sequence": int(row["ORDINAL_POSITION"]),
            }
        )

    partition_by_table = {row["TABLE_NAME"]: row for row in partitions}
    table_items: list[dict[str, Any]] = []
    for row in tables:
        table_name = row["TABLE_NAME"]
        partition = partition_by_table.get(table_name)
        table_items.append(
            {
                "schema": schema_name,
                "name": table_name,
                "type": row["TABLE_TYPE"],
                "engine": row["ENGINE"],
                "collation": row["TABLE_COLLATION"],
                "comment": row["TABLE_COMMENT"] or "",
                "domain": infer_domain(table_name),
                "scopeColumns": [
                    item["name"]
                    for item in columns_by_table[table_name]
                    if item["scopeRole"] in {"tenant-scope", "store-scope"}
                ],
                "columns": columns_by_table[table_name],
                "indexes": sorted(indexes_by_table[table_name].values(), key=lambda item: item["name"]),
                "foreignKeys": sorted(foreign_keys_by_table[table_name].values(), key=lambda item: item["name"]),
                "partition": None
                if partition is None
                else {
                    "method": partition["PARTITION_METHOD"],
                    "subpartitionMethod": partition["SUBPARTITION_METHOD"],
                    "count": int(partition["PARTITION_COUNT"]),
                },
            }
        )

    return {
        "schema": schema_name,
        "connectionAliases": sorted(connection["aliases"]),
        "roles": sorted(set(connection["roles"])),
        "liveVerified": True,
        "structureEvidence": "mysql-information-schema",
        "structureSourceSchema": schema_name,
        "serverVersion": server["version"],
        "tables": table_items,
        "triggers": [
            {
                "name": row["TRIGGER_NAME"],
                "event": row["EVENT_MANIPULATION"],
                "table": row["EVENT_OBJECT_TABLE"],
                "timing": row["ACTION_TIMING"],
            }
            for row in triggers
        ],
        "routines": [
            {"name": row["ROUTINE_NAME"], "type": row["ROUTINE_TYPE"], "returnType": row["DATA_TYPE"]}
            for row in routines
        ],
    }


def inherit_identical_finance_shards(
    schemas: list[dict[str, Any]],
    collection_failures: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Cover failed TenantData0..9 schemas from one live shard after an explicit operator confirmation."""
    fallback_alias_pattern = re.compile(r"^TenantData[0-9]$")
    templates = [
        schema
        for schema in schemas
        if "finance-shard" in schema["roles"]
        and any(fallback_alias_pattern.fullmatch(alias) for alias in schema["connectionAliases"])
    ]
    if not templates:
        raise RuntimeError("没有成功采集 TenantData0-9 中的任何模板库，无法继承财务分库结构")

    # The operator-confirmed invariant applies only to TenantData0..9. The base TenantData route
    # is not silently covered unless its physical target also carries one of those shard aliases.
    template = sorted(templates, key=lambda item: item["schema"])[0]
    inherited: list[dict[str, Any]] = []
    for failure in collection_failures:
        aliases = failure["connectionAliases"]
        is_confirmed_shard = "finance-shard" in failure["roles"] and any(
            fallback_alias_pattern.fullmatch(alias) for alias in aliases
        )
        if not is_confirmed_shard:
            failure["structureCoveredByTemplate"] = False
            continue

        clone = copy.deepcopy(template)
        clone["schema"] = failure["schema"]
        clone["connectionAliases"] = aliases
        clone["roles"] = failure["roles"]
        clone["liveVerified"] = False
        clone["structureEvidence"] = "operator-confirmed-finance-template"
        clone["structureSourceSchema"] = template["schema"]
        clone["serverVersion"] = None
        for table in clone["tables"]:
            table["schema"] = clone["schema"]
        failure["structureCoveredByTemplate"] = True
        failure["structureSourceSchema"] = template["schema"]
        inherited.append(clone)
    return inherited


def structural_fingerprint(schema: dict[str, Any]) -> str:
    """Hash table, column, index, FK, and partition structure while excluding drift-prone metadata."""
    structural = []
    for table in schema["tables"]:
        structural.append(
            {
                "name": table["name"],
                "type": table["type"],
                "engine": table["engine"],
                "columns": [
                    {
                        "name": column["name"],
                        "columnType": column["columnType"],
                        "nullable": column["nullable"],
                        "key": column["key"],
                        "extra": column["extra"],
                    }
                    for column in table["columns"]
                ],
                "indexes": table["indexes"],
                "foreignKeys": table["foreignKeys"],
                "partition": table["partition"],
            }
        )
    payload = json.dumps(structural, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def markdown_escape(value: Any) -> str:
    """Keep generated Markdown tables valid without changing the underlying JSON catalog."""
    if value is None:
        return ""
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def build_markdown(
    schemas: list[dict[str, Any]],
    routes: dict[str, Any],
    generated_at: str,
    collection_failures: list[dict[str, Any]],
) -> str:
    """Render the complete human-readable dictionary; JSONL remains the runtime-oriented source."""
    lines = [
        "# 课小秘数据库完整物理数据字典",
        "",
        f"生成时间：{generated_at}",
        "",
        "本字典只来自 MySQL `information_schema` 与部署分库配置，不读取业务数据。连接地址、账号、密码和连接串不会写入本文件。",
        "字段的 `queryPolicy` 只是自动风险分类，不等于 Agent 已获授权；运行时仍必须使用服务端字段白名单、门店/租户注入、只读账号、条数和超时限制。",
        "",
        "## 财务分库路由",
        "",
    ]
    lines.extend(f"- {item}" for item in routes["algorithm"])
    lines.extend(["", "| TenantId | 最小 TenantId | 最大 TenantId | 连接名 |", "|---:|---:|---:|---|"])
    for route in routes["explicitRoutes"]:
        lines.append(
            f"| {route['tenantId']} | {route['minTenantId']} | {route['maxTenantId']} | {markdown_escape(route['connectionName'])} |"
        )

    lines.extend(["", "## 采集覆盖情况", ""])
    if collection_failures:
        covered = all(item.get("structureCoveredByTemplate") is True for item in collection_failures)
        if covered:
            lines.append(
                "全部配置目标均已有结构目录：未实时连通的 TenantData0-9 分片按运维方确认的同构约束继承自已实测模板库。"
                "结构覆盖完整不代表连接可用，运行时仍必须按目标租户路由并在连接失败时拒绝查询。"
            )
        else:
            lines.append("当前配置仍存在既未成功采集、也未被已确认同构模板覆盖的目标，不能把字典描述为完整结构快照。")
        lines.extend(
            [
                "",
                "| 逻辑连接别名 | 配置数据库 | 结构覆盖 | 模板数据库 | 实时错误类型 | MySQL 错误码 |",
                "|---|---|---|---|---|---:|",
            ]
        )
        for failure in collection_failures:
            lines.append(
                f"| {markdown_escape(', '.join(failure['connectionAliases']))} | {markdown_escape(failure['schema'])} | "
                f"{'模板继承' if failure.get('structureCoveredByTemplate') else '未覆盖'} | "
                f"{markdown_escape(failure.get('structureSourceSchema'))} | {markdown_escape(failure['errorType'])} | "
                f"{markdown_escape(failure['errorCode'])} |"
            )
    else:
        lines.append("全部配置路由目标均已成功采集。")

    lines.extend(["", "## 数据库概览", "", "| 数据库 | 角色 | 结构证据 | 模板数据库 | 逻辑连接别名 | 表/视图 | 字段 | 索引 | 外键 |", "|---|---|---|---|---|---:|---:|---:|---:|"])
    for schema in schemas:
        lines.append(
            "| {schema} | {roles} | {evidence} | {source_schema} | {aliases} | {tables} | {columns} | {indexes} | {foreign_keys} |".format(
                schema=markdown_escape(schema["schema"]),
                roles=markdown_escape(", ".join(schema["roles"])),
                evidence="实时采集" if schema["liveVerified"] else "同构模板继承",
                source_schema=markdown_escape(schema["structureSourceSchema"]),
                aliases=markdown_escape(", ".join(schema["connectionAliases"])),
                tables=len(schema["tables"]),
                columns=sum(len(item["columns"]) for item in schema["tables"]),
                indexes=sum(len(item["indexes"]) for item in schema["tables"]),
                foreign_keys=sum(len(item["foreignKeys"]) for item in schema["tables"]),
            )
        )

    for schema in schemas:
        lines.extend(["", f"## 数据库 `{schema['schema']}`", ""])
        lines.append(
            f"角色：{', '.join(schema['roles'])}；连接别名：{', '.join(schema['connectionAliases'])}；"
            f"结构证据：{'MySQL 实时元数据' if schema['liveVerified'] else '运维确认的同构模板继承'}；"
            f"结构来源：`{schema['structureSourceSchema']}`；结构指纹：`{schema['structuralFingerprint']}`。"
        )
        for table in schema["tables"]:
            lines.extend(
                [
                    "",
                    f"### `{table['name']}`",
                    "",
                    f"类型：{table['type']}；引擎：{table['engine'] or ''}；领域：{table['domain']}；隔离字段：{', '.join(table['scopeColumns']) or '无'}。",
                    f"表注释：{table['comment'] or '无'}",
                    "",
                    "| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |",
                    "|---:|---|---|---|---|---|---|---|---|---|",
                ]
            )
            for column in table["columns"]:
                lines.append(
                    "| {ordinal} | `{name}` | `{column_type}` | {nullable} | {key} | {default} | {comment} | {sensitivity} | {scope} | {policy} |".format(
                        ordinal=column["ordinal"],
                        name=markdown_escape(column["name"]),
                        column_type=markdown_escape(column["columnType"]),
                        nullable="是" if column["nullable"] else "否",
                        key=markdown_escape(column["key"]),
                        default=markdown_escape(column["default"]),
                        comment=markdown_escape(column["comment"]),
                        sensitivity=column["sensitivity"],
                        scope=column["scopeRole"],
                        policy=column["queryPolicy"],
                    )
                )
            if table["indexes"]:
                lines.extend(["", "索引："])
                for index in table["indexes"]:
                    columns = ", ".join(item["name"] or "<expression>" for item in index["columns"])
                    lines.append(f"- `{index['name']}`：{'唯一' if index['unique'] else '非唯一'} {index['type']}（{columns}）")
            if table["foreignKeys"]:
                lines.extend(["", "物理外键："])
                for foreign_key in table["foreignKeys"]:
                    pairs = ", ".join(
                        f"{item['column']} → {foreign_key['referencedTable']}.{item['referencedColumn']}"
                        for item in foreign_key["columns"]
                    )
                    lines.append(f"- `{foreign_key['name']}`：{pairs}")
            if table["partition"]:
                partition = table["partition"]
                lines.extend(["", f"分区：{partition['method']}，数量 {partition['count']}。"])

        if schema["triggers"]:
            lines.extend(["", "### 触发器目录", ""])
            lines.extend(
                f"- `{item['name']}`：{item['timing']} {item['event']} ON `{item['table']}`"
                for item in schema["triggers"]
            )
        if schema["routines"]:
            lines.extend(["", "### 存储过程与函数目录", ""])
            lines.extend(
                f"- `{item['name']}`：{item['type']}，返回类型 `{item['returnType'] or ''}`"
                for item in schema["routines"]
            )
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(
    output_dir: Path,
    schemas: list[dict[str, Any]],
    routes: dict[str, Any],
    collection_failures: list[dict[str, Any]],
) -> dict[str, Any]:
    """Write deterministic JSONL plus a full Markdown rendering and a compact validation report."""
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    for schema in schemas:
        schema["structuralFingerprint"] = structural_fingerprint(schema)

    jsonl_path = output_dir / "database-schema.jsonl"
    records = []
    for schema in schemas:
        for table in schema["tables"]:
            records.append(
                {
                    "catalogVersion": 1,
                    "generatedAtUtc": generated_at,
                    "source": schema["structureEvidence"],
                    "schema": schema["schema"],
                    "schemaRoles": schema["roles"],
                    "connectionAliases": schema["connectionAliases"],
                    "liveVerified": schema["liveVerified"],
                    "structureSourceSchema": schema["structureSourceSchema"],
                    "schemaFingerprint": schema["structuralFingerprint"],
                    **table,
                }
            )
    jsonl_path.write_text(
        "\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True, default=str) for item in records) + "\n",
        encoding="utf-8",
    )

    routing_path = output_dir / "database-routing.json"
    routing_path.write_text(json.dumps(routes, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    markdown_path = output_dir / "database-dictionary.md"
    markdown_path.write_text(
        build_markdown(schemas, routes, generated_at, collection_failures),
        encoding="utf-8",
    )

    finance = [schema for schema in schemas if "finance-shard" in schema["roles"]]
    fingerprints = defaultdict(list)
    for schema in finance:
        fingerprints[schema["structuralFingerprint"]].append(schema["schema"])
    validation = {
        "generatedAtUtc": generated_at,
        "schemaCount": len(schemas),
        "tableRecordCount": len(records),
        "columnCount": sum(len(item["columns"]) for schema in schemas for item in schema["tables"]),
        "indexCount": sum(len(item["indexes"]) for schema in schemas for item in schema["tables"]),
        "foreignKeyCount": sum(len(item["foreignKeys"]) for schema in schemas for item in schema["tables"]),
        "financialShardStructureGroups": [
            {"fingerprint": fingerprint, "schemas": sorted(schema_names)}
            for fingerprint, schema_names in sorted(fingerprints.items())
        ],
        "complete": all(item.get("structureCoveredByTemplate") is True for item in collection_failures),
        "structuralCoverageComplete": all(
            item.get("structureCoveredByTemplate") is True for item in collection_failures
        ),
        "liveCollectionComplete": len(collection_failures) == 0,
        "inheritedSchemas": [
            {
                "schema": schema["schema"],
                "structureSourceSchema": schema["structureSourceSchema"],
                "fingerprint": schema["structuralFingerprint"],
            }
            for schema in schemas
            if not schema["liveVerified"]
        ],
        "collectionFailures": collection_failures,
        "credentialsWritten": False,
        "businessRowsRead": False,
    }
    validation_path = output_dir / "database-dictionary-validation.json"
    validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return validation


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-access-config",
        type=Path,
        default=DEFAULT_DATA_ACCESS_CONFIG,
        help="课小秘 Skill 私有 data-access.local.json；默认读取当前 Skill/runtime",
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--inherit-finance-template-on-failure",
        action="store_true",
        help="按已确认的 TenantData0-9 同构约束，用成功采集的分片模板覆盖失败分片的结构目录",
    )
    args = parser.parse_args()

    if not args.data_access_config.is_file():
        parser.error("data-access-config 必须指向存在的 Skill 私有配置")

    try:
        connections, routes = discover_connections(load_json(args.data_access_config))
        schemas = []
        collection_failures = []
        for connection in sorted(connections, key=lambda item: ("main" not in item["roles"], item["database"])):
            # Progress contains only logical aliases/schema names; endpoint and credentials stay private.
            print(
                json.dumps(
                    {"collecting": connection["database"], "aliases": sorted(connection["aliases"])},
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
            try:
                schemas.append(collect_schema(connection))
            except Exception as exc:
                # Keep the catalog honest and useful: continue other targets, but persist only aliases,
                # configured schema, exception type, and numeric driver code. Never persist endpoints.
                error_code = None
                if getattr(exc, "args", None) and isinstance(exc.args[0], int):
                    error_code = exc.args[0]
                collection_failures.append(
                    {
                        "connectionAliases": sorted(connection["aliases"]),
                        "schema": connection["database"],
                        "roles": sorted(set(connection["roles"])),
                        "errorType": type(exc).__name__,
                        "errorCode": error_code,
                    }
                )
                print(
                    json.dumps(
                        {
                            "collectionFailed": connection["database"],
                            "aliases": sorted(connection["aliases"]),
                            "errorType": type(exc).__name__,
                            "errorCode": error_code,
                        },
                        ensure_ascii=False,
                    ),
                    file=sys.stderr,
                )
        if not schemas or not any("main" in schema["roles"] for schema in schemas):
            raise RuntimeError("课小秘主库元数据未成功采集，拒绝生成字典")
        if args.inherit_finance_template_on_failure:
            schemas.extend(inherit_identical_finance_shards(schemas, collection_failures))
        schemas.sort(key=lambda item: ("main" not in item["roles"], item["schema"]))
        validation = write_outputs(args.output_dir, schemas, routes, collection_failures)
        print(json.dumps(validation, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        # Driver errors can echo endpoint details, so only our explicit validation errors expose text.
        message = str(exc).splitlines()[0] if isinstance(exc, RuntimeError) else "数据库元数据采集失败，请检查本机网络和只读账号权限"
        print(json.dumps({"error": type(exc).__name__, "message": message}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
