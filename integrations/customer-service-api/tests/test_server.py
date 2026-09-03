"""Deterministic tests for the customer-service HTTP transport adapter."""

from __future__ import annotations

import base64
import importlib.util
import json
import sys
from pathlib import Path

import pytest


SERVER_PATH = Path(__file__).resolve().parents[1] / "server.py"
PATCH_PATH = Path(__file__).resolve().parents[1] / "customer-service.cordis.patch.yml"
SPEC = importlib.util.spec_from_file_location("customer_service_api_server", SERVER_PATH)
assert SPEC is not None and SPEC.loader is not None
SERVER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SERVER
SPEC.loader.exec_module(SERVER)


def test_customer_service_profile_mounts_time_and_host_owned_capability_broker() -> None:
    """Keep relative dates and trusted MCP invocation state in the shipped profile."""
    patch = PATCH_PATH.read_text(encoding="utf-8")

    assert "name: '@deepseek-ai/dsh-time-context'" in patch
    assert "timeZone: Asia/Shanghai" in patch
    assert "refreshIntervalMs: 60000" in patch
    assert "capabilityBroker:" in patch
    assert "searchToolName: search_capabilities" in patch
    assert "invokeToolName: invoke_capability" in patch


def valid_model_config() -> dict[str, object]:
    """Return one complete model file without coupling tests to a real credential."""
    return {
        "provider": "qwen-standard-cn",
        "model": "qwen3.8-max",
        "displayName": "Qwen 3.8 Max",
        "baseUrl": "https://model.example.test/v1",
        "apiKey": "test-only-key",
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
    assert config.reasoning_effort == "high"
    assert config.request_max_tokens == 8192
    assert "test-only-key" not in repr(config)


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"apiKey": ""}, "apiKey must be a non-empty string"),
        ({"unexpectedSetting": True}, "unknown keys"),
        ({"provider": "another-provider"}, "must be qwen-standard-cn"),
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

    config = SERVER.ApiConfig.from_environment()
    environment = SERVER.CustomerServiceRuntime(config)._runtime_environment(
        {
            "conversationId": "conversation-1",
            "productCode": "kxm_pc",
            "mcp": {},
        },
        "dcs_trace1",
    )

    assert config.model == "qwen3.8-max"
    assert environment["DCS_MODEL_ID"] == "qwen3.8-max"
    assert environment["DCS_MODEL_CONTEXT_WINDOW"] == "131072"
    assert environment["DASHSCOPE_API_KEY"] == "test-only-key"
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
