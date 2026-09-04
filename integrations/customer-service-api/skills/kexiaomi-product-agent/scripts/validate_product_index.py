#!/usr/bin/env python3
"""Validate the generated 课小秘 product index without printing indexed content."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REQUIRED_FIELDS = {
    "chunkId",
    "productCodes",
    "client",
    "domains",
    "headingPath",
    "part",
    "evidenceLevels",
    "entities",
    "apis",
    "sourceFile",
    "sourceSha256",
    "content",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--index", required=True, type=Path)
    args = parser.parse_args()

    source_hash = hashlib.sha256(args.source.read_bytes()).hexdigest()
    records = []
    for line_number, line in enumerate(args.index.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        record = json.loads(line)
        missing = REQUIRED_FIELDS.difference(record)
        if missing:
            raise ValueError(f"line {line_number} missing fields: {sorted(missing)}")
        if record["sourceSha256"] != source_hash:
            raise ValueError(f"line {line_number} source hash mismatch")
        if not record["content"] or not record["headingPath"]:
            raise ValueError(f"line {line_number} contains an empty chunk")
        records.append(record)

    if len(records) < 100:
        raise ValueError(f"index is unexpectedly small: {len(records)} records")
    clients = {record["client"] for record in records}
    required_clients = {"customer-mini-program", "business-mini-program", "pc-admin"}
    if not required_clients.issubset(clients):
        raise ValueError(f"missing client coverage: {sorted(required_clients.difference(clients))}")
    domains = {domain for record in records for domain in record["domains"]}
    required_domains = {"member-card", "reservation-waitlist", "staff-binding", "payment-refund"}
    if not required_domains.issubset(domains):
        raise ValueError(f"missing domain coverage: {sorted(required_domains.difference(domains))}")

    print(json.dumps({"records": len(records), "clients": len(clients), "domains": len(domains)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
