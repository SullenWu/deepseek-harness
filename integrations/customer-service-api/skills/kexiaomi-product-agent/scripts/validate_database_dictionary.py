#!/usr/bin/env python3
"""Validate 课小秘 database dictionary structure, cross-file references, and coverage flags."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_SENSITIVITY = {"internal", "sensitive", "sensitive-unstructured", "restricted"}
ALLOWED_QUERY_POLICY = {
    "deny",
    "server-filter-only",
    "masked-or-filter-only",
    "semantic-review-required",
}
ALLOWED_RUNTIME_USAGES = {
    "select", "literal-filter", "order", "member-mobile-filter", "operator-uid-filter",
    "unclaimed-member-filter",
}
ALLOWED_RUNTIME_AGGREGATES = {"count", "sum", "min", "max"}
ALLOWED_FIELD_POLICIES = {"reviewed-business-fields", "support-metadata-only"}
FORBIDDEN_RUNTIME_FIELD_NAMES = {
    "appid", "app_id", "buyer_name", "condition_describe", "condition_info", "consignee",
    "enroll_id", "express_no", "external_userid", "material_data", "merchant_code",
    "mer_chant_no", "msg_info", "nick_name", "no", "out_no", "pay_by", "pay_order_no",
    "permanent_code", "pickup_code", "post_order_no", "principal_name", "promotion_code",
    "receive_account", "receiver_name", "receiver_zip", "rider_name", "sms_info", "sms_param",
    "temp_info", "user_description", "user_name", "user_state", "wechat_mer_no", "alipay_mer_no",
}
FORBIDDEN_RUNTIME_FIELD_MARKERS = {
    "trade_no", "order_no", "merchant_no", "mer_chant_no", "device_code", "card_no",
}
UNSAFE_RUNTIME_TABLE_MARKERS = {
    "auth_token", "platform_auth", "alipay_auth_info", "merchants_config", "merchant_config",
    "yop_config", "pay_config", "payment_config", "bank_account", "bank_card",
}
UNSAFE_RUNTIME_FIELD_MARKERS = {
    "password", "passwd", "pwd", "secret", "token", "openid", "open_id", "union_id",
    "mobile", "phone", "email", "address", "remark", "note", "content", "message",
    "payload", "request", "response", "identity", "bank", "random_param", "user_ip",
    "client_ip", "remote_ip", "ip_address",
}
USER_CARD_IDENTITY_OUTPUT_FIELDS = {
    "state", "store_user_no", "open_date", "last_date", "is_experience", "source_type",
    "wx_card_state", "is_sign_agreement", "create_date", "update_date",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Parse a JSONL artifact and include line numbers in validation failures."""
    result = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            result.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.name}:{line_number} 不是有效 JSON") from exc
    return result


def require(condition: bool, message: str) -> None:
    """Raise one concise validation error at the first broken invariant."""
    if not condition:
        raise ValueError(message)


def validate_schema(records: list[dict[str, Any]]) -> tuple[set[tuple[str, str]], dict[str, set[str]]]:
    """Validate unique tables, ordered unique columns, policies, indexes, and FK references."""
    table_keys: set[tuple[str, str]] = set()
    columns_by_table: dict[str, set[str]] = {}
    for record in records:
        schema = str(record.get("schema") or "")
        table = str(record.get("name") or "")
        require(schema and table, "schema 记录缺少数据库或表名")
        key = (schema, table)
        require(key not in table_keys, f"重复表记录：{schema}.{table}")
        table_keys.add(key)
        require(isinstance(record.get("liveVerified"), bool), f"{schema}.{table} 缺少结构实测标记")
        require(record.get("structureSourceSchema"), f"{schema}.{table} 缺少结构来源数据库")
        expected_source = "mysql-information-schema" if record["liveVerified"] else "operator-confirmed-finance-template"
        require(record.get("source") == expected_source, f"{schema}.{table} 结构证据与实测标记不一致")

        columns = record.get("columns") or []
        require(columns, f"{schema}.{table} 没有字段")
        column_names = [str(column.get("name") or "") for column in columns]
        normalized_column_names = [name.lower() for name in column_names]
        require(all(column_names), f"{schema}.{table} 存在空字段名")
        require(len(column_names) == len(set(normalized_column_names)), f"{schema}.{table} 存在重复字段")
        ordinals = [int(column.get("ordinal") or 0) for column in columns]
        require(ordinals == list(range(1, len(columns) + 1)), f"{schema}.{table} 字段序号不连续")
        for column in columns:
            require(column.get("sensitivity") in ALLOWED_SENSITIVITY, f"{schema}.{table}.{column['name']} 敏感级别无效")
            require(column.get("queryPolicy") in ALLOWED_QUERY_POLICY, f"{schema}.{table}.{column['name']} 查询策略无效")

        columns_by_table[table.lower()] = set(normalized_column_names)
        for index in record.get("indexes") or []:
            require(index.get("name"), f"{schema}.{table} 存在空索引名")
            for index_column in index.get("columns") or []:
                name = index_column.get("name")
                require(name is None or str(name).lower() in columns_by_table[table.lower()], f"{schema}.{table} 索引引用未知字段 {name}")
        for foreign_key in record.get("foreignKeys") or []:
            require(foreign_key.get("referencedTable"), f"{schema}.{table} 外键缺少目标表")
            for pair in foreign_key.get("columns") or []:
                require(str(pair.get("column") or "").lower() in columns_by_table[table.lower()], f"{schema}.{table} 外键引用未知本表字段")
    return table_keys, columns_by_table


def validate_inherited_schemas(
    records: list[dict[str, Any]],
    physical_validation: dict[str, Any],
) -> None:
    """Ensure every inherited shard is byte-equivalent in structure to its declared live template."""
    records_by_schema: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        records_by_schema.setdefault(record["schema"], []).append(record)

    for inherited in physical_validation.get("inheritedSchemas") or []:
        schema = inherited.get("schema")
        source_schema = inherited.get("structureSourceSchema")
        require(schema in records_by_schema, f"继承数据库不存在：{schema}")
        require(source_schema in records_by_schema, f"继承模板数据库不存在：{source_schema}")
        inherited_records = records_by_schema[schema]
        source_records = records_by_schema[source_schema]
        require(all(item.get("liveVerified") is False for item in inherited_records), f"继承数据库误标为实时采集：{schema}")
        require(all(item.get("liveVerified") is True for item in source_records), f"模板数据库不是实时采集：{source_schema}")
        require(
            {item.get("schemaFingerprint") for item in inherited_records}
            == {item.get("schemaFingerprint") for item in source_records}
            == {inherited.get("fingerprint")},
            f"继承数据库与模板结构指纹不一致：{schema}",
        )
        inherited_tables = {item["name"] for item in inherited_records}
        source_tables = {item["name"] for item in source_records}
        require(inherited_tables == source_tables, f"继承数据库与模板表集合不一致：{schema}")


def validate_relations(
    relations: list[dict[str, Any]],
    table_names: set[str],
    columns_by_table: dict[str, set[str]],
) -> None:
    """Reject logical relationships that reference a table or field absent from the live catalog."""
    seen = set()
    for relation in relations:
        key = (
            relation.get("leftTable"),
            relation.get("leftColumn"),
            relation.get("rightTable"),
            relation.get("rightColumn"),
        )
        require(key not in seen, f"重复逻辑关系：{key}")
        seen.add(key)
        left_table, left_column, right_table, right_column = key
        require(left_table in table_names and right_table in table_names, f"逻辑关系引用未知表：{key}")
        require(left_column in columns_by_table[left_table], f"逻辑关系引用未知字段：{left_table}.{left_column}")
        require(right_column in columns_by_table[right_table], f"逻辑关系引用未知字段：{right_table}.{right_column}")
        require(relation.get("agentJoinPolicy") == "semantic-review-required", f"逻辑关系意外授予运行权限：{key}")


def validate_enums(
    enums: list[dict[str, Any]],
    table_names: set[str],
    columns_by_table: dict[str, set[str]],
) -> None:
    """Ensure enum hints remain tied to existing fields and retain their review-required boundary."""
    for item in enums:
        table = item.get("table")
        column = item.get("column")
        require(table in table_names, f"枚举引用未知表：{table}")
        require(column in columns_by_table[table], f"枚举引用未知字段：{table}.{column}")
        require(item.get("values"), f"枚举没有值：{table}.{column}")
        require(item.get("confidence") == "comment-derived-review-required", f"枚举意外跳过复核：{table}.{column}")


def validate_query_policy(
    schema_records: list[dict[str, Any]],
    logical_relations: list[dict[str, Any]],
    query_tables: list[dict[str, Any]],
    query_relations: list[dict[str, Any]],
    customer_service_scope: dict[str, Any],
) -> None:
    """Verify runtime authorization is a conservative subset of the generated physical and relation catalogs."""
    physical: dict[tuple[str, str], dict[str, Any]] = {}
    for record in schema_records:
        roles = record.get("schemaRoles") or []
        source = "main" if "main" in roles else "finance" if "finance-shard" in roles and record.get("liveVerified") else None
        if source is not None:
            physical[(source, str(record["name"]).lower())] = record

    approved_scope_tables = {}
    for group in customer_service_scope.get("groups") or []:
        field_policy = str(group.get("fieldPolicy") or "")
        require(field_policy in ALLOWED_FIELD_POLICIES, f"客服数据分组字段策略无效：{group.get('name')}")
        for table in group.get("tables") or []:
            table_name = str(table).lower()
            require(table_name not in approved_scope_tables, f"客服数据范围重复归组：{table_name}")
            approved_scope_tables[table_name] = {
                "businessGroup": group.get("name"),
                "authority": group.get("authority"),
                "fieldPolicy": field_policy,
            }
    scope_version = int(customer_service_scope.get("scopeVersion") or 0)
    audience = str(customer_service_scope.get("audience") or "")
    require(scope_version >= 1, "客服数据库范围映射版本无效")
    require(audience == "merchant-customer-service", "客服数据库范围受众无效")
    require(customer_service_scope.get("defaultPolicy") == "exclude-unclassified", "客服数据库范围必须默认排除未归组表")

    seen_tables = set()
    for table in query_tables:
        source = table.get("dataSource")
        table_name = str(table.get("table") or "").lower()
        key = (source, table_name)
        require(source in {"main", "finance"} and key in physical, f"运行目录引用未知表：{key}")
        require(key not in seen_tables, f"运行目录重复表：{key}")
        require(table_name in approved_scope_tables, f"运行目录包含未进入客服范围映射的表：{key}")
        require(int(table.get("policyVersion") or 0) >= 2, f"运行目录表仍使用旧策略版本：{key}")
        require(int(table.get("scopeVersion") or 0) == scope_version, f"运行目录表范围版本不一致：{key}")
        require(table.get("audience") == audience, f"运行目录表受众不属于商家客服：{key}")
        require(table.get("businessGroup"), f"运行目录表缺少客服业务分组：{key}")
        require(table.get("authority"), f"运行目录表缺少数据权威级别：{key}")
        require(
            table.get("fieldPolicy") == approved_scope_tables[table_name]["fieldPolicy"],
            f"运行目录表字段策略与客服范围不一致：{key}",
        )
        require(set(table.get("rowCountAggregates") or []) == {"count"}, f"运行目录行数聚合边界无效：{key}")
        require(
            not any(marker in table_name for marker in UNSAFE_RUNTIME_TABLE_MARKERS),
            f"运行目录包含敏感配置表：{key}",
        )
        seen_tables.add(key)
        record = physical[key]
        physical_columns = {str(item["name"]).lower(): item for item in record.get("columns") or []}
        require(table.get("scopeColumns"), f"运行目录表缺少隔离字段：{key}")
        require(set(map(str.lower, table["scopeColumns"])) <= set(physical_columns), f"运行目录隔离字段不存在：{key}")
        for field in table.get("fields") or []:
            name = str(field.get("name") or "").lower()
            require(name in physical_columns, f"运行目录字段不存在：{key}.{name}")
            require(name not in FORBIDDEN_RUNTIME_FIELD_NAMES, f"运行目录包含敏感业务字段：{key}.{name}")
            require(
                not any(marker in name for marker in FORBIDDEN_RUNTIME_FIELD_MARKERS),
                f"运行目录包含订单、商户或设备标识：{key}.{name}",
            )
            usages = set(field.get("usages") or [])
            require(usages and usages <= ALLOWED_RUNTIME_USAGES, f"运行目录字段用法无效：{key}.{name}")
            aggregates = set(field.get("aggregates") or [])
            require(aggregates <= ALLOWED_RUNTIME_AGGREGATES, f"运行目录字段聚合无效：{key}.{name}")
            require(not aggregates or "select" in usages, f"不可输出字段意外获得聚合权限：{key}.{name}")
            if "unclaimed-member-filter" in usages:
                require(
                    key == ("main", "user_card") and name == "uid" and "literal-filter" not in usages,
                    f"未领卡身份过滤只能固定用于 main.user_card.uid：{key}.{name}",
                )
            if "member-mobile-filter" in usages and name == "card_tag":
                require(
                    key == ("main", "user_card"),
                    f"card_tag 手机号过滤只能定位门店会员身份：{key}.{name}",
                )
            if "member-mobile-filter" in usages:
                require(
                    (key, name) in {
                        (("main", "users"), "user_mobile"),
                        (("main", "user_card"), "card_tag"),
                    },
                    f"会员手机号值源被错误授予其他业务字段：{key}.{name}",
                )
            if "operator-uid-filter" in usages:
                require(
                    name in {"create_by", "update_by"},
                    f"当前操作人值源被错误授予业务实体字段：{key}.{name}",
                )
            if "select" in usages:
                if key == ("main", "user_card"):
                    require(
                        name in USER_CARD_IDENTITY_OUTPUT_FIELDS,
                        f"user_card 只能输出会员身份字段，具体持卡事实必须读取 user_card_child：{name}",
                    )
                column = physical_columns[name]
                require(column.get("sensitivity") == "internal", f"运行目录输出敏感字段：{key}.{name}")
                require(column.get("queryPolicy") == "semantic-review-required", f"运行目录输出服务端字段：{key}.{name}")
                require(
                    name != "id" and not name.endswith("_id") and not name.endswith("_uid"),
                    f"运行目录输出内部业务主键：{key}.{name}",
                )
                require(
                    not any(marker in name for marker in UNSAFE_RUNTIME_FIELD_MARKERS),
                    f"运行目录输出高风险字段：{key}.{name}",
                )

    logical_keys = {
        (
            item.get("leftTable"), item.get("leftColumn"), item.get("rightTable"), item.get("rightColumn")
        )
        for item in logical_relations
        if item.get("confidence") == "high" and int(item.get("occurrences") or 0) >= 3
    }
    for relation in query_relations:
        source = relation.get("dataSource")
        left_table = str(relation.get("leftTable") or "").lower()
        right_table = str(relation.get("rightTable") or "").lower()
        key = (
            relation.get("leftTable"), relation.get("leftColumn"), relation.get("rightTable"), relation.get("rightColumn")
        )
        require(key in logical_keys, f"运行目录关系没有高置信度源码证据：{key}")
        require((source, left_table) in seen_tables and (source, right_table) in seen_tables, f"运行目录关系引用未授权表：{key}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", required=True, type=Path)
    parser.add_argument("--customer-service-scope", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--require-live", action="store_true")
    args = parser.parse_args()

    required_files = (
        "database-schema.jsonl",
        "database-routing.json",
        "database-dictionary-validation.json",
        "database-logical-relations.jsonl",
        "database-enums.jsonl",
        "database-semantic-validation.json",
        "database-dictionary.md",
        "database-agent-query-catalog.jsonl",
        "database-agent-query-relations.jsonl",
        "database-query-policy-validation.json",
    )
    for name in required_files:
        require((args.directory / name).is_file(), f"缺少数据字典文件：{name}")

    schema_records = read_jsonl(args.directory / "database-schema.jsonl")
    relations = read_jsonl(args.directory / "database-logical-relations.jsonl")
    enums = read_jsonl(args.directory / "database-enums.jsonl")
    physical_validation = json.loads((args.directory / "database-dictionary-validation.json").read_text(encoding="utf-8"))
    semantic_validation = json.loads((args.directory / "database-semantic-validation.json").read_text(encoding="utf-8"))
    query_tables = read_jsonl(args.directory / "database-agent-query-catalog.jsonl")
    query_relations = read_jsonl(args.directory / "database-agent-query-relations.jsonl")
    query_validation = json.loads((args.directory / "database-query-policy-validation.json").read_text(encoding="utf-8"))
    scope_path = args.customer_service_scope or args.directory.parent / "database-customer-service-scope.json"
    require(scope_path.is_file(), f"缺少客服数据库范围映射：{scope_path}")
    customer_service_scope = json.loads(scope_path.read_text(encoding="utf-8-sig"))
    json.loads((args.directory / "database-routing.json").read_text(encoding="utf-8"))

    table_keys, columns_by_table = validate_schema(schema_records)
    validate_inherited_schemas(schema_records, physical_validation)
    table_names = set(columns_by_table)
    validate_relations(relations, table_names, columns_by_table)
    validate_enums(enums, table_names, columns_by_table)
    validate_query_policy(schema_records, relations, query_tables, query_relations, customer_service_scope)

    require(physical_validation.get("tableRecordCount") == len(schema_records), "物理表计数与 JSONL 不一致")
    require(semantic_validation.get("logicalRelationCount") == len(relations), "逻辑关系计数不一致")
    require(semantic_validation.get("enumHintCount") == len(enums), "枚举计数不一致")
    require(semantic_validation.get("runtimeAuthorizationGranted") is False, "语义目录不得授予运行权限")
    require(physical_validation.get("credentialsWritten") is False, "物理目录凭据边界无效")
    require(physical_validation.get("businessRowsRead") is False, "物理目录采集越过元数据边界")
    require(query_validation.get("tableCount") == len(query_tables), "运行目录表计数不一致")
    require(query_validation.get("fieldCount") == sum(len(item.get("fields") or []) for item in query_tables), "运行目录字段计数不一致")
    require(query_validation.get("relationCount") == len(query_relations), "运行目录关系计数不一致")
    require(query_validation.get("runtimeAuthorizationGranted") is True, "运行目录没有明确授予受控查询权限")
    require(query_validation.get("policyVersion") == 2, "运行目录策略版本不是 V2")
    require(query_validation.get("scopeVersion") == customer_service_scope.get("scopeVersion"), "运行目录范围版本不一致")
    require(query_validation.get("audience") == "merchant-customer-service", "运行目录受众不是商家客服")
    require(query_validation.get("defaultTablePolicy") == "exclude-unclassified", "运行目录未默认排除新表")
    require(query_validation.get("rawSqlAccepted") is False, "运行目录不得允许原始 SQL")
    require(query_validation.get("scopeInjectedByServer") is True, "运行目录必须由服务端注入隔离范围")
    require(query_validation.get("maxRows") == 20, "运行目录最大返回行数必须为二十")
    if args.require_complete:
        require(physical_validation.get("structuralCoverageComplete") is True, "配置中的数据库目标尚未全部获得结构覆盖")
    if args.require_live:
        require(physical_validation.get("liveCollectionComplete") is True, "配置中的数据库目标尚未全部实时采集成功")

    print(
        json.dumps(
            {
                "validated": True,
                "complete": bool(physical_validation.get("complete")),
                "liveCollectionComplete": bool(physical_validation.get("liveCollectionComplete")),
                "tables": len(table_keys),
                "relations": len(relations),
                "enums": len(enums),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
