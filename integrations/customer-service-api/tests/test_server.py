"""Deterministic tests for the customer-service HTTP transport adapter."""

from __future__ import annotations

import base64
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


SERVER_PATH = Path(__file__).resolve().parents[1] / "server.py"
PATCH_PATH = Path(__file__).resolve().parents[1] / "customer-service.cordis.patch.yml"
SPEC = importlib.util.spec_from_file_location("customer_service_api_server", SERVER_PATH)
assert SPEC is not None and SPEC.loader is not None
SERVER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SERVER
SPEC.loader.exec_module(SERVER)


def test_customer_service_profile_mounts_time_and_mutually_exclusive_data_sources() -> None:
    """Keep relative dates and publish only the selected business-data tool pair."""
    patch = PATCH_PATH.read_text(encoding="utf-8")

    assert "name: '@deepseek-ai/dsh-time-context'" in patch
    assert "timeZone: Asia/Shanghai" in patch
    assert "refreshIntervalMs: 60000" in patch
    assert "capabilityBroker:" in patch
    assert "searchToolName: search_capabilities" in patch
    assert "invokeToolName: invoke_capability" in patch
    assert "name: '@deepseek-ai/dsh-customer-service-database'" in patch
    assert "process.env.DCS_BUSINESS_DATA_MODE !== 'ApiMcp'" in patch
    assert "process.env.DCS_BUSINESS_DATA_MODE !== 'Database'" in patch
    assert "process.env.DCS_DATABASE_MERCHANT_VERIFIED !== 'true'" in patch
    assert "不得按固定问法、关键词、页面、表、接口或答案编排分支" in patch
    assert "实时结论必须由本轮成功观察明确绑定对象、属性、值、适用范围或时间" in patch
    assert "业务数据工具能力只来自本轮可见工具和本轮成功观察" in patch
    assert "API-MCP 调用能力" not in patch
    assert "失败调用不得原样重复" in patch
    assert "Number(process.env.DCS_MCP_TOOL_CALL_TIMEOUT_MILLISECONDS)" in patch
    assert "process.env.DCS_MCP_FAIL_ON_STARTUP_ERROR === 'true'" in patch
    assert "Number(process.env.DCS_DATABASE_MAX_CATALOG_TABLES)" in patch


def valid_model_config() -> dict[str, object]:
    """Return one complete model file without coupling tests to a real credential."""
    return {
        "provider": "qwen-standard-cn",
        "model": "qwen3.8-max",
        "displayName": "Qwen 3.8 Max",
        "baseUrl": "https://model.example.test/v1",
        "apiKey": "test-only-key",
        "businessDataMode": "ApiMcp",
        "apiMcpUrl": "http://mcp.example.test/mcp",
        "apiMcpToolCallTimeoutMilliseconds": 45000,
        "apiMcpFailOnStartupError": False,
        "databaseMaxCatalogTables": 6,
        "contextWindow": 131072,
        "maxOutputTokens": 16384,
        "reasoningEffort": "high",
        "requestMaxTokens": 8192,
        "timeoutMilliseconds": 180000,
    }


def test_model_config_loads_all_runtime_model_settings(tmp_path: Path) -> None:
    config_path = tmp_path / "customer-service.model.json"
    config_path.write_text(json.dumps(valid_model_config()), encoding="utf-8")

    config = SERVER.ModelConfig.from_file(config_path)

    assert config.provider == "qwen-standard-cn"
    assert config.model == "qwen3.8-max"
    assert config.business_data_mode == "ApiMcp"
    assert config.api_mcp_url == "http://mcp.example.test/mcp"
    assert config.api_mcp_tool_call_timeout_milliseconds == 45000
    assert config.api_mcp_fail_on_startup_error is False
    assert config.database_max_catalog_tables == 6
    assert config.reasoning_effort == "high"
    assert config.request_max_tokens == 8192
    assert "test-only-key" not in repr(config)


def test_api_config_rejects_unknown_business_data_mode(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    model_path = tmp_path / "customer-service.model.json"
    payload = valid_model_config()
    payload["businessDataMode"] = "Both"
    model_path.write_text(json.dumps(payload), encoding="utf-8")
    skill_dir = tmp_path / "skills"
    skill_dir.mkdir()
    monkeypatch.setenv("DCS_DSH_HOME", str(tmp_path / "dsh-home"))
    monkeypatch.setenv("DCS_DSH_BIN", str(SERVER_PATH))
    monkeypatch.setenv("DCS_PATCH_FILE", str(SERVER_PATH))
    monkeypatch.setenv("DCS_SKILL_DIR", str(skill_dir))
    monkeypatch.setenv("DCS_MODEL_CONFIG_FILE", str(model_path))

    with pytest.raises(RuntimeError, match="businessDataMode must be Database or ApiMcp"):
        SERVER.ApiConfig.from_environment()


def test_api_config_allows_non_loopback_database_listener(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    model_path = tmp_path / "customer-service.model.json"
    payload = valid_model_config()
    payload["businessDataMode"] = "Database"
    model_path.write_text(json.dumps(payload), encoding="utf-8")
    skill_dir = tmp_path / "skills"
    skill_dir.mkdir()
    monkeypatch.setenv("DCS_DSH_HOME", str(tmp_path / "dsh-home"))
    monkeypatch.setenv("DCS_DSH_BIN", str(SERVER_PATH))
    monkeypatch.setenv("DCS_PATCH_FILE", str(SERVER_PATH))
    monkeypatch.setenv("DCS_SKILL_DIR", str(skill_dir))
    monkeypatch.setenv("DCS_MODEL_CONFIG_FILE", str(model_path))
    monkeypatch.setenv("DCS_BUSINESS_DATA_MODE", "ApiMcp")
    monkeypatch.setenv("DCS_HOST", "0.0.0.0")

    config = SERVER.ApiConfig.from_environment()

    assert config.host == "0.0.0.0"
    assert config.business_data_mode == "Database"


def test_database_mode_injects_trusted_scope_and_current_message_mobile(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    model_path = tmp_path / "customer-service.model.json"
    payload = valid_model_config()
    payload["businessDataMode"] = "Database"
    model_path.write_text(json.dumps(payload), encoding="utf-8")
    skill_dir = tmp_path / "skills"
    skill_dir.mkdir()
    monkeypatch.setenv("DCS_DSH_HOME", str(tmp_path / "dsh-home"))
    monkeypatch.setenv("DCS_DSH_BIN", str(SERVER_PATH))
    monkeypatch.setenv("DCS_PATCH_FILE", str(SERVER_PATH))
    monkeypatch.setenv("DCS_SKILL_DIR", str(skill_dir))
    monkeypatch.setenv("DCS_MODEL_CONFIG_FILE", str(model_path))
    config = SERVER.ApiConfig.from_environment()

    environment = SERVER.CustomerServiceRuntime(config)._runtime_environment(
        {
            "conversationId": "conversation-1",
            "productCode": "kxm_pc",
            "message": "会员手机号是 13800138000，请帮我查卡",
            "context": {
                "storeId": 12,
                "operatorUid": 34,
                "merchantProfileVerified": True,
            },
            "mcp": {},
        },
        "dcs_trace1",
    )

    assert environment["DCS_BUSINESS_DATA_MODE"] == "Database"
    assert environment["DCS_DATABASE_STORE_ID"] == "12"
    assert environment["DCS_DATABASE_OPERATOR_UID"] == "34"
    assert environment["DCS_DATABASE_MERCHANT_VERIFIED"] == "true"
    assert environment["DCS_DATABASE_MEMBER_MOBILE"] == "13800138000"


@pytest.mark.parametrize(
    ("context", "message"),
    [
        ({"storeId": "12", "operatorUid": 34, "merchantProfileVerified": True}, "context.storeId must be a positive integer"),
        ({"storeId": 12, "operatorUid": True, "merchantProfileVerified": True}, "context.operatorUid must be a positive integer"),
    ],
)
def test_database_mode_rejects_invalid_verified_transport_scope(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    context: dict[str, object],
    message: str,
) -> None:
    model_path = tmp_path / "customer-service.model.json"
    payload = valid_model_config()
    payload["businessDataMode"] = "Database"
    model_path.write_text(json.dumps(payload), encoding="utf-8")
    skill_dir = tmp_path / "skills"
    skill_dir.mkdir()
    monkeypatch.setenv("DCS_DSH_HOME", str(tmp_path / "dsh-home"))
    monkeypatch.setenv("DCS_DSH_BIN", str(SERVER_PATH))
    monkeypatch.setenv("DCS_PATCH_FILE", str(SERVER_PATH))
    monkeypatch.setenv("DCS_SKILL_DIR", str(skill_dir))
    monkeypatch.setenv("DCS_MODEL_CONFIG_FILE", str(model_path))
    config = SERVER.ApiConfig.from_environment()

    with pytest.raises(SERVER.RequestError, match=message):
        SERVER.CustomerServiceRuntime(config).run(
            {
                "conversationId": "conversation-1",
                "messageId": "message-1",
                "productCode": "kxm_pc",
                "entryPoint": "",
                "message": "查会员卡",
                "context": context,
                "mcp": {},
                "attachments": [],
            }
        )


@pytest.mark.parametrize("context", [{}, {"merchantProfileVerified": False}])
def test_database_mode_unverified_request_launches_without_business_data_tools(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    context: dict[str, object],
) -> None:
    model_path = tmp_path / "customer-service.model.json"
    payload = valid_model_config()
    payload["businessDataMode"] = "Database"
    model_path.write_text(json.dumps(payload), encoding="utf-8")
    skill_dir = tmp_path / "skills"
    skill_dir.mkdir()
    monkeypatch.setenv("DCS_DSH_HOME", str(tmp_path / "dsh-home"))
    monkeypatch.setenv("DCS_DSH_BIN", str(SERVER_PATH))
    monkeypatch.setenv("DCS_PATCH_FILE", str(SERVER_PATH))
    monkeypatch.setenv("DCS_SKILL_DIR", str(skill_dir))
    monkeypatch.setenv("DCS_MODEL_CONFIG_FILE", str(model_path))
    config = SERVER.ApiConfig.from_environment()
    captured: dict[str, object] = {}

    class FakeHarness:
        def __init__(self, **kwargs: object) -> None:
            captured.update(kwargs)

        def __enter__(self) -> "FakeHarness":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def run(self, blocks: object, session_id: str) -> object:
            return SimpleNamespace(
                final_response='{"action":"answer","replyText":"请从排课页面查看明天课程。","reason":"未核验商户范围，只能回答产品资料。"}',
                session_id=session_id,
                finish_reason="stop",
            )

    monkeypatch.setattr(SERVER, "DeepSeekHarness", FakeHarness)

    response = SERVER.CustomerServiceRuntime(config).run(
        {
            "conversationId": "conversation-1",
            "messageId": "message-1",
            "productCode": "kxm_pc",
            "entryPoint": "",
            "message": "明天排课怎么看",
            "context": context,
            "mcp": {},
            "attachments": [],
        }
    )

    environment = captured["env"]
    assert isinstance(environment, dict)
    assert environment["DCS_DATABASE_MERCHANT_VERIFIED"] == "false"
    assert response["action"] == "answer"
    stderr = capsys.readouterr().err
    assert "businessDataMode=Database" in stderr
    assert "activeBusinessDataTools=none" in stderr
    assert "search_business_schema" not in stderr


def test_request_handler_logs_bad_request_reason(
    capsys: pytest.CaptureFixture[str],
) -> None:
    captured: dict[str, object] = {}
    handler = object.__new__(SERVER.CustomerServiceRequestHandler)
    handler.path = "/v1/customer-service/run"
    handler._read_json_body = lambda: (_ for _ in ()).throw(  # type: ignore[method-assign]
        SERVER.RequestError("context.storeId must be a positive integer in Database mode")
    )
    handler._write_json = lambda status, payload: captured.update(  # type: ignore[method-assign]
        {"status": status, "payload": payload}
    )

    handler.do_POST()

    assert captured["status"] == SERVER.HTTPStatus.BAD_REQUEST
    assert captured["payload"] == {
        "error": "invalid_request",
        "message": "context.storeId must be a positive integer in Database mode",
    }
    assert (
        "invalid customer-service request: "
        "context.storeId must be a positive integer in Database mode"
    ) in capsys.readouterr().err


def test_database_mode_logs_and_launches_only_database_tools(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    model_path = tmp_path / "customer-service.model.json"
    payload = valid_model_config()
    payload["businessDataMode"] = "Database"
    model_path.write_text(json.dumps(payload), encoding="utf-8")
    skill_dir = tmp_path / "skills"
    skill_dir.mkdir()
    monkeypatch.setenv("DCS_DSH_HOME", str(tmp_path / "dsh-home"))
    monkeypatch.setenv("DCS_DSH_BIN", str(SERVER_PATH))
    monkeypatch.setenv("DCS_PATCH_FILE", str(SERVER_PATH))
    monkeypatch.setenv("DCS_SKILL_DIR", str(skill_dir))
    monkeypatch.setenv("DCS_MODEL_CONFIG_FILE", str(model_path))
    config = SERVER.ApiConfig.from_environment()
    captured: dict[str, object] = {}

    class FakeHarness:
        def __init__(self, **kwargs: object) -> None:
            captured.update(kwargs)

        def __enter__(self) -> "FakeHarness":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def run(self, blocks: object, session_id: str) -> object:
            return SimpleNamespace(
                final_response='{"action":"answer","replyText":"已确认","reason":""}',
                session_id=session_id,
                finish_reason="stop",
            )

    monkeypatch.setattr(SERVER, "DeepSeekHarness", FakeHarness)

    SERVER.CustomerServiceRuntime(config).run(
        {
            "conversationId": "conversation-1",
            "messageId": "message-1",
            "productCode": "kxm_pc",
            "entryPoint": "",
            "message": "查会员卡",
            "context": {
                "storeId": 12,
                "operatorUid": 34,
                "merchantProfileVerified": True,
            },
            "mcp": {},
            "attachments": [],
        }
    )

    environment = captured["env"]
    assert isinstance(environment, dict)
    assert environment["DCS_BUSINESS_DATA_MODE"] == "Database"
    stderr = capsys.readouterr().err
    assert "businessDataMode=Database" in stderr
    assert "activeBusinessDataTools=search_business_schema,query_business_data" in stderr
    assert "search_capabilities" not in stderr


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"apiKey": ""}, "apiKey must be a non-empty string"),
        ({"unexpectedSetting": True}, "unknown keys"),
        ({"provider": "another-provider"}, "must be qwen-standard-cn"),
        ({"apiMcpToolCallTimeoutMilliseconds": 999}, "must be between 1000 and 300000"),
        ({"apiMcpFailOnStartupError": "false"}, "must be a boolean"),
        ({"databaseMaxCatalogTables": 21}, "must be between 1 and 20"),
    ],
)
def test_model_config_rejects_unsafe_or_unsupported_values(
    tmp_path: Path,
    change: dict[str, object],
    message: str,
) -> None:
    payload = valid_model_config()
    payload.update(change)
    config_path = tmp_path / "customer-service.model.json"
    config_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(RuntimeError, match=message):
        SERVER.ModelConfig.from_file(config_path)


def test_api_config_injects_file_owned_model_values_into_runtime(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    model_path = tmp_path / "customer-service.model.json"
    model_path.write_text(json.dumps(valid_model_config()), encoding="utf-8")
    skill_dir = tmp_path / "skills"
    skill_dir.mkdir()
    monkeypatch.setenv("DCS_DSH_HOME", str(tmp_path / "dsh-home"))
    monkeypatch.setenv("DCS_DSH_BIN", str(SERVER_PATH))
    monkeypatch.setenv("DCS_PATCH_FILE", str(SERVER_PATH))
    monkeypatch.setenv("DCS_SKILL_DIR", str(skill_dir))
    monkeypatch.setenv("DCS_WORKSPACE", str(skill_dir))
    monkeypatch.setenv("DCS_MODEL_CONFIG_FILE", str(model_path))
    monkeypatch.setenv("DCS_MCP_URL", "http://legacy-env.example.test/mcp")

    config = SERVER.ApiConfig.from_environment()
    assert config.business_data_mode == "ApiMcp"
    environment = SERVER.CustomerServiceRuntime(config)._runtime_environment(
        {
            "conversationId": "conversation-1",
            "productCode": "kxm_pc",
            "mcp": {},
        },
        "dcs_trace1",
    )

    assert config.model == "qwen3.8-max"
    assert config.mcp_url == "http://mcp.example.test/mcp"
    assert environment["DCS_MODEL_ID"] == "qwen3.8-max"
    assert environment["DCS_MODEL_CONTEXT_WINDOW"] == "131072"
    assert environment["DASHSCOPE_API_KEY"] == "test-only-key"
    assert environment["DCS_MCP_URL"] == "http://mcp.example.test/mcp"
    assert environment["DCS_MCP_TOOL_CALL_TIMEOUT_MILLISECONDS"] == "45000"
    assert environment["DCS_MCP_FAIL_ON_STARTUP_ERROR"] == "false"
    assert environment["DCS_DATABASE_MAX_CATALOG_TABLES"] == "6"
    assert "test-only-key" not in repr(config)


def test_parse_request_preserves_transport_fields_and_image() -> None:
    request = SERVER.parse_request(
        {
            "conversationId": "conversation-1",
            "messageId": "message-1",
            "message": "会员卡为什么看不到？",
            "productCode": "kxm_pc",
            "entryPoint": "merchant",
            "context": {"storeId": 12},
            "mcp": {"perspective": "merchant"},
            "attachments": [
                {
                    "mimeType": "image/png",
                    "data": base64.b64encode(b"image-bytes").decode("ascii"),
                    "fileName": "screen.png",
                }
            ],
        }
    )

    assert request["message"] == "会员卡为什么看不到？"
    assert request["context"] == {"storeId": 12}
    assert request["attachments"][0]["mimeType"] == "image/png"


def test_build_prompt_blocks_redacts_mobile_from_message_and_context() -> None:
    request = SERVER.parse_request(
        {
            "conversationId": "conversation-1",
            "messageId": "message-1",
            "message": "会员手机号是 13800138000，请帮我确认",
            "productCode": "kxm_pc",
            "context": {
                "contact": "13800138001",
                "numericContact": 13800138002,
            },
        }
    )

    prompt = SERVER.build_prompt_blocks(request)[0]["text"]

    assert "13800138000" not in prompt
    assert "13800138001" not in prompt
    assert "13800138002" not in prompt
    assert prompt.count("[已提供会员手机号]") == 3
    assert request["message"] == "会员手机号是 13800138000，请帮我确认"


def test_parse_request_rejects_non_image_attachment() -> None:
    with pytest.raises(SERVER.RequestError, match="supported raster image"):
        SERVER.parse_request(
            {
                "conversationId": "conversation-1",
                "messageId": "message-1",
                "message": "请看附件",
                "productCode": "kxm_pc",
                "attachments": [
                    {
                        "mimeType": "application/pdf",
                        "data": base64.b64encode(b"pdf").decode("ascii"),
                    }
                ],
            }
        )


@pytest.mark.parametrize("action", ["answer", "ask", "handoff"])
def test_parse_agent_response_accepts_only_documented_actions(action: str) -> None:
    result = SERVER.parse_agent_response(
        '{"action":"%s","replyText":"%s","reason":""}'
        % (action, "" if action == "handoff" else "回复")
    )

    assert result["action"] == action


def test_parse_agent_response_rejects_free_form_text() -> None:
    with pytest.raises(RuntimeError, match="not valid JSON"):
        SERVER.parse_agent_response("普通文本")


@pytest.mark.parametrize(
    "response",
    [
        '{"action":"answer","replyText":"回复"}',
        '{"action":"answer","replyText":"回复","reason":"","references":[]}',
    ],
)
def test_parse_agent_response_requires_exact_output_fields(response: str) -> None:
    with pytest.raises(RuntimeError, match="exactly action, replyText, and reason"):
        SERVER.parse_agent_response(response)
