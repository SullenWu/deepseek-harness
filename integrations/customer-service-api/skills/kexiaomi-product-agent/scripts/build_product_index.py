#!/usr/bin/env python3
"""Build a deterministic, heading-aware JSONL index from the 课小秘 product manual."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
EVIDENCE_LABELS = (
    "服务端强制",
    "前端预判",
    "配置驱动",
    "平台差异",
    "源码推断",
    "冲突",
    "历史兼容",
    "接口缺口",
)
DOMAIN_KEYWORDS = {
    "identity-store": ("登录", "身份", "门店", "切店", "授权"),
    "permission-version": ("权限", "版本", "模块", "服务期", "到期"),
    "member-card": ("会员", "会员卡", "课卡", "卡资格", "卡绑定", "合同"),
    "course-schedule": ("课程", "排课", "课次", "教练", "场地"),
    "reservation-waitlist": ("预约", "候补", "签到", "取消", "旷课"),
    "staff-binding": ("员工", "店员", "管理员", "扫码绑定", "离职"),
    "payment-refund": ("消费", "支付", "退款", "优惠券", "积分"),
    "operations-sales": ("报表", "经营", "订购", "产品", "营销"),
}
ENTITY_KEYWORDS = {
    "Store": ("门店", "StoreId"),
    "PlatformUser": ("平台用户", "Uid", "登录身份"),
    "StoreMember": ("门店会员", "会员资料"),
    "StaffMembership": ("员工关系", "正式员工", "临时员工", "教练"),
    "Course": ("课程项目", "CourseId"),
    "Lesson": ("课次", "LessonsId"),
    "Reservation": ("预约", "候补", "签到"),
    "UserCard": ("会员持有卡", "会员卡", "CardId"),
    "CourseCardBinding": ("课程与卡关联", "课程卡绑定", "卡资格"),
    "ConsumptionLog": ("消费单", "ConsumptionId"),
    "PaymentOrder": ("支付单", "渠道支付", "支付回调"),
    "RefundAttempt": ("退款", "退卡", "回卡"),
}
API_RE = re.compile(r"(?<![A-Za-z0-9_])/?([A-Za-z][A-Za-z0-9]+/[A-Za-z][A-Za-z0-9]+)")


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def split_content(content: str, limit: int) -> list[str]:
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", content) if item.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = paragraph if not current else current + "\n\n" + paragraph
        if len(candidate) <= limit:
            current = candidate
            continue
        if current:
            chunks.append(current)
        while len(paragraph) > limit:
            chunks.append(paragraph[:limit])
            paragraph = paragraph[limit:]
        current = paragraph
    if current:
        chunks.append(current)
    return chunks


def infer_values(text: str, mapping: dict[str, tuple[str, ...]]) -> list[str]:
    return [name for name, keywords in mapping.items() if any(keyword in text for keyword in keywords)]


def infer_client(heading_path: str) -> str:
    if "顾客端" in heading_path:
        return "customer-mini-program"
    if "商家端" in heading_path:
        return "business-mini-program"
    if "PC" in heading_path or "管理后台" in heading_path:
        return "pc-admin"
    return "cross-client"


def build_records(source: Path, product_codes: list[str], chunk_limit: int) -> list[dict]:
    raw = source.read_text(encoding="utf-8")
    source_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    heading_stack: list[str] = []
    sections: list[tuple[str, str]] = []
    buffer: list[str] = []

    def flush() -> None:
        content = "\n".join(buffer).strip()
        buffer.clear()
        if content:
            sections.append((" > ".join(heading_stack) or "文档说明", content))

    for line in raw.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        match = HEADING_RE.match(line)
        if not match:
            buffer.append(line)
            continue
        flush()
        level = len(match.group(1))
        heading = normalize_text(match.group(2))
        heading_stack[:] = heading_stack[: level - 1]
        heading_stack.append(heading)
    flush()

    records: list[dict] = []
    for heading_path, content in sections:
        for part_index, part in enumerate(split_content(content, chunk_limit), start=1):
            searchable = heading_path + "\n" + part
            evidence = [label for label in EVIDENCE_LABELS if f"【{label}】" in searchable]
            if "待确认" in searchable and "待确认" not in evidence:
                evidence.append("待确认")
            apis = sorted({match.group(1) for match in API_RE.finditer(searchable)})
            domains = infer_values(searchable, DOMAIN_KEYWORDS) or ["general"]
            entities = infer_values(searchable, ENTITY_KEYWORDS)
            identity_material = f"{source_hash}|{heading_path}|{part_index}|{part}".encode("utf-8")
            records.append(
                {
                    "chunkId": hashlib.sha256(identity_material).hexdigest()[:20],
                    "productCodes": product_codes,
                    "client": infer_client(heading_path),
                    "domains": domains,
                    "headingPath": heading_path,
                    "part": part_index,
                    "evidenceLevels": evidence or ["源码说明"],
                    "entities": entities,
                    "apis": apis,
                    "sourceFile": source.name,
                    "sourceSha256": source_hash,
                    "content": part,
                }
            )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--product-code",
        action="append",
        dest="product_codes",
        default=[],
        help="Repeat for each product code that may load this skill.",
    )
    parser.add_argument("--chunk-limit", type=int, default=2400)
    args = parser.parse_args()

    if not args.source.is_file():
        parser.error(f"source file does not exist: {args.source}")
    if not args.product_codes:
        parser.error("at least one --product-code is required")
    if args.chunk_limit < 800 or args.chunk_limit > 4000:
        parser.error("--chunk-limit must be between 800 and 4000")

    records = build_records(args.source, sorted(set(args.product_codes)), args.chunk_limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = "\n".join(json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    print(json.dumps({"records": len(records), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
