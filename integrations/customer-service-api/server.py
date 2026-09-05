#!/usr/bin/env python3
"""Expose one DeepSeek Harness customer-service turn as a small HTTP API."""

from __future__ import annotations

import base64
import binascii
import json
import os
import re
import sys
import threading
import uuid
from dataclasses import dataclass, field
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_SDK = REPO_ROOT / "python" / "sdk" / "src"
if SOURCE_SDK.is_dir():
    sys.path.insert(0, str(SOURCE_SDK))

from deepseek_harness import DeepSeekHarness  # noqa: E402


SUPPORTED_IMAGE_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/gif",
}
ALLOWED_ACTIONS = {"answer", "ask", "handoff"}
BUSINESS_DATA_MODES = {"Database", "ApiMcp"}
MEMBER_MOBILE_PATTERN = re.compile(r"(?<!\d)(1[3-9]\d{9})(?!\d)")
MEMBER_MOBILE_PLACEHOLDER = "[已提供会员手机号]"


class RequestError(ValueError):
    """A client request failed deterministic HTTP input validation."""


@dataclass(frozen=True, slots=True)
class ModelConfig:
    """Model route loaded from the server-owned JSON file rather than DuckAI."""

    provider: str
    model: str
    display_name: str
    base_url: str
    api_key: str = field(repr=False)
    business_data_mode: str
    api_mcp_url: str
    api_mcp_tool_call_timeout_milliseconds: int
    api_mcp_fail_on_startup_error: bool
    database_max_catalog_tables: int
    context_window: int
    max_output_tokens: int
    reasoning_effort: str | None
    request_max_tokens: int | None
    timeout_milliseconds: int

    @classmethod
    def from_file(cls, path: Path) -> "ModelConfig":
        """Read one strict model file and reject missing values or misspelled keys."""
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"model config does not exist: {path}; copy customer-service.model.example.json first"
            ) from exc
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"model config must be readable UTF-8 JSON: {path}") from exc
        if not isinstance(payload, dict):
            raise RuntimeError("model config root must be a JSON object")

        allowed_keys = {
            "provider",
            "model",
            "displayName",
            "baseUrl",
            "apiKey",
            "businessDataMode",
            "apiMcpUrl",
            "apiMcpToolCallTimeoutMilliseconds",
            "apiMcpFailOnStartupError",
            "databaseMaxCatalogTables",
            "contextWindow",
            "maxOutputTokens",
            "reasoningEffort",
            "requestMaxTokens",
            "timeoutMilliseconds",
        }
        unknown_keys = sorted(set(payload) - allowed_keys)
        if unknown_keys:
            raise RuntimeError(f"model config contains unknown keys: {', '.join(unknown_keys)}")

        provider = _model_string(payload, "provider")
        if provider != "qwen-standard-cn":
            raise RuntimeError("model config provider must be qwen-standard-cn for this profile")
        business_data_mode = _model_string(payload, "businessDataMode")
        if business_data_mode not in BUSINESS_DATA_MODES:
            raise RuntimeError("model config businessDataMode must be Database or ApiMcp")
        api_mcp_tool_call_timeout_milliseconds = _model_positive_int(
            payload, "apiMcpToolCallTimeoutMilliseconds"
        )
        if not 1_000 <= api_mcp_tool_call_timeout_milliseconds <= 300_000:
            raise RuntimeError(
                "model config apiMcpToolCallTimeoutMilliseconds must be between 1000 and 300000"
            )
        database_max_catalog_tables = _model_positive_int(payload, "databaseMaxCatalogTables")
        if database_max_catalog_tables > 20:
            raise RuntimeError("model config databaseMaxCatalogTables must be between 1 and 20")
        reasoning_effort = payload.get("reasoningEffort", "high")
        if reasoning_effort is not None:
            reasoning_effort = _model_string(payload, "reasoningEffort")
            if reasoning_effort not in {"low", "medium", "high"}:
                raise RuntimeError("model config reasoningEffort must be low, medium, high, or null")

        request_max_tokens = payload.get("requestMaxTokens", 8192)
        if request_max_tokens is not None:
            request_max_tokens = _model_positive_int(payload, "requestMaxTokens")
        return cls(
            provider=provider,
            model=_model_string(payload, "model"),
            display_name=_model_string(payload, "displayName"),
            base_url=_model_string(payload, "baseUrl"),
            api_key=_model_string(payload, "apiKey"),
            business_data_mode=business_data_mode,
            api_mcp_url=_model_string(payload, "apiMcpUrl"),
            api_mcp_tool_call_timeout_milliseconds=api_mcp_tool_call_timeout_milliseconds,
            api_mcp_fail_on_startup_error=_model_boolean(payload, "apiMcpFailOnStartupError"),
            database_max_catalog_tables=database_max_catalog_tables,
            context_window=_model_positive_int(payload, "contextWindow"),
            max_output_tokens=_model_positive_int(payload, "maxOutputTokens"),
            reasoning_effort=reasoning_effort,
            request_max_tokens=request_max_tokens,
            timeout_milliseconds=_model_positive_int(payload, "timeoutMilliseconds"),
        )


@dataclass(frozen=True, slots=True)
class ApiConfig:
    """Process configuration shared by every customer-service request."""

    host: str
    port: int
    dsh_home: Path
    dsh_bin: Path
    patch_file: Path
    workspace: Path
    skill_dir: Path
    business_data_mode: str
    mcp_url: str
    mcp_tool_call_timeout_milliseconds: int
    mcp_fail_on_startup_error: bool
    database_max_catalog_tables: int
    model_base_url: str
    model_api_key: str = field(repr=False)
    provider: str
    model: str
    model_display_name: str
    model_context_window: int
    model_max_output_tokens: int
    model_timeout_milliseconds: int
    reasoning_effort: str | None
    max_tokens: int | None
    request_timeout_seconds: float
    max_request_bytes: int
    node_bin_dir: Path | None

    @classmethod
    def from_environment(cls) -> "ApiConfig":
        """Resolve deployment settings and reject missing runtime assets."""
        integration_root = Path(__file__).resolve().parent
        dsh_home_text = os.environ.get("DCS_DSH_HOME", "").strip()
        skill_dir_text = os.environ.get("DCS_SKILL_DIR", "").strip()
        workspace_text = os.environ.get("DCS_WORKSPACE", skill_dir_text).strip()
        if not dsh_home_text:
            raise RuntimeError("DCS_DSH_HOME must name an isolated Harness home")
        if not skill_dir_text:
            raise RuntimeError("DCS_SKILL_DIR must name the directory containing product skill bundles")
        if not workspace_text:
            raise RuntimeError("DCS_WORKSPACE or DCS_SKILL_DIR must name the Harness workspace")

        # 模型、推理参数和业务数据源只归 Harness 服务自己的文件管理，DuckAI 不持有这些配置。
        model_config_path = Path(
            os.environ.get(
                "DCS_MODEL_CONFIG_FILE",
                integration_root / "customer-service.model.json",
            )
        ).resolve()
        model_config = ModelConfig.from_file(model_config_path)

        dsh_bin = Path(os.environ.get("DCS_DSH_BIN", REPO_ROOT / "apps" / "cli" / "lib" / "bin.js")).resolve()
        patch_file = Path(os.environ.get("DCS_PATCH_FILE", integration_root / "customer-service.cordis.patch.yml")).resolve()
        skill_dir = Path(skill_dir_text).resolve()
        workspace = Path(workspace_text).resolve()
        for label, path in (
            ("DCS_DSH_BIN", dsh_bin),
            ("DCS_PATCH_FILE", patch_file),
            ("DCS_SKILL_DIR", skill_dir),
            ("DCS_WORKSPACE", workspace),
        ):
            if not path.exists():
                raise RuntimeError(f"{label} does not exist: {path}")

        dsh_home = Path(dsh_home_text).resolve()
        dsh_home.mkdir(parents=True, exist_ok=True)
        node_bin_text = os.environ.get("DCS_NODE_BIN_DIR", "").strip()
        host = os.environ.get("DCS_HOST", "127.0.0.1").strip() or "127.0.0.1"
        return cls(
            host=host,
            port=_positive_int("DCS_PORT", 8765),
            dsh_home=dsh_home,
            dsh_bin=dsh_bin,
            patch_file=patch_file,
            workspace=workspace,
            skill_dir=skill_dir,
            business_data_mode=model_config.business_data_mode,
            mcp_url=model_config.api_mcp_url,
            mcp_tool_call_timeout_milliseconds=(
                model_config.api_mcp_tool_call_timeout_milliseconds
            ),
            mcp_fail_on_startup_error=model_config.api_mcp_fail_on_startup_error,
            database_max_catalog_tables=model_config.database_max_catalog_tables,
            model_base_url=model_config.base_url,
            model_api_key=model_config.api_key,
            provider=model_config.provider,
            model=model_config.model,
            model_display_name=model_config.display_name,
            model_context_window=model_config.context_window,
            model_max_output_tokens=model_config.max_output_tokens,
            model_timeout_milliseconds=model_config.timeout_milliseconds,
            reasoning_effort=model_config.reasoning_effort,
            max_tokens=model_config.request_max_tokens,
            request_timeout_seconds=float(os.environ.get("DCS_REQUEST_TIMEOUT_SECONDS", "240")),
            max_request_bytes=_positive_int("DCS_MAX_REQUEST_BYTES", 25 * 1024 * 1024),
            node_bin_dir=Path(node_bin_text).resolve() if node_bin_text else None,
        )


def _positive_int(name: str, default: int) -> int:
    value = int(os.environ.get(name, str(default)))
    if value < 1:
        raise RuntimeError(f"{name} must be a positive integer")
    return value


def _model_string(payload: dict[str, Any], field_name: str) -> str:
    """Return a required trimmed model setting without ever logging its value."""
    value = payload.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(f"model config {field_name} must be a non-empty string")
    return value.strip()


def _model_positive_int(payload: dict[str, Any], field_name: str) -> int:
    """Return a required positive integer model setting; booleans are not integers here."""
    value = payload.get(field_name)
    if type(value) is not int or value < 1:
        raise RuntimeError(f"model config {field_name} must be a positive integer")
    return value


def _model_boolean(payload: dict[str, Any], field_name: str) -> bool:
    """Return a required JSON boolean without accepting integers or strings."""
    value = payload.get(field_name)
    if type(value) is not bool:
        raise RuntimeError(f"model config {field_name} must be a boolean")
    return value


def _required_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RequestError(f"{field} must be a non-empty string")
    return value.strip()


def _optional_string(value: Any, field: str) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise RequestError(f"{field} must be a string")
    return value.strip()


def parse_request(payload: Any) -> dict[str, Any]:
    """Validate the transport payload without making customer-service decisions."""
    if not isinstance(payload, dict):
        raise RequestError("request body must be a JSON object")
    context = payload.get("context") or {}
    mcp = payload.get("mcp") or {}
    attachments = payload.get("attachments") or []
    if not isinstance(context, dict):
        raise RequestError("context must be a JSON object")
    if not isinstance(mcp, dict):
        raise RequestError("mcp must be a JSON object")
    if not isinstance(attachments, list):
        raise RequestError("attachments must be a JSON array")

    normalized_attachments: list[dict[str, str]] = []
    for index, item in enumerate(attachments):
        if not isinstance(item, dict):
            raise RequestError(f"attachments[{index}] must be a JSON object")
        mime_type = _required_string(item.get("mimeType"), f"attachments[{index}].mimeType").lower()
        data = _required_string(item.get("data"), f"attachments[{index}].data")
        if mime_type not in SUPPORTED_IMAGE_MIME_TYPES:
            raise RequestError(f"attachments[{index}].mimeType is not a supported raster image")
        try:
            base64.b64decode(data, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise RequestError(f"attachments[{index}].data must be canonical base64") from exc
        normalized_attachments.append(
            {
                "mimeType": mime_type,
                "data": data,
                "fileName": _optional_string(item.get("fileName"), f"attachments[{index}].fileName"),
            }
        )

    return {
        "conversationId": _required_string(payload.get("conversationId"), "conversationId"),
        "messageId": _required_string(payload.get("messageId"), "messageId"),
        "message": _required_string(payload.get("message"), "message"),
        "productCode": _required_string(payload.get("productCode"), "productCode"),
        "entryPoint": _optional_string(payload.get("entryPoint"), "entryPoint"),
        "context": context,
        "mcp": mcp,
        "attachments": normalized_attachments,
    }


def _redact_model_value(value: Any) -> Any:
    """Remove recognized private values before they enter model-visible history."""
    if isinstance(value, str):
        return MEMBER_MOBILE_PATTERN.sub(MEMBER_MOBILE_PLACEHOLDER, value)
    if type(value) is int and MEMBER_MOBILE_PATTERN.fullmatch(str(value)):
        return MEMBER_MOBILE_PLACEHOLDER
    if isinstance(value, list):
        return [_redact_model_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _redact_model_value(item) for key, item in value.items()}
    return value


def build_prompt_blocks(request: dict[str, Any]) -> list[dict[str, Any]]:
    """Render redacted channel facts and inline images into one Harness turn."""
    metadata = _redact_model_value({
        "messageId": request["messageId"],
        "productCode": request["productCode"],
        "entryPoint": request["entryPoint"],
        "context": request["context"],
    })
    customer_message = _redact_model_value(request["message"])
    text = (
        "这是当前企业微信客服消息。通道元数据只提供上下文，不包含处理结论。\n"
        f"<channel_context>{json.dumps(metadata, ensure_ascii=False, separators=(',', ':'))}</channel_context>\n"
        f"<customer_message>{customer_message}</customer_message>\n"
        "请完整执行客服调查，并严格按系统要求输出最终 JSON。"
    )
    blocks: list[dict[str, Any]] = [{"type": "text", "text": text}]
    blocks.extend(
        {"type": "image", "data": item["data"], "mimeType": item["mimeType"]}
        for item in request["attachments"]
    )
    return blocks


def parse_agent_response(raw_response: str) -> dict[str, str]:
    """Require the model-owned decision to use the documented three-action JSON result."""
    text = (raw_response or "").strip()
    if text.startswith("```json") and text.endswith("```"):
        text = text[7:-3].strip()
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Harness final response is not valid JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("Harness final response must be a JSON object")
    expected_fields = {"action", "replyText", "reason"}
    if set(payload) != expected_fields:
        raise RuntimeError("Harness final response must contain exactly action, replyText, and reason")
    action = payload.get("action")
    reply_text = payload.get("replyText")
    reason = payload.get("reason")
    if action not in ALLOWED_ACTIONS:
        raise RuntimeError("Harness final response action must be answer, ask, or handoff")
    if not isinstance(reply_text, str) or (action != "handoff" and not reply_text.strip()):
        raise RuntimeError("Harness final response requires replyText for answer and ask")
    if not isinstance(reason, str):
        raise RuntimeError("Harness final response reason must be a string")
    return {"action": action, "replyText": reply_text.strip(), "reason": reason.strip()}


def _database_scope_verified(request: dict[str, Any]) -> bool:
    return request.get("context", {}).get("merchantProfileVerified") is True


def _business_data_tool_names(mode: str, database_scope_verified: bool = True) -> tuple[str, ...]:
    if mode == "Database":
        if not database_scope_verified:
            return ()
        return ("search_business_schema", "query_business_data")
    if mode == "ApiMcp":
        return ("search_capabilities", "invoke_capability")
    raise RuntimeError("businessDataMode must be Database or ApiMcp")


def _require_database_request_context(request: dict[str, Any]) -> None:
    context = request.get("context", {})
    if not _database_scope_verified(request):
        return
    if type(context.get("storeId")) is not int or context["storeId"] < 1:
        raise RequestError("context.storeId must be a positive integer in Database mode")
    if type(context.get("operatorUid")) is not int or context["operatorUid"] < 1:
        raise RequestError("context.operatorUid must be a positive integer in Database mode")


def _log_startup_configuration(config: ApiConfig) -> None:
    tools = ", ".join(_business_data_tool_names(config.business_data_mode))
    print("customer-service-api configuration:", file=sys.stderr)
    print(f"  businessDataMode: {config.business_data_mode}", file=sys.stderr)
    print(f"  activeBusinessDataTools: {tools}", file=sys.stderr)
    print(f"  patchFile: {config.patch_file}", file=sys.stderr)
    print(f"  skillDir: {config.skill_dir}", file=sys.stderr)
    print(f"  workspace: {config.workspace}", file=sys.stderr)
    print(f"  dshHome: {config.dsh_home}", file=sys.stderr)
    print(f"  dshBin: {config.dsh_bin}", file=sys.stderr)


class CustomerServiceRuntime:
    """Run isolated Harness processes while serializing access to one session store."""

    def __init__(self, config: ApiConfig) -> None:
        self._config = config
        self._lock = threading.Lock()

    def run(self, request: dict[str, Any]) -> dict[str, str]:
        """Execute one customer-service turn and return the Harness-owned decision."""
        if self._config.business_data_mode == "Database":
            _require_database_request_context(request)
        trace_id = f"dcs_{uuid.uuid4().hex}"
        environment = self._runtime_environment(request, trace_id)
        active_tools = ",".join(
            _business_data_tool_names(
                environment["DCS_BUSINESS_DATA_MODE"],
                environment["DCS_DATABASE_MERCHANT_VERIFIED"] == "true",
            )
        ) or "none"
        print(
            "customer-service-api run: "
            f"traceId={trace_id} "
            f"sessionId=customer-service-{request['conversationId']} "
            f"businessDataMode={environment['DCS_BUSINESS_DATA_MODE']} "
            f"activeBusinessDataTools={active_tools} "
            f"patchFile={self._config.patch_file}",
            file=sys.stderr,
        )
        with self._lock:
            with DeepSeekHarness(
                dsh_home=str(self._config.dsh_home),
                dsh_bin=str(self._config.dsh_bin),
                profile="sdk",
                patches=(str(self._config.patch_file),),
                cwd=str(self._config.workspace),
                runtime_cwd=str(REPO_ROOT),
                provider=self._config.provider,
                model=self._config.model,
                reasoning_effort=self._config.reasoning_effort,
                max_tokens=self._config.max_tokens,
                env=environment,
                request_timeout_seconds=self._config.request_timeout_seconds,
            ) as harness:
                result = harness.run(
                    build_prompt_blocks(request),
                    session_id=f"customer-service-{request['conversationId']}",
                )
        response = parse_agent_response(result.final_response)
        response.update(
            {
                "sessionId": result.session_id,
                "traceId": trace_id,
                "finishReason": result.finish_reason or "",
            }
        )
        return response

    def _runtime_environment(self, request: dict[str, Any], trace_id: str) -> dict[str, str]:
        mcp = request["mcp"]
        context = request.get("context", {})
        member_mobile_match = MEMBER_MOBILE_PATTERN.search(request.get("message", ""))
        environment = {
            "DCS_SKILL_DIR": str(self._config.skill_dir),
            "DCS_BUSINESS_DATA_MODE": self._config.business_data_mode,
            "DCS_DATABASE_PRODUCT_CODE": request["productCode"],
            "DCS_DATABASE_STORE_ID": str(context.get("storeId", "")),
            "DCS_DATABASE_OPERATOR_UID": str(context.get("operatorUid", "")),
            "DCS_DATABASE_MERCHANT_VERIFIED": (
                "true" if context.get("merchantProfileVerified") is True else "false"
            ),
            "DCS_DATABASE_MEMBER_MOBILE": (
                member_mobile_match.group(1) if member_mobile_match is not None else ""
            ),
            "DCS_MCP_URL": self._config.mcp_url,
            "DCS_MCP_TOOL_CALL_TIMEOUT_MILLISECONDS": str(
                self._config.mcp_tool_call_timeout_milliseconds
            ),
            "DCS_MCP_FAIL_ON_STARTUP_ERROR": (
                "true" if self._config.mcp_fail_on_startup_error else "false"
            ),
            "DCS_DATABASE_MAX_CATALOG_TABLES": str(self._config.database_max_catalog_tables),
            "DCS_MODEL_BASE_URL": self._config.model_base_url,
            "DCS_MODEL_ID": self._config.model,
            "DCS_MODEL_DISPLAY_NAME": self._config.model_display_name,
            "DCS_MODEL_CONTEXT_WINDOW": str(self._config.model_context_window),
            "DCS_MODEL_MAX_OUTPUT_TOKENS": str(self._config.model_max_output_tokens),
            "DCS_MODEL_TIMEOUT_MILLISECONDS": str(self._config.model_timeout_milliseconds),
            "DASHSCOPE_API_KEY": self._config.model_api_key,
            "DCS_MCP_SERVICE_KEY": _optional_string(mcp.get("serviceKey"), "mcp.serviceKey"),
            "DCS_MCP_CALLER_ID": _optional_string(mcp.get("callerId"), "mcp.callerId"),
            "DCS_MCP_CONVERSATION_ID": _optional_string(
                mcp.get("conversationId"), "mcp.conversationId"
            ) or request["conversationId"],
            "DCS_MCP_PRODUCT_CODE": request["productCode"],
            "DCS_MCP_PERSPECTIVE": _optional_string(mcp.get("perspective"), "mcp.perspective") or "merchant",
            "DCS_MCP_SECURE_CONTEXT": _optional_string(mcp.get("secureContext"), "mcp.secureContext"),
            "DCS_MCP_ALLOW_MINIMUM_DATA": _optional_string(
                mcp.get("allowMinimumData"), "mcp.allowMinimumData"
            ) or "false",
            "DCS_MCP_CUSTOMER_SUBJECT_GRANT": _optional_string(
                mcp.get("customerSubjectGrant"), "mcp.customerSubjectGrant"
            ),
            "DCS_MCP_REQUEST_ID": trace_id.removeprefix("dcs_"),
            "DSH_PERMISSION_MODE": "read-only",
            "DSH_TELEMETRY_DISABLED": "1",
        }
        if self._config.node_bin_dir is not None:
            environment["PATH"] = str(self._config.node_bin_dir) + os.pathsep + os.environ.get("PATH", "")
        return environment


class CustomerServiceHttpServer(ThreadingHTTPServer):
    """HTTP listener carrying immutable config and the Harness runtime adapter."""

    def __init__(self, config: ApiConfig) -> None:
        super().__init__((config.host, config.port), CustomerServiceRequestHandler)
        self.config = config
        self.runtime = CustomerServiceRuntime(config)


class CustomerServiceRequestHandler(BaseHTTPRequestHandler):
    """Handle health checks and customer-service run requests."""

    server: CustomerServiceHttpServer

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health/live":
            self._write_json(HTTPStatus.OK, {"status": "ok"})
            return
        self._write_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/customer-service/run":
            self._write_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        try:
            request = parse_request(self._read_json_body())
            response = self.server.runtime.run(request)
        except RequestError as exc:
            self.log_error("invalid customer-service request: %s", exc)
            self._write_json(HTTPStatus.BAD_REQUEST, {"error": "invalid_request", "message": str(exc)})
            return
        except Exception as exc:  # The HTTP process stays alive after one failed Harness turn.
            self.log_error("customer-service run failed: %s", exc)
            self._write_json(
                HTTPStatus.BAD_GATEWAY,
                {"error": "harness_run_failed", "message": str(exc)},
            )
            return
        self._write_json(HTTPStatus.OK, response)

    def _read_json_body(self) -> Any:
        content_length = self.headers.get("Content-Length")
        if content_length is None:
            raise RequestError("Content-Length is required")
        try:
            length = int(content_length)
        except ValueError as exc:
            raise RequestError("Content-Length must be an integer") from exc
        if length < 1 or length > self.server.config.max_request_bytes:
            raise RequestError("request body size is outside the configured limit")
        try:
            return json.loads(self.rfile.read(length))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RequestError("request body must be valid UTF-8 JSON") from exc

    def _write_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write("customer-service-api: " + (format % args) + "\n")


def main() -> None:
    """Start the blocking HTTP listener until SIGINT or SIGTERM stops the process."""
    config = ApiConfig.from_environment()
    _log_startup_configuration(config)
    server = CustomerServiceHttpServer(config)
    print(f"customer-service-api listening on http://{config.host}:{config.port}", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        # 本地联调使用 Ctrl+C 结束时正常关闭监听器，不输出与故障相同的堆栈。
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
