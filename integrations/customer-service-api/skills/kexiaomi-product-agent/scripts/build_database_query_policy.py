#!/usr/bin/env python3
"""Build the conservative runtime query policy consumed by the 课小秘 customer-service Agent."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_CUSTOMER_SERVICE_SCOPE = (
    Path(__file__).resolve().parent.parent / "references" / "database-customer-service-scope.json"
)

SAFE_TYPES = {
    "bit", "bool", "boolean", "tinyint", "smallint", "mediumint", "int", "integer", "bigint",
    "decimal", "numeric", "float", "double", "real", "date", "datetime", "timestamp", "time",
    "year", "char", "varchar", "enum",
}
UNSAFE_NAME_MARKERS = (
    "password", "passwd", "pwd", "pass", "secret", "token", "openid", "open_id", "union_id",
    "mobile", "phone", "email", "address", "remark", "note", "content", "desc", "reason", "message",
    "payload", "request", "response", "body", "file", "image", "img", "url", "path", "license",
    "longitude", "latitude", "card_number", "card_tag", "identity", "bank", "random_param",
    "user_ip", "client_ip", "remote_ip", "ip_address",
    "trade_no", "order_no", "merchant_no", "mer_chant_no", "device_code", "card_no",
    "create_by", "update_by",
)
UNSAFE_EXACT_FIELD_NAMES = {
    # 这些字段名称未必包含传统 PII 关键词，但会暴露订单定位信息、外部账号或消息正文。
    "appid", "app_id", "buyer_name", "condition_describe", "condition_info", "consignee",
    "enroll_id", "express_no", "external_userid", "material_data", "merchant_code",
    "mer_chant_no", "msg_info", "nick_name", "out_no", "pay_by", "pay_order_no", "permanent_code",
    "pickup_code", "post_order_no", "principal_name", "promotion_code", "receive_account",
    "receiver_name", "receiver_zip", "rider_name", "sms_info", "sms_param", "temp_info",
    "user_description", "user_name", "user_state", "wechat_mer_no", "alipay_mer_no", "no",
}
UNSAFE_COMMENT_MARKERS = (
    "手机号", "手机号码", "密码", "身份证", "银行卡", "地址", "经度", "纬度", "备注", "说明内容",
    "请求内容", "响应内容", "文件地址", "图片地址", "姓名", "收件人", "收货", "法人", "受益人",
    "外部联系人", "商户号", "商户账号", "授权码", "提货码", "快递单号", "消息内容", "模板内容",
    "筛选条件", "欢迎语", "交易流水", "外部单号", "推广码", "用户名称",
)
# 当前客服身份链只确认操作人的平台 UID；业务表中的 uid/user_id/staff_id 经常属于会员或员工实体，
# 不能仅凭字段名绑定为当前操作人。创建人与修改人字段才允许使用该值源。
OPERATOR_FIELD_NAMES = {"create_by", "update_by"}
MEMBER_MOBILE_FILTER_FIELDS = {("users", "user_mobile"), ("user_card", "card_tag")}
TABLE_SEMANTIC_COMMENTS = {
    "users": "平台账号身份；已领卡会员由 user_mobile 定位账号，再通过 users.id = user_card.uid 关联门店会员身份。",
    "user_card": "当前门店会员身份；不是会员持有的具体卡。已领卡由 uid 关联 users，未领卡由 card_tag 手机号且 uid=0 定位。",
    "user_card_child": "会员实际持有的具体卡；必须通过 user_card.id = user_card_child.card_id 关联会员身份，不直接按手机号定位。",
}
# 信息库字段注释可能落后于当前业务代码。这里只修正跨问题都适用的字段语义，
# 不在运行目录中编排某一种客服问法或预置查询条件。
FIELD_SEMANTIC_COMMENTS = {
    ("store_vacation", "card_extension"): "会员卡延期模式：0不延期；1仅期限类卡（CardType=2/3）；2所有卡类型中符合有效期和状态条件的持卡记录，不代表无条件处理全部会员或全部卡。",
    ("store_vacation", "card_extension_days"): "独立配置的延期天数，不自动等于放假起止日期跨度。",
    ("user_card_child", "card_type"): "当前卡类型：0计次、1储值、2时限、3周期（旧称权益）、4安心充、6课时；旧数据库注释中的课时卡5已过时。",
}
USER_CARD_IDENTITY_OUTPUT_FIELDS = {
    "state", "store_user_no", "open_date", "last_date", "is_experience", "source_type",
    "wx_card_state", "is_sign_agreement", "create_date", "update_date",
}
UNSAFE_TABLE_MARKERS = (
    "auth_token", "platform_auth", "alipay_auth_info", "merchants_config", "merchant_config",
    "yop_config", "pay_config", "payment_config", "bank_account", "bank_card",
)
ALLOWED_FIELD_POLICIES = {"reviewed-business-fields", "support-metadata-only"}
SUPPORT_METADATA_EXACT_FIELDS = {
    "state", "status", "type", "platform", "title", "name", "order_by", "distance",
}
SUPPORT_METADATA_NAME_MARKERS = (
    "state", "status", "type", "count", "sum", "price", "amount", "fee", "deduct",
    "integral", "discount", "rate", "value", "quantity", "date", "time", "version",
    "method", "mode", "platform", "source", "tag", "title", "name", "level", "expire",
    "audit", "is_", "with_", "can_", "max_", "min_",
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read non-empty JSONL records."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def is_safe_output(column: dict[str, Any]) -> bool:
    """Allow only bounded, internal business fields and reject text likely to contain secrets or free-form PII."""
    name = str(column.get("name") or "").lower()
    comment = str(column.get("comment") or "")
    if column.get("queryPolicy") != "semantic-review-required" or column.get("sensitivity") != "internal":
        return False
    if str(column.get("dataType") or "").lower() not in SAFE_TYPES:
        return False
    if name in UNSAFE_EXACT_FIELD_NAMES:
        return False
    if any(marker in name for marker in UNSAFE_NAME_MARKERS):
        return False
    # 内部主键只可由运行关系目录用于 Join，不能作为结果、排序或模型填写的 literal 条件。
    if name == "id" or name.endswith("_id") or name.endswith("_uid"):
        return False
    if any(marker in comment for marker in UNSAFE_COMMENT_MARKERS):
        return False
    length = column.get("characterLength")
    return length is None or int(length) <= 200


def is_semantically_safe_output(
    table_name: str,
    column: dict[str, Any],
    field_policy: str,
) -> bool:
    """Apply the table field profile without encoding any customer question or fixed answer."""
    name = str(column.get("name") or "").lower()
    if not is_safe_output(column):
        return False
    if table_name == "user_card" and name not in USER_CARD_IDENTITY_OUTPUT_FIELDS:
        return False
    if field_policy == "reviewed-business-fields":
        return True
    if field_policy != "support-metadata-only":
        return False
    return name in SUPPORT_METADATA_EXACT_FIELDS or any(
        marker in name for marker in SUPPORT_METADATA_NAME_MARKERS
    )


def member_mobile_filter(table_name: str, column: dict[str, Any]) -> bool:
    """Permit phone matching only through the server-held current-message mobile placeholder."""
    name = str(column.get("name") or "").lower()
    return (table_name, name) in MEMBER_MOBILE_FILTER_FIELDS


def unclaimed_member_filter(table_name: str, column: dict[str, Any]) -> bool:
    """Expose only the reviewed user_card.uid=0 branch through a server-fixed value source."""
    return table_name == "user_card" and str(column.get("name") or "").lower() == "uid"


def operator_filter(column: dict[str, Any]) -> bool:
    """Expose identity columns only as equality filters bound to the verified current operator."""
    return str(column.get("name") or "").lower() in OPERATOR_FIELD_NAMES


def is_safe_table(
    record: dict[str, Any],
    approved_tables: dict[str, dict[str, str]],
    excluded_patterns: list[re.Pattern[str]],
) -> bool:
    """只授权客服范围映射明确归组的表，并再次拒绝安全或内部范围规则命中的表。"""
    name = str(record.get("name") or "").lower()
    return (
        name in approved_tables
        and not any(marker in name for marker in UNSAFE_TABLE_MARKERS)
        and not any(pattern.search(name) for pattern in excluded_patterns)
    )


def load_customer_service_scope(
    path: Path,
) -> tuple[int, str, dict[str, dict[str, str]], list[re.Pattern[str]]]:
    """读取人工审核的数据受众映射；未归组表默认排除，避免新表自动暴露给客服 Agent。"""
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    scope_version = int(payload.get("scopeVersion") or 0)
    audience = str(payload.get("audience") or "").strip()
    if scope_version < 1 or not audience or payload.get("defaultPolicy") != "exclude-unclassified":
        raise RuntimeError("客服数据库范围映射版本、受众或默认排除策略无效")

    approved_tables: dict[str, dict[str, str]] = {}
    for group in payload.get("groups") or []:
        group_name = str(group.get("name") or "").strip()
        authority = str(group.get("authority") or "").strip()
        field_policy = str(group.get("fieldPolicy") or "").strip()
        if not group_name or not authority or field_policy not in ALLOWED_FIELD_POLICIES:
            raise RuntimeError("客服数据库范围分组缺少 name/authority 或 fieldPolicy 无效")
        for raw_table in group.get("tables") or []:
            table = str(raw_table or "").strip().lower()
            if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", table):
                raise RuntimeError(f"客服数据库范围包含非法表名：{table}")
            if table in approved_tables:
                raise RuntimeError(f"客服数据库范围重复归组：{table}")
            approved_tables[table] = {
                "audience": audience,
                "authority": authority,
                "businessGroup": group_name,
                "fieldPolicy": field_policy,
            }

    excluded_patterns: list[re.Pattern[str]] = []
    for family in payload.get("excludedFamilies") or []:
        for raw_pattern in family.get("tablePatterns") or []:
            excluded_patterns.append(re.compile(str(raw_pattern), re.IGNORECASE))
    overlap = sorted(
        table for table in approved_tables if any(pattern.search(table) for pattern in excluded_patterns)
    )
    if overlap:
        raise RuntimeError("客服授权表同时命中排除范围：" + ",".join(overlap))
    return scope_version, audience, approved_tables, excluded_patterns


def data_source(record: dict[str, Any]) -> str | None:
    """Map the physical catalog role to the only two runtime connection families."""
    roles = record.get("schemaRoles") or []
    if "main" in roles:
        return "main"
    if "finance-shard" in roles and record.get("liveVerified") is True:
        return "finance"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema-catalog", required=True, type=Path)
    parser.add_argument("--relations", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--customer-service-scope", type=Path, default=DEFAULT_CUSTOMER_SERVICE_SCOPE)
    args = parser.parse_args()

    schema_records = read_jsonl(args.schema_catalog)
    relation_records = read_jsonl(args.relations)
    scope_version, audience, approved_tables, excluded_patterns = load_customer_service_scope(
        args.customer_service_scope
    )
    schema_table_names = {str(record.get("name") or "").lower() for record in schema_records}
    unknown_approved_tables = sorted(set(approved_tables) - schema_table_names)
    if unknown_approved_tables:
        raise RuntimeError("客服数据库范围包含物理目录不存在的表：" + ",".join(unknown_approved_tables))
    table_records: list[dict[str, Any]] = []
    eligible_by_source: dict[str, set[str]] = {"main": set(), "finance": set()}
    explicitly_excluded_tables: set[str] = set()
    unclassified_tables: set[str] = set()

    for record in schema_records:
        source = data_source(record)
        scope_columns = record.get("scopeColumns") or []
        table_name = str(record.get("name") or "").lower()
        if source is None or not scope_columns:
            continue
        if any(pattern.search(table_name) for pattern in excluded_patterns):
            explicitly_excluded_tables.add(table_name)
        elif table_name not in approved_tables:
            unclassified_tables.add(table_name)
        if not is_safe_table(record, approved_tables, excluded_patterns):
            continue
        # 表级字段策略来自已审核的客服业务域映射，必须先确定后再筛选任何字段。
        scope = approved_tables[table_name]
        fields = []
        for column in record.get("columns") or []:
            usages = []
            if is_semantically_safe_output(table_name, column, scope["fieldPolicy"]):
                usages.extend(["select", "literal-filter", "order"])
            if member_mobile_filter(table_name, column):
                usages.append("member-mobile-filter")
            if operator_filter(column):
                usages.append("operator-uid-filter")
            if unclaimed_member_filter(table_name, column):
                usages.append("unclaimed-member-filter")
            if not usages:
                continue
            aggregates = []
            if "select" in usages:
                aggregates.extend(["count", "min", "max"])
                if str(column.get("dataType") or "").lower() in {
                    "bit", "bool", "boolean", "tinyint", "smallint", "mediumint", "int", "integer",
                    "bigint", "decimal", "numeric", "float", "double", "real",
                }:
                    aggregates.append("sum")
            fields.append(
                {
                    "name": column["name"],
                    "dataType": column["dataType"],
                    "comment": FIELD_SEMANTIC_COMMENTS.get(
                        (table_name, str(column.get("name") or "").lower()),
                        column.get("comment") or "",
                    ),
                    "usages": usages,
                    "aggregates": aggregates,
                }
            )
        # 已归组表即使没有可输出字段，也保留经授权的 COUNT(*) 能力；这不会放开任何具体列，
        # 但可回答“是否有记录/共有多少条”这类通用商家事实。
        eligible_by_source[source].add(table_name)
        table_records.append(
            {
                "policyVersion": 2,
                "scopeVersion": scope_version,
                "dataSource": source,
                "table": table_name,
                "domain": record.get("domain") or "other",
                "businessGroup": scope["businessGroup"],
                "audience": scope["audience"],
                "authority": scope["authority"],
                "fieldPolicy": scope["fieldPolicy"],
                "comment": TABLE_SEMANTIC_COMMENTS.get(table_name, record.get("comment") or ""),
                "scopeColumns": scope_columns,
                "rowCountAggregates": ["count"],
                "fields": fields,
            }
        )

    relation_policy: list[dict[str, Any]] = []
    for relation in relation_records:
        if relation.get("confidence") != "high" or int(relation.get("occurrences") or 0) < 3:
            continue
        for source in ("main", "finance"):
            if relation["leftTable"] not in eligible_by_source[source] or relation["rightTable"] not in eligible_by_source[source]:
                continue
            relation_policy.append(
                {
                    "policyVersion": 2,
                    "dataSource": source,
                    "leftTable": relation["leftTable"],
                    "leftColumn": relation["leftColumn"],
                    "rightTable": relation["rightTable"],
                    "rightColumn": relation["rightColumn"],
                    "evidenceType": relation["evidenceType"],
                    "occurrences": relation["occurrences"],
                }
            )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    table_records.sort(key=lambda item: (item["dataSource"], item["table"]))
    relation_policy.sort(
        key=lambda item: (
            item["dataSource"], item["leftTable"], item["leftColumn"], item["rightTable"], item["rightColumn"]
        )
    )
    (args.output_dir / "database-agent-query-catalog.jsonl").write_text(
        "\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in table_records) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "database-agent-query-relations.jsonl").write_text(
        "\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in relation_policy) + "\n",
        encoding="utf-8",
    )
    validation = {
        "generatedAtUtc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "policyVersion": 2,
        "scopeVersion": scope_version,
        "audience": audience,
        "defaultTablePolicy": "exclude-unclassified",
        "approvedTableCount": len(approved_tables),
        "explicitlyExcludedTableCount": len(explicitly_excluded_tables),
        "unclassifiedExcludedTableCount": len(unclassified_tables),
        "tableCount": len(table_records),
        "fieldCount": sum(len(item["fields"]) for item in table_records),
        "relationCount": len(relation_policy),
        "runtimeAuthorizationGranted": True,
        "rawSqlAccepted": False,
        "scopeInjectedByServer": True,
        "maxRows": 20,
        "authorizationBasis": "scoped-tables-safe-fields-and-high-confidence-repository-joins",
    }
    (args.output_dir / "database-query-policy-validation.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(validation, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
