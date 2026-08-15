#!/usr/bin/env python3
"""Small standard-library client for the local Infinity AI role gateway."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


class InfinityAIError(RuntimeError):
    """The local runtime was unavailable or returned an invalid contract."""


class InfinityAIClient:
    def __init__(self, base_url: str | None = None, timeout: float = 60):
        self.base_url = (base_url or os.environ.get(
            "INFINITY_AI_BASE_URL", "http://127.0.0.1:11435"
        )).rstrip("/")
        self.timeout = timeout

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        request = urllib.request.Request(
            self.base_url + path,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
            raise InfinityAIError(f"Infinity AI request failed: {exc}") from exc
        if not isinstance(result, dict):
            raise InfinityAIError("Infinity AI response must be a JSON object")
        return result

    def reason(self, prompt: str, context: dict[str, Any]) -> dict[str, Any]:
        result = self._post("/v1/reason", {"input": prompt, "context": context})
        if (
            result.get("schema") != "infinity/reason-result/v1"
            or result.get("role") != "REASONER"
            or result.get("evidenceState") != "INFERRED"
            or not isinstance(result.get("output"), str)
        ):
            raise InfinityAIError("REASONER returned an invalid or elevated evidence contract")
        return result

    def propose_research_tool(self, prompt: str, token_id: str) -> dict[str, Any]:
        result = self._post("/v1/tools", {
            "input": prompt,
            "context": {"token_id": token_id},
            "tools": [
                {
                    "name": "research.expand_token",
                    "description": "Propose deeper research for one ledgered commit token",
                },
                {
                    "name": "research.search",
                    "description": "Propose a search for external sources; the application executes it separately",
                },
            ],
        })
        if result.get("executed") is not False or not isinstance(result.get("proposal"), dict):
            raise InfinityAIError("TOOL_ROUTER must return a proposal with executed=false")
        return result
