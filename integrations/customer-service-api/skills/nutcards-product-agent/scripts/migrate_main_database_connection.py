#!/usr/bin/env python3
"""把现有主库连接最小化迁入 DuckAI 坚果卡包 Skill 私有 runtime 文件。"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migrate NutCards main database into DuckAI Skill runtime.")
    parser.add_argument("--sql-config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-connection", default="LinkFitDataOnlyRead")
    parser.add_argument("--target-connection", default="LinkFitDataOnlyRead")
    return parser.parse_args()


def load_source_connection(path: Path, name: str) -> dict[str, Any]:
    normalized_name = name.lower()
    if "readonly" not in normalized_name and "onlyread" not in normalized_name:
        raise ValueError("只允许迁移名称明确标识为只读的数据库连接")
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    connections = payload.get("ConnectionConfig", {}).get("Connections", [])
    matches = [item for item in connections if str(item.get("Name", "")).lower() == name.lower()]
    if len(matches) != 1 or not str(matches[0].get("ConnectionString", "")).strip():
        raise ValueError("来源主库连接不存在、重复或连接串为空")
    return matches[0]


def main() -> int:
    args = parse_args()
    if args.output.name != "data-access.local.json" or args.output.parent.name != "runtime":
        raise ValueError("输出必须是坚果卡包 Skill/runtime/data-access.local.json")

    source = load_source_connection(args.sql_config, args.source_connection)
    payload = {
        "schemaVersion": 1,
        "productCode": "nutcards",
        "mainConnectionName": args.target_connection,
        "connections": [
            {
                "name": args.target_connection,
                "providerName": "MySql",
                "connectionString": str(source["ConnectionString"]).strip(),
            }
        ],
        "tenantRoutes": [],
        "financeFallback": None,
        "executionPolicy": {
            "readOnly": True,
            "commandTimeoutSeconds": 5,
            "maxRows": 20,
            "maxFields": 16,
            "maxJoins": 4,
            "maxSerializedCharacters": 12000,
        },
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=args.output.parent,
            prefix=".data-access.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(payload, temporary, ensure_ascii=False, indent=2)
            temporary.write("\n")
        os.chmod(temporary_path, 0o600)
        os.replace(temporary_path, args.output)
        os.chmod(args.output, 0o600)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()

    # 只报告目标文件，不输出任何连接值。
    print(json.dumps({"connections": 1, "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
