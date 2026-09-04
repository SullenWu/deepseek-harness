#!/usr/bin/env python3
"""Enrich the physical 课小秘 catalog with source-evidenced logical joins and enum hints.

Legacy tables declare no physical foreign keys, so information_schema alone cannot describe the
business graph. This script scans repository SQL text for explicit alias.column equality joins and
extracts state/type enum hints from database column comments. The result is discovery evidence for
later review; it does not authorize an Agent to execute a join or expose a field.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


TABLE_ALIAS_RE = re.compile(
    r"\b(?:from|join)\s+`?(?P<table>[a-z][a-z0-9_]*)`?\s+(?:as\s+)?`?(?P<alias>[a-z][a-z0-9_]*)`?",
    re.IGNORECASE,
)
EQUALITY_RE = re.compile(
    r"`?(?P<left_alias>[a-z][a-z0-9_]*)`?\s*\.\s*`?(?P<left_column>[a-z][a-z0-9_]*)`?\s*=\s*"
    r"`?(?P<right_alias>[a-z][a-z0-9_]*)`?\s*\.\s*`?(?P<right_column>[a-z][a-z0-9_]*)`?",
    re.IGNORECASE,
)
ENUM_COLUMN_RE = re.compile(r"(^|_)(state|status|type|mode|way|source|platform|client_type|is_[a-z0-9_]+)($|_)")
ENUM_VALUE_RE = re.compile(r"(?<![0-9.])-?\d+(?![0-9.])")
SOURCE_ROOTS = (
    "Libraries/LingKe.Persistence",
    "Libraries/LingKe.Provider",
    "Libraries/LingKeModel",
    "Platform/LingKe/LingKe.Model",
    "Public/LingKe/NutBooking.Tools",
)


def load_catalog(path: Path) -> tuple[list[dict[str, Any]], set[str], dict[str, set[str]]]:
    """Load JSONL and build schema-independent table/column lookup sets."""
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    table_names = {str(record["name"]).lower() for record in records}
    columns_by_table: dict[str, set[str]] = defaultdict(set)
    for record in records:
        table_name = str(record["name"]).lower()
        columns_by_table[table_name].update(str(column["name"]).lower() for column in record["columns"])
    return records, table_names, columns_by_table


def find_alias_table(text: str, alias: str, before: int, table_names: set[str]) -> tuple[str, int] | None:
    """Find the nearest preceding SQL FROM/JOIN definition for one alias within a bounded query window."""
    window_start = max(0, before - 2200)
    candidate = None
    for match in TABLE_ALIAS_RE.finditer(text, window_start, before):
        if match.group("alias").lower() != alias.lower():
            continue
        table_name = match.group("table").lower()
        if table_name not in table_names:
            continue
        candidate = (table_name, match.start())
    return candidate


def normalize_relation(
    left_table: str,
    left_column: str,
    right_table: str,
    right_column: str,
) -> tuple[str, str, str, str]:
    """Give equivalent join evidence a deterministic direction and identifier."""
    left = (left_table, left_column)
    right = (right_table, right_column)
    if right < left:
        left, right = right, left
    return left[0], left[1], right[0], right[1]


def extract_logical_relations(
    repo_root: Path,
    table_names: set[str],
    columns_by_table: dict[str, set[str]],
) -> list[dict[str, Any]]:
    """Extract only relationships whose two tables and two columns exist in the live physical catalog."""
    evidence: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for relative_root in SOURCE_ROOTS:
        source_root = repo_root / relative_root
        if not source_root.is_dir():
            continue
        for path in source_root.rglob("*.cs"):
            try:
                text = path.read_text(encoding="utf-8-sig", errors="ignore")
            except OSError:
                continue
            relative_path = str(path.relative_to(repo_root))
            for match in EQUALITY_RE.finditer(text):
                left_alias = match.group("left_alias").lower()
                right_alias = match.group("right_alias").lower()
                if left_alias == right_alias:
                    continue
                left_mapping = find_alias_table(text, left_alias, match.start(), table_names)
                right_mapping = find_alias_table(text, right_alias, match.start(), table_names)
                if left_mapping is None or right_mapping is None:
                    continue
                left_table, left_position = left_mapping
                right_table, right_position = right_mapping
                if left_table == right_table or match.start() - min(left_position, right_position) > 2200:
                    continue
                left_column = match.group("left_column").lower()
                right_column = match.group("right_column").lower()
                if left_column not in columns_by_table[left_table] or right_column not in columns_by_table[right_table]:
                    continue
                key = normalize_relation(left_table, left_column, right_table, right_column)
                item = evidence.setdefault(
                    key,
                    {
                        "leftTable": key[0],
                        "leftColumn": key[1],
                        "rightTable": key[2],
                        "rightColumn": key[3],
                        "evidenceType": "repository-sql-equality",
                        "occurrences": 0,
                        "sourceFiles": set(),
                    },
                )
                item["occurrences"] += 1
                # Keep evidence useful without creating an unbounded list for frequently reused joins.
                if len(item["sourceFiles"]) < 12:
                    item["sourceFiles"].add(relative_path)

    result = []
    for item in evidence.values():
        source_files = sorted(item.pop("sourceFiles"))
        item["sourceFiles"] = source_files
        item["confidence"] = (
            "high"
            if item["occurrences"] >= 3 or len(source_files) >= 2
            else "medium"
        )
        item["agentJoinPolicy"] = "semantic-review-required"
        result.append(item)
    return sorted(
        result,
        key=lambda item: (item["leftTable"], item["leftColumn"], item["rightTable"], item["rightColumn"]),
    )


def clean_enum_label(value: str) -> str:
    """Remove common connective suffixes that belong to the following enum item."""
    label = re.sub(r"\s+", " ", value or "").strip(" ：:=，,；;、-—")
    label = re.sub(r"^(?:表示|为)\s*", "", label)
    label = re.sub(r"\s+(?:and|or)$", "", label, flags=re.IGNORECASE)
    return label


def extract_enums(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract conservative numeric enum hints only from state/type-like columns with DB comments."""
    result = []
    seen = set()
    for record in records:
        for column in record["columns"]:
            column_name = str(column["name"]).lower()
            comment = str(column.get("comment") or "").strip()
            if not comment or not ENUM_COLUMN_RE.search(column_name):
                continue
            values = []
            number_matches = list(ENUM_VALUE_RE.finditer(comment))
            for index, match in enumerate(number_matches):
                label_end = number_matches[index + 1].start() if index + 1 < len(number_matches) else len(comment)
                label = clean_enum_label(comment[match.end():label_end])
                if not label or len(label) > 36:
                    continue
                pair = (match.group(0), label)
                if pair not in values:
                    values.append(pair)
            if not values:
                continue
            key = (record["schema"], record["name"], column_name, tuple(values))
            if key in seen:
                continue
            seen.add(key)
            result.append(
                {
                    "schema": record["schema"],
                    "table": record["name"],
                    "column": column_name,
                    "source": "information-schema-column-comment",
                    "comment": comment,
                    "values": [{"value": value, "label": label} for value, label in values],
                    "confidence": "comment-derived-review-required",
                }
            )
    return sorted(result, key=lambda item: (item["schema"], item["table"], item["column"]))


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    """Write stable UTF-8 JSONL suitable for indexed retrieval."""
    path.write_text(
        "\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in records) + ("\n" if records else ""),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    if not args.catalog.is_file() or not args.repo_root.is_dir():
        parser.error("catalog 和 repo-root 必须存在")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    records, table_names, columns_by_table = load_catalog(args.catalog)
    relations = extract_logical_relations(args.repo_root, table_names, columns_by_table)
    enums = extract_enums(records)
    write_jsonl(args.output_dir / "database-logical-relations.jsonl", relations)
    write_jsonl(args.output_dir / "database-enums.jsonl", enums)

    validation = {
        "catalogTableRecords": len(records),
        "catalogUniqueTables": len(table_names),
        "logicalRelationCount": len(relations),
        "highConfidenceRelationCount": sum(item["confidence"] == "high" for item in relations),
        "enumHintCount": len(enums),
        "runtimeAuthorizationGranted": False,
    }
    (args.output_dir / "database-semantic-validation.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(validation, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
