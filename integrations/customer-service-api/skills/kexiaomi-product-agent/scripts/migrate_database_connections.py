#!/usr/bin/env python3
"""将课小秘旧连接与租户路由配置最小化迁入 Skill 私有 runtime 文件。"""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


CONNECTION_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,63}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Migrate 课小秘 database connections into Skill/runtime/data-access.local.json."
    )
    parser.add_argument("--sql-config", type=Path, required=True)
    parser.add_argument("--tenant-config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--main-connection", default="LinkFitDataOnlyRead")
    parser.add_argument("--finance-prefix", default="TenantData")
    parser.add_argument("--finance-suffix", default="")
    parser.add_argument("--modulo", type=int, default=10)
    parser.add_argument("--command-timeout-seconds", type=int, default=5)
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"配置文件不存在: {path}")
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"配置文件根节点必须是对象: {path}")
    return payload


def connection_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    section = payload.get("ConnectionConfig")
    items = section.get("Connections") if isinstance(section, dict) else None
    if not isinstance(items, list):
        raise ValueError("SqlConnectionConfig.json 缺少 ConnectionConfig.Connections")
    return [item for item in items if isinstance(item, dict)]


def route_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    section = payload.get("ConnectionConfig")
    items = section.get("Connections") if isinstance(section, dict) else None
    if not isinstance(items, list):
        raise ValueError("TenantConnectionConfig.json 缺少 ConnectionConfig.Connections")
    return [item for item in items if isinstance(item, dict)]


def require_name(value: Any, label: str) -> str:
    name = str(value or "").strip()
    if not CONNECTION_NAME.fullmatch(name):
        raise ValueError(f"{label}无效")
    return name


def main() -> int:
    args = parse_args()
    if args.output.name != "data-access.local.json" or args.output.parent.name != "runtime":
        raise ValueError("输出必须是产品 Skill/runtime/data-access.local.json")
    if args.modulo < 1 or args.modulo > 100:
        raise ValueError("modulo 必须在 1 到 100 之间")

    sql_payload = read_json(args.sql_config)
    tenant_payload = read_json(args.tenant_config)
    source_connections: dict[str, dict[str, Any]] = {}
    for item in connection_items(sql_payload):
        name = require_name(item.get("Name"), "连接名")
        if name.lower() in source_connections:
            raise ValueError(f"存在重复连接名: {name}")
        source_connections[name.lower()] = item

    main_name = require_name(args.main_connection, "主库连接名")
    prefix = require_name(args.finance_prefix, "财务连接前缀")
    if args.finance_suffix and not re.fullmatch(r"[A-Za-z0-9_]{1,16}", args.finance_suffix):
        raise ValueError("财务连接后缀无效")

    routes: list[dict[str, Any]] = []
    needed_names = {main_name}
    for item in route_items(tenant_payload):
        source_name = require_name(item.get("ConnectionName"), "租户路由连接名")
        target_name = require_name(source_name + args.finance_suffix, "租户目标连接名")
        needed_names.add(target_name)
        routes.append(
            {
                "tenantId": int(item.get("TenantId") or 0),
                "minTenantId": int(item.get("MinTenantId") or 0),
                "maxTenantId": int(item.get("MaxTenantId") or 0),
                "connectionName": target_name,
            }
        )

    for index in range(args.modulo):
        needed_names.add(require_name(f"{prefix}{index}{args.finance_suffix}", "财务回退连接名"))

    connections: list[dict[str, str]] = []
    for name in sorted(needed_names, key=str.lower):
        source = source_connections.get(name.lower())
        if source is None:
            raise ValueError(f"SqlConnectionConfig.json 缺少所需连接: {name}")
        connection_string = str(source.get("ConnectionString") or "").strip()
        if not connection_string:
            raise ValueError(f"连接串为空: {name}")
        connections.append(
            {
                "name": name,
                "providerName": str(source.get("ProviderName") or "MySql"),
                "connectionString": connection_string,
            }
        )

    output_payload = {
        "schemaVersion": 1,
        "productCode": "kexiaomi",
        "mainConnectionName": main_name,
        "connections": connections,
        "tenantRoutes": routes,
        "financeFallback": {
            "modulo": args.modulo,
            "connectionNameTemplate": f"{prefix}{{index}}{args.finance_suffix}",
        },
        "executionPolicy": {
            "readOnly": True,
            "commandTimeoutSeconds": args.command_timeout_seconds,
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
            json.dump(output_payload, temporary, ensure_ascii=False, indent=2)
            temporary.write("\n")
        os.chmod(temporary_path, 0o600)
        os.replace(temporary_path, args.output)
        os.chmod(args.output, 0o600)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()

    # 只输出连接数量与目标文件，不输出任何连接值。
    print(json.dumps({"connections": len(connections), "routes": len(routes), "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
