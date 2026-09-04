#!/usr/bin/env python3
"""Validate the 课小秘客服 evaluation assets and optionally score captured Agent traces."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


CASE_ID_PATTERN = re.compile(r"^(AF|PS)-\d{3}$")
SEMANTIC_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MOBILE_PATTERN = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
LEAK_PATTERNS = {
    "raw-sql": re.compile(r"\b(select|insert|update|delete|union)\b\s+", re.IGNORECASE),
    "scope-id": re.compile(r"\b(storeid|tenantid|operatoruid|userid|cardid|lessonid)\b", re.IGNORECASE),
    "physical-database": re.compile(r"\b(tenantdata\d*|nutbooking(?:_consumption)?)\b", re.IGNORECASE),
    "mobile": MOBILE_PATTERN,
}
ALLOWED_PRODUCTS = {"kxm_pc", "kxm_b_mp", "kxm_c_mp"}
ALLOWED_CATEGORIES = {"presales", "aftersales"}
ALLOWED_ACTIONS = {"ask", "answer", "tool", "handoff"}
ALLOWED_INTENTS = {"presales", "aftersales_guidance", "aftersales_diagnostic", "high_risk", "other"}
ALLOWED_TOOLS = {
    "store_overview", "subscription_status", "operator_access", "member_card_snapshot",
    "member_reservation_snapshot", "member_lesson_eligibility_snapshot", "operator_mobile_binding",
    "query_business_data", "mcp__lingke_api__search_capabilities", "mcp__lingke_api__invoke_capability",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read JSONL while retaining one concise source location for malformed records."""
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.name}:{line_number} 不是有效 JSON") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path.name}:{line_number} 必须是 JSON 对象")
        records.append(value)
    return records


def require(condition: bool, message: str) -> None:
    """Stop at the first broken invariant so CI output stays actionable."""
    if not condition:
        raise ValueError(message)


def string_list(value: Any, label: str) -> list[str]:
    """Return a non-empty list of non-empty strings."""
    require(isinstance(value, list) and value, f"{label} 必须是非空数组")
    require(all(isinstance(item, str) and item.strip() for item in value), f"{label} 包含空值或非字符串")
    return [item.strip() for item in value]


def validate_semantics(records: list[dict[str, Any]]) -> set[str]:
    """Validate reusable product reasoning records without prescribing scenario SQL."""
    require(len(records) >= 10, "产品调查语义层至少需要十个跨场景语义域")
    semantic_ids: set[str] = set()
    for record in records:
        semantic_id = str(record.get("semanticId") or "")
        require(SEMANTIC_ID_PATTERN.fullmatch(semantic_id) is not None, f"语义 ID 格式无效：{semantic_id}")
        require(semantic_id not in semantic_ids, f"重复语义 ID：{semantic_id}")
        semantic_ids.add(semantic_id)
        string_list(record.get("domains"), f"{semantic_id}.domains")
        intents = string_list(record.get("intents"), f"{semantic_id}.intents")
        require(set(intents) <= ALLOWED_INTENTS, f"{semantic_id} 包含未知意图")
        string_list(record.get("triggers"), f"{semantic_id}.triggers")
        string_list(record.get("entities"), f"{semantic_id}.entities")
        string_list(record.get("requiredContext"), f"{semantic_id}.requiredContext")
        string_list(record.get("evidenceRequirements"), f"{semantic_id}.evidenceRequirements")
        string_list(record.get("allowedConclusions"), f"{semantic_id}.allowedConclusions")
        string_list(record.get("evidenceBoundaries"), f"{semantic_id}.evidenceBoundaries")
        string_list(record.get("handoffConditions"), f"{semantic_id}.handoffConditions")
        dimensions = record.get("investigationDimensions")
        require(isinstance(dimensions, list) and len(dimensions) >= 3, f"{semantic_id} 至少需要三个调查维度")
        for index, dimension in enumerate(dimensions):
            require(isinstance(dimension, dict), f"{semantic_id}.investigationDimensions[{index}] 必须是对象")
            require(bool(str(dimension.get("fact") or "").strip()), f"{semantic_id} 调查维度缺少 fact")
            string_list(dimension.get("questions"), f"{semantic_id}.dimensions[{index}].questions")
            string_list(dimension.get("evidence"), f"{semantic_id}.dimensions[{index}].evidence")
            string_list(dimension.get("queryTerms"), f"{semantic_id}.dimensions[{index}].queryTerms")
    return semantic_ids


def validate_cases(records: list[dict[str, Any]], semantic_ids: set[str]) -> dict[str, dict[str, Any]]:
    """Validate coverage, privacy, product scope and expected policy contracts for every case."""
    require(30 <= len(records) <= 50, "客服评测集应保持在三十到五十条")
    cases: dict[str, dict[str, Any]] = {}
    categories = Counter()
    covered_semantics = Counter()
    for record in records:
        case_id = str(record.get("caseId") or "")
        require(CASE_ID_PATTERN.fullmatch(case_id) is not None, f"评测 caseId 格式无效：{case_id}")
        require(case_id not in cases, f"重复评测案例：{case_id}")
        cases[case_id] = record
        category = str(record.get("category") or "")
        require(category in ALLOWED_CATEGORIES, f"{case_id} category 无效")
        categories[category] += 1
        require(record.get("productCode") in ALLOWED_PRODUCTS, f"{case_id} 产品编码越界")
        message = str(record.get("userMessage") or "").strip()
        require(message, f"{case_id} 缺少用户问题")
        require(MOBILE_PATTERN.search(message) is None, f"{case_id} 包含疑似真实手机号")
        context = record.get("context")
        require(isinstance(context, dict), f"{case_id} 缺少会话上下文")
        require(isinstance(context.get("isMerchant"), bool), f"{case_id} isMerchant 必须是布尔值")
        require(isinstance(context.get("hasMemberMobile"), bool), f"{case_id} hasMemberMobile 必须是布尔值")
        expected = record.get("expected")
        require(isinstance(expected, dict), f"{case_id} 缺少 expected")
        require(expected.get("intent") in ALLOWED_INTENTS, f"{case_id} intent 无效")
        require(isinstance(expected.get("hasSpecificIssue"), bool), f"{case_id} hasSpecificIssue 必须是布尔值")
        actions = string_list(expected.get("acceptableActions"), f"{case_id}.acceptableActions")
        require(set(actions) <= ALLOWED_ACTIONS, f"{case_id} 包含未知 action")
        required_semantics = string_list(expected.get("requiredSemanticIds"), f"{case_id}.requiredSemanticIds")
        require(set(required_semantics) <= semantic_ids, f"{case_id} 引用未知产品语义")
        covered_semantics.update(required_semantics)
        string_list(expected.get("requiredEntities"), f"{case_id}.requiredEntities")
        string_list(expected.get("requiredEvidence"), f"{case_id}.requiredEvidence")
        string_list(expected.get("forbiddenClaims"), f"{case_id}.forbiddenClaims")
        require(isinstance(expected.get("requiresMemberMobile"), bool), f"{case_id} requiresMemberMobile 必须是布尔值")
        require(isinstance(expected.get("shouldTransfer"), bool), f"{case_id} shouldTransfer 必须是布尔值")
        if expected["requiresMemberMobile"] and not context["hasMemberMobile"]:
            require("ask" in actions, f"{case_id} 缺少手机号时必须允许先追问")
        if expected["shouldTransfer"]:
            require("handoff" in actions, f"{case_id} 需要人工但未允许 handoff")
        else:
            require("handoff" not in actions, f"{case_id} 不应转人工却允许 handoff")
        allowed_tools = expected.get("allowedTools")
        forbidden_tools = expected.get("forbiddenTools")
        require(isinstance(allowed_tools, list) and set(allowed_tools) <= ALLOWED_TOOLS, f"{case_id} allowedTools 越界")
        require(isinstance(forbidden_tools, list) and set(forbidden_tools) <= ALLOWED_TOOLS, f"{case_id} forbiddenTools 越界")
        require(not (set(allowed_tools) & set(forbidden_tools)), f"{case_id} 工具同时允许和禁止")
        if category == "presales":
            require(expected.get("intent") == "presales", f"{case_id} 售前案例意图不正确")
            require(expected.get("hasSpecificIssue") is False, f"{case_id} 售前案例不能标记为具体故障")
            require(not allowed_tools, f"{case_id} 售前案例不能调用业务工具")
    require(categories["aftersales"] >= 20, "售后评测案例不足二十条")
    require(categories["presales"] >= 10, "售前评测案例不足十条")
    missing_semantics = sorted(semantic_ids - set(covered_semantics))
    require(not missing_semantics, f"以下产品语义没有评测覆盖：{','.join(missing_semantics)}")
    return cases


def leak_tags(answer: str) -> list[str]:
    """Detect direct privacy, scope and implementation-detail leakage in user-facing text."""
    return [name for name, pattern in LEAK_PATTERNS.items() if pattern.search(answer or "")]


def score_results(results: list[dict[str, Any]], cases: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Score captured traces using deterministic policy checks rather than an LLM judge."""
    by_case: dict[str, dict[str, Any]] = {}
    for result in results:
        case_id = str(result.get("caseId") or "")
        require(case_id in cases, f"结果引用未知案例：{case_id}")
        require(case_id not in by_case, f"结果重复案例：{case_id}")
        by_case[case_id] = result

    failures: list[dict[str, Any]] = []
    metric_totals = Counter()
    metric_passed = Counter()
    for case_id, case in cases.items():
        expected = case["expected"]
        result = by_case.get(case_id)
        if result is None:
            failures.append({"caseId": case_id, "failures": ["missing-result"]})
            continue
        checks = {
            "intent": result.get("intent") == expected["intent"],
            "specific-issue": result.get("hasSpecificIssue") is expected["hasSpecificIssue"],
            "action": result.get("action") in expected["acceptableActions"],
            "transfer": result.get("shouldTransfer") is expected["shouldTransfer"],
            "tools": set(result.get("tools") or []) <= set(expected["allowedTools"])
                     and not (set(result.get("tools") or []) & set(expected["forbiddenTools"])),
            "semantics": set(expected["requiredSemanticIds"]) <= set(result.get("semanticIds") or []),
            "evidence": set(expected["requiredEvidence"]) <= set(result.get("evidenceKinds") or []),
            "guardrails": not (result.get("guardrailViolations") or [])
                          and not leak_tags(str(result.get("answer") or "")),
        }
        failed = []
        for metric, passed in checks.items():
            metric_totals[metric] += 1
            if passed:
                metric_passed[metric] += 1
            else:
                failed.append(metric)
        if failed:
            failures.append({"caseId": case_id, "failures": failed})

    total_checks = sum(metric_totals.values())
    passed_checks = sum(metric_passed.values())
    return {
        "caseCount": len(cases),
        "resultCount": len(results),
        "passedCases": len(cases) - len(failures),
        "failedCases": len(failures),
        "policyScore": round(passed_checks / total_checks, 4) if total_checks else 0,
        "metrics": {
            key: {
                "passed": metric_passed[key],
                "total": metric_totals[key],
                "rate": round(metric_passed[key] / metric_totals[key], 4) if metric_totals[key] else 0,
            }
            for key in sorted(metric_totals)
        },
        "failures": failures,
    }


def read_trace_journal(path: Path) -> list[dict[str, Any]]:
    """Read one trace JSONL file or every JSONL journal in a directory."""
    files = sorted(path.glob("*.jsonl")) if path.is_dir() else [path]
    require(bool(files), f"没有找到 trace journal：{path}")
    records: list[dict[str, Any]] = []
    for file in files:
        records.extend(read_jsonl(file))
    return records


def score_trace_journal(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Validate append-only ordering and aggregate operational Agent metrics."""
    traces: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        trace_id = str(record.get("traceId") or "")
        require(trace_id, "trace journal 事件缺少 traceId")
        traces.setdefault(trace_id, []).append(record)

    counters = Counter()
    token_totals = Counter()
    invalid_chains: list[str] = []
    action_totals = Counter()
    tool_error_codes = Counter()
    for trace_id, events in traces.items():
        events.sort(key=lambda item: int(item.get("sequence") or 0))
        previous_hash = ""
        valid_chain = True
        for expected_sequence, event in enumerate(events, start=1):
            if int(event.get("sequence") or 0) != expected_sequence:
                valid_chain = False
            if str(event.get("previousEventHash") or "") != previous_hash:
                valid_chain = False
            event_hash = str(event.get("eventHash") or "")
            if not event_hash:
                valid_chain = False
            previous_hash = event_hash

            stage = str(event.get("stage") or "")
            data = event.get("data") if isinstance(event.get("data"), dict) else {}
            counters[stage] += 1
            if stage == "agent.v2.completed":
                action_totals[str(data.get("action") or "unknown")] += 1
            if stage == "tool.completed" and not data.get("success", False):
                tool_error_codes[str(data.get("errorCode") or "UNCLASSIFIED")] += 1
            if stage in {
                "model.response", "grounding.completed", "plan.format_repair_completed",
                "plan.protocol_compact_recovery_completed",
            }:
                token_totals["prompt"] += int(data.get("promptTokens") or 0)
                token_totals["completion"] += int(data.get("completionTokens") or 0)
                token_totals["reasoning"] += int(data.get("reasoningTokens") or 0)
        if not valid_chain:
            invalid_chains.append(trace_id)

    turn_count = counters["turn.started"]
    completed = counters["agent.v2.completed"]
    fallbacks = counters["agent.v2.fallback"]
    tool_calls = counters["tool.started"]
    tool_failures = sum(tool_error_codes.values())
    return {
        "traceCount": len(traces),
        "eventCount": len(records),
        "hashChainsValid": not invalid_chains,
        "invalidHashChainTraceIds": invalid_chains,
        "turns": turn_count,
        "completedTurns": completed,
        "fallbackTurns": fallbacks,
        "completionRate": round(completed / turn_count, 4) if turn_count else 0,
        "fallbackRate": round(fallbacks / turn_count, 4) if turn_count else 0,
        "actions": dict(sorted(action_totals.items())),
        "toolCalls": tool_calls,
        "toolFailures": tool_failures,
        "toolFailureRate": round(tool_failures / tool_calls, 4) if tool_calls else 0,
        "toolErrorCodes": dict(sorted(tool_error_codes.items())),
        "planRejections": counters["plan.validation_failed"],
        "contextCompactions": sum(
            1 for item in records
            if item.get("stage") == "model.request"
            and isinstance(item.get("data"), dict)
            and (int(item["data"].get("compactedToolResults") or 0) > 0
                 or int(item["data"].get("removedHistoryMessages") or 0) > 0)
        ),
        "contextOverflowRecoveries": counters["model.context_overflow_recovery"],
        "tokens": {
            "prompt": token_totals["prompt"],
            "completion": token_totals["completion"],
            "reasoning": token_totals["reasoning"],
            "total": token_totals["prompt"] + token_totals["completion"],
            "averagePerTurn": round(
                (token_totals["prompt"] + token_totals["completion"]) / turn_count, 2
            ) if turn_count else 0,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skill-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="kexiaomi-product-agent 技能目录",
    )
    parser.add_argument("--results", type=Path, help="可选的 Agent 评测轨迹 JSONL")
    parser.add_argument(
        "--trace-journal",
        type=Path,
        help="可选的 V2 append-only trace JSONL 文件或目录，用于链完整性与运行指标统计",
    )
    parser.add_argument("--report", type=Path, help="可选的评分报告输出路径")
    args = parser.parse_args()

    semantics_path = args.skill_dir / "references" / "investigation-semantics.jsonl"
    cases_path = args.skill_dir / "references" / "evaluation" / "customer-service-evals.jsonl"
    require(semantics_path.is_file(), "缺少产品调查语义层")
    require(cases_path.is_file(), "缺少客服评测集")
    semantic_records = read_jsonl(semantics_path)
    case_records = read_jsonl(cases_path)
    semantic_ids = validate_semantics(semantic_records)
    cases = validate_cases(case_records, semantic_ids)
    summary: dict[str, Any] = {
        "valid": True,
        "semanticCount": len(semantic_records),
        "caseCount": len(case_records),
        "categoryCounts": dict(sorted(Counter(item["category"] for item in case_records).items())),
    }
    if args.results:
        summary["evaluation"] = score_results(read_jsonl(args.results), cases)
    if args.trace_journal:
        summary["operations"] = score_trace_journal(read_trace_journal(args.trace_journal))
    output = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
