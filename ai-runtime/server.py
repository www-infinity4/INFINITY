#!/usr/bin/env python3
"""Infinity local-first Gemma role gateway.

Standard-library-only HTTP service that presents one stable Infinity contract
over one or more OpenAI-compatible local inference endpoints (for example
llama-server). It proposes tools but never executes them.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "runtime-config.json"
ROLE_ENDPOINTS = {
    "/v1/reason": "REASONER",
    "/v1/tools": "TOOL_ROUTER",
    "/v1/moderate/image": "IMAGE_SAFETY",
    "/v1/moderate/text": "TEXT_SAFETY",
    "/v1/embed": "EMBEDDINGS",
}
SAFETY_ROLES = {"IMAGE_SAFETY", "TEXT_SAFETY"}
LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}


class RuntimeErrorResponse(Exception):
    def __init__(self, status: int, message: str, payload: dict[str, Any] | None = None):
        super().__init__(message)
        self.status = status
        self.message = message
        self.payload = payload or {}


class LocalGemmaRuntime:
    def __init__(self, config_path: str | Path = DEFAULT_CONFIG):
        self.config_path = Path(config_path)
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.roles = self.config.get("roles", {})
        self.local = self.config.get("localInference", {})
        self.default_base = os.environ.get(
            "INFINITY_GEMMA_BASE_URL",
            self.local.get("baseUrl", "http://127.0.0.1:8080/v1"),
        ).rstrip("/")
        self.timeout = float(os.environ.get(
            "INFINITY_GEMMA_TIMEOUT",
            self.local.get("timeoutSeconds", 60),
        ))
        tool_config = self.config.get("toolExecution", {})
        self.allowed_tools = set(tool_config.get("allowedTools", []))

    def role_config(self, role: str) -> dict[str, Any]:
        config = self.roles.get(role)
        if not isinstance(config, dict):
            raise RuntimeErrorResponse(500, f"Role {role} is not configured.")
        return config

    def role_base(self, role: str) -> str:
        config = self.role_config(role)
        env_name = "INFINITY_" + role + "_BASE_URL"
        return os.environ.get(
            env_name,
            config.get("upstreamBaseUrl", self.default_base),
        ).rstrip("/")

    def available_models(self, role: str, timeout: float | None = None) -> list[str]:
        result = self.upstream_json(role, "GET", "/models", timeout=timeout)
        return [
            str(item.get("id"))
            for item in result.get("data", [])
            if isinstance(item, dict) and item.get("id")
        ]

    def upstream_model(self, role: str) -> str:
        config = self.role_config(role)
        env_name = "INFINITY_" + role + "_MODEL"
        explicit = os.environ.get(env_name, config.get("upstreamModel", "AUTO"))
        if explicit and str(explicit).upper() != "AUTO":
            return str(explicit)
        available = self.available_models(role, timeout=min(self.timeout, 3))
        if not available:
            raise RuntimeErrorResponse(503, f"Local provider for {role} has no loaded model.")
        return available[0]

    def upstream_json(
        self,
        role: str,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        url = self.role_base(role) + path
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout or self.timeout) as response:
                raw = response.read().decode("utf-8")
                parsed = json.loads(raw) if raw else {}
                if not isinstance(parsed, dict):
                    raise ValueError("upstream response is not an object")
                return parsed
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, socket.timeout, ValueError) as exc:
            raise RuntimeErrorResponse(
                503,
                f"Local provider for {role} is unavailable.",
                {"role": role, "upstream": url, "detail": str(exc)},
            ) from exc

    def health(self) -> dict[str, Any]:
        role_states: dict[str, Any] = {}
        for role, config in self.roles.items():
            try:
                available = self.available_models(role, timeout=min(self.timeout, 3))
                if not available:
                    raise RuntimeErrorResponse(503, f"Local provider for {role} has no loaded model.")
                explicit = config.get("upstreamModel", "AUTO")
                resolved = available[0] if str(explicit).upper() == "AUTO" else str(explicit)
                role_states[role] = {
                    "ready": resolved in available,
                    "provider": config.get("provider"),
                    "configuredModel": config.get("model"),
                    "resolvedModel": resolved,
                    "availableModels": available,
                    "baseUrl": self.role_base(role),
                }
            except RuntimeErrorResponse as exc:
                role_states[role] = {
                    "ready": False,
                    "provider": config.get("provider"),
                    "configuredModel": config.get("model"),
                    "baseUrl": self.role_base(role),
                    "error": exc.message,
                    "failClosed": bool(config.get("failClosed")),
                }
        ready = all(state["ready"] for state in role_states.values())
        safety_ready = all(role_states.get(role, {}).get("ready") for role in SAFETY_ROLES)
        return {
            "schema": "infinity/ai-runtime-health/v1",
            "status": "READY" if ready else "DEGRADED",
            "localOnly": True,
            "hostedFallbackEnabled": bool(self.config.get("hostedFallback", {}).get("enabled")),
            "publicationAllowed": bool(safety_ready),
            "roles": role_states,
            "checkedAt": int(time.time()),
        }

    @staticmethod
    def input_text(payload: dict[str, Any]) -> str:
        value = payload.get("input", payload.get("text", ""))
        if isinstance(value, dict):
            value = value.get("text", "")
        text = str(value or "").strip()
        if not text:
            raise RuntimeErrorResponse(400, "A non-empty input is required.")
        return text

    def chat(
        self,
        role: str,
        messages: list[dict[str, Any]],
        temperature: float = 0.2,
        response_format: dict[str, Any] | None = None,
    ) -> tuple[str, dict[str, Any]]:
        config = self.role_config(role)
        body: dict[str, Any] = {
            "model": self.upstream_model(role),
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }
        if response_format:
            body["response_format"] = response_format
        result = self.upstream_json(role, "POST", "/chat/completions", body)
        try:
            content = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeErrorResponse(502, f"Local provider returned no {role} result.") from exc
        return str(content), result

    def reason(self, payload: dict[str, Any]) -> dict[str, Any]:
        text = self.input_text(payload)
        context = payload.get("context")
        system = (
            "You are the local Infinity REASONER. Preserve evidence labels: "
            "OBSERVED, INFERRED, EXTERNALLY_VERIFIED, and USER_DEFINED. "
            "Never claim external verification unless sources were supplied."
        )
        if context:
            system += "\nContext supplied by the application:\n" + json.dumps(context, ensure_ascii=False)
        content, raw = self.chat(
            "REASONER",
            [{"role": "system", "content": system}, {"role": "user", "content": text}],
            float(payload.get("temperature", 0.2)),
        )
        return {
            "schema": "infinity/reason-result/v1",
            "role": "REASONER",
            "model": raw.get("model", self.role_config("REASONER").get("model")),
            "output": content,
            "evidenceState": "INFERRED",
            "local": True,
        }

    @staticmethod
    def parse_json_object(text: str) -> dict[str, Any]:
        cleaned = text.strip()
        cleaned = re.sub(r"^\`\`\`(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*\`\`\`$", "", cleaned)
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
            if not match:
                raise RuntimeErrorResponse(502, "Tool router did not return a JSON object.")
            try:
                parsed = json.loads(match.group(0))
            except json.JSONDecodeError as exc:
                raise RuntimeErrorResponse(502, "Tool router returned invalid JSON.") from exc
        if not isinstance(parsed, dict):
            raise RuntimeErrorResponse(502, "Tool router result must be an object.")
        return parsed

    def validate_tool(self, proposal: dict[str, Any], request_tools: Any) -> dict[str, Any]:
        name = str(proposal.get("name", "")).strip()
        arguments = proposal.get("arguments", {})
        request_names = {
            item.get("name")
            for item in (request_tools if isinstance(request_tools, list) else [])
            if isinstance(item, dict) and item.get("name")
        }
        allowed = self.allowed_tools & request_names if request_names else self.allowed_tools
        if not name or name not in allowed:
            raise RuntimeErrorResponse(
                422,
                "Tool proposal is not allowlisted for this request.",
                {"proposedTool": name, "allowedTools": sorted(allowed)},
            )
        if not isinstance(arguments, dict):
            raise RuntimeErrorResponse(422, "Tool arguments must be an object.")
        return {"name": name, "arguments": arguments}

    def tools(self, payload: dict[str, Any]) -> dict[str, Any]:
        text = self.input_text(payload)
        tools = payload.get("tools", [])
        available = [
            item for item in tools
            if isinstance(item, dict) and item.get("name") in self.allowed_tools
        ]
        system = (
            "You are Infinity TOOL_ROUTER. Propose exactly one allowed tool and never execute it. "
            "Return only JSON: {\"name\":\"tool.name\",\"arguments\":{...}}.\n"
            "Allowed tool definitions:\n" + json.dumps(available, ensure_ascii=False)
        )
        content, raw = self.chat(
            "TOOL_ROUTER",
            [{"role": "system", "content": system}, {"role": "user", "content": text}],
            0.0,
            {"type": "json_object"},
        )
        proposal = self.validate_tool(self.parse_json_object(content), available)
        return {
            "schema": "infinity/tool-proposal/v1",
            "role": "TOOL_ROUTER",
            "model": raw.get("model", self.role_config("TOOL_ROUTER").get("model")),
            "proposal": proposal,
            "executed": False,
            "requiresApplicationValidation": True,
            "local": True,
        }

    @staticmethod
    def normalize_decision(value: Any) -> str:
        decision = str(value or "").upper().strip()
        return decision if decision in {"APPROVED", "BLOCKED", "REVIEW_REQUIRED"} else "REVIEW_REQUIRED"

    def moderate(self, role: str, payload: dict[str, Any]) -> dict[str, Any]:
        system = (
            "You are an Infinity publication safety gate. Return JSON only: "
            "{\"decision\":\"APPROVED|BLOCKED|REVIEW_REQUIRED\",\"reasons\":[\"...\"]}. "
            "When uncertain choose REVIEW_REQUIRED."
        )
        if role == "TEXT_SAFETY":
            user_content: Any = self.input_text(payload)
        else:
            image = payload.get("image")
            if not image:
                raise RuntimeErrorResponse(400, "An image data URL or local-runtime image reference is required.")
            user_content = [
                {"type": "text", "text": str(payload.get("prompt", "Review this image for public publication."))},
                {"type": "image_url", "image_url": {"url": str(image)}},
            ]
        try:
            content, raw = self.chat(
                role,
                [{"role": "system", "content": system}, {"role": "user", "content": user_content}],
                0.0,
                {"type": "json_object"},
            )
            parsed = self.parse_json_object(content)
            decision = self.normalize_decision(parsed.get("decision"))
            reasons = parsed.get("reasons", [])
            if not isinstance(reasons, list):
                reasons = [str(reasons)]
            return {
                "schema": "infinity/moderation-result/v1",
                "role": role,
                "model": raw.get("model", self.role_config(role).get("model")),
                "decision": decision,
                "reasons": [str(item) for item in reasons],
                "failClosed": True,
                "local": True,
            }
        except RuntimeErrorResponse as exc:
            if exc.status < 500:
                raise
            return {
                "schema": "infinity/moderation-result/v1",
                "role": role,
                "decision": "REVIEW_REQUIRED",
                "reasons": [exc.message],
                "failClosed": True,
                "local": True,
                "providerReady": False,
            }

    def embed(self, payload: dict[str, Any]) -> dict[str, Any]:
        input_value = payload.get("input")
        if not isinstance(input_value, (str, list)) or input_value == "" or input_value == []:
            raise RuntimeErrorResponse(400, "Embedding input must be a non-empty string or list.")
        config = self.role_config("EMBEDDINGS")
        result = self.upstream_json(
            "EMBEDDINGS",
            "POST",
            "/embeddings",
            {"model": self.upstream_model("EMBEDDINGS"), "input": input_value},
        )
        return {
            "schema": "infinity/embedding-result/v1",
            "role": "EMBEDDINGS",
            "model": result.get("model", config.get("model")),
            "data": result.get("data", []),
            "local": True,
        }

    def dispatch(self, path: str, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        role = ROLE_ENDPOINTS.get(path)
        if not role:
            raise RuntimeErrorResponse(404, "Unknown endpoint.")
        if role == "REASONER":
            return 200, self.reason(payload)
        if role == "TOOL_ROUTER":
            return 200, self.tools(payload)
        if role in SAFETY_ROLES:
            result = self.moderate(role, payload)
            return (200 if result.get("providerReady", True) else 503), result
        return 200, self.embed(payload)


class InfinityAIHandler(BaseHTTPRequestHandler):
    server_version = "InfinityAI/1.0"

    def log_message(self, fmt: str, *args: Any) -> None:
        if os.environ.get("INFINITY_AI_QUIET") != "1":
            super().log_message(fmt, *args)

    def headers_json(self, status: int) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", os.environ.get("INFINITY_AI_ALLOW_ORIGIN", "*"))
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def write_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", os.environ.get("INFINITY_AI_ALLOW_ORIGIN", "*"))
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self.headers_json(204)

    def do_GET(self) -> None:
        if self.path.rstrip("/") != "/v1/health":
            self.write_json(404, {"error": "Unknown endpoint."})
            return
        self.write_json(200, self.server.runtime.health())

    def do_POST(self) -> None:
        try:
            max_bytes = int(self.server.runtime.config.get("server", {}).get("maxRequestBytes", 10_485_760))
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > max_bytes:
                raise RuntimeErrorResponse(413 if length > max_bytes else 400, "Invalid request size.")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(payload, dict):
                raise RuntimeErrorResponse(400, "JSON body must be an object.")
            status, result = self.server.runtime.dispatch(self.path.rstrip("/"), payload)
            self.write_json(status, result)
        except json.JSONDecodeError:
            self.write_json(400, {"error": "Invalid JSON."})
        except RuntimeErrorResponse as exc:
            self.write_json(exc.status, {"error": exc.message, **exc.payload})
        except Exception as exc:  # keep loopback service alive, without leaking a traceback
            self.write_json(500, {"error": "Local runtime error.", "detail": str(exc)})


class InfinityAIServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], runtime: LocalGemmaRuntime):
        self.runtime = runtime
        super().__init__(address, InfinityAIHandler)


def build_server(host: str, port: int, config_path: str | Path = DEFAULT_CONFIG) -> InfinityAIServer:
    if host not in LOOPBACK_HOSTS and os.environ.get("INFINITY_AI_ALLOW_REMOTE") != "1":
        raise ValueError("Refusing a non-loopback bind without INFINITY_AI_ALLOW_REMOTE=1.")
    return InfinityAIServer((host, port), LocalGemmaRuntime(config_path))


def main() -> int:
    parser = argparse.ArgumentParser(description="Infinity local Gemma role gateway")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--host")
    parser.add_argument("--port", type=int)
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    server_config = config.get("server", {})
    host = args.host or os.environ.get("INFINITY_AI_HOST", server_config.get("host", "127.0.0.1"))
    port = args.port or int(os.environ.get("INFINITY_AI_PORT", server_config.get("port", 11435)))
    server = build_server(host, port, args.config)
    print(f"Infinity AI runtime listening on http://{host}:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
