#!/usr/bin/env python3
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from server import build_server


class FakeGemmaHandler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def send_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/v1/models":
            self.send_json(200, {"data": [{"id": "fake-local-gemma"}]})
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length))
        if self.path == "/v1/embeddings":
            self.send_json(200, {
                "model": body.get("model"),
                "data": [{"index": 0, "embedding": [0.1, 0.2, 0.3]}],
            })
            return
        if self.path != "/v1/chat/completions":
            self.send_json(404, {"error": "not found"})
            return
        system = str(body.get("messages", [{}])[0].get("content", ""))
        if "TOOL_ROUTER" in system:
            output = json.dumps({"name": "research.search", "arguments": {"query": "hydrogen"}})
        elif "publication safety gate" in system:
            output = json.dumps({"decision": "APPROVED", "reasons": ["test-safe"]})
        else:
            output = "Local Gemma reasoning response."
        self.send_json(200, {
            "model": body.get("model"),
            "choices": [{"message": {"content": output}}],
        })


class RuntimeIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake = ThreadingHTTPServer(("127.0.0.1", 0), FakeGemmaHandler)
        cls.fake_thread = threading.Thread(target=cls.fake.serve_forever, daemon=True)
        cls.fake_thread.start()

        cls.tempdir = tempfile.TemporaryDirectory()
        cls.config_path = Path(cls.tempdir.name) / "runtime-config.json"
        base = f"http://127.0.0.1:{cls.fake.server_port}/v1"
        cls.config_path.write_text(json.dumps({
            "schema": "infinity/ai-runtime/v1",
            "mode": "LOCAL_FIRST",
            "server": {"host": "127.0.0.1", "port": 0, "maxRequestBytes": 1048576},
            "localInference": {"baseUrl": base, "timeoutSeconds": 2},
            "roles": {
                role: {
                    "provider": "local-gemma",
                    "model": role.lower() + "-test",
                    "requiredForPublication": role in {"IMAGE_SAFETY", "TEXT_SAFETY"},
                    "failClosed": role in {"IMAGE_SAFETY", "TEXT_SAFETY"},
                }
                for role in ["REASONER", "TOOL_ROUTER", "IMAGE_SAFETY", "TEXT_SAFETY", "EMBEDDINGS"]
            },
            "hostedFallback": {"enabled": False},
            "toolExecution": {
                "allowedTools": ["research.search", "wallet.get_balance"],
                "allowlistOnly": True,
                "requireSchemaValidation": True,
                "requirePermissionCheck": True,
                "requireIdempotency": True,
            },
        }), encoding="utf-8")
        cls.runtime = build_server("127.0.0.1", 0, cls.config_path)
        cls.runtime_thread = threading.Thread(target=cls.runtime.serve_forever, daemon=True)
        cls.runtime_thread.start()
        cls.base = f"http://127.0.0.1:{cls.runtime.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.runtime.shutdown()
        cls.runtime.server_close()
        cls.fake.shutdown()
        cls.fake.server_close()
        cls.tempdir.cleanup()

    def request(self, method, path, payload=None):
        data = None if payload is None else json.dumps(payload).encode()
        request = urllib.request.Request(
            self.base + path,
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=3) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def test_health_reports_every_role_ready(self):
        status, body = self.request("GET", "/v1/health")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "READY")
        self.assertTrue(body["publicationAllowed"])
        self.assertEqual(set(body["roles"]), {
            "REASONER", "TOOL_ROUTER", "IMAGE_SAFETY", "TEXT_SAFETY", "EMBEDDINGS"
        })

    def test_reason_returns_typed_inference(self):
        status, body = self.request("POST", "/v1/reason", {"input": "Explain the token."})
        self.assertEqual(status, 200)
        self.assertEqual(body["role"], "REASONER")
        self.assertEqual(body["evidenceState"], "INFERRED")
        self.assertEqual(body["output"], "Local Gemma reasoning response.")

    def test_tool_router_proposes_but_does_not_execute(self):
        status, body = self.request("POST", "/v1/tools", {
            "input": "Research hydrogen",
            "tools": [{"name": "research.search", "description": "Search captured sources"}],
        })
        self.assertEqual(status, 200)
        self.assertEqual(body["proposal"]["name"], "research.search")
        self.assertFalse(body["executed"])
        self.assertTrue(body["requiresApplicationValidation"])

    def test_tool_router_rejects_unrequested_tool(self):
        status, body = self.request("POST", "/v1/tools", {
            "input": "Research hydrogen",
            "tools": [{"name": "wallet.get_balance"}],
        })
        self.assertEqual(status, 422)
        self.assertIn("allowlisted", body["error"])

    def test_text_and_image_moderation(self):
        status, text = self.request("POST", "/v1/moderate/text", {"input": "A public caption"})
        self.assertEqual(status, 200)
        self.assertEqual(text["decision"], "APPROVED")
        status, image = self.request("POST", "/v1/moderate/image", {
            "image": "data:image/png;base64,dGVzdA==",
            "prompt": "Review image",
        })
        self.assertEqual(status, 200)
        self.assertEqual(image["decision"], "APPROVED")

    def test_embeddings_are_typed(self):
        status, body = self.request("POST", "/v1/embed", {"input": "Infinity token"})
        self.assertEqual(status, 200)
        self.assertEqual(body["role"], "EMBEDDINGS")
        self.assertEqual(body["data"][0]["embedding"], [0.1, 0.2, 0.3])


    def private_network_preflight(self, allow_origin):
        request = urllib.request.Request(
            self.base + "/v1/health",
            method="OPTIONS",
            headers={
                "Origin": "https://example.test",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Private-Network": "true",
            },
        )
        with patch.dict(os.environ, {
            "INFINITY_AI_ALLOW_ORIGIN": allow_origin,
            "INFINITY_AI_ALLOW_PRIVATE_NETWORK": "1",
            "INFINITY_AI_QUIET": "1",
        }, clear=False):
            with urllib.request.urlopen(request, timeout=3) as response:
                return response.status, response.headers

    def test_exact_origin_may_receive_private_network_grant(self):
        status, headers = self.private_network_preflight("https://example.test")
        self.assertEqual(status, 204)
        self.assertEqual(headers["Access-Control-Allow-Origin"], "https://example.test")
        self.assertEqual(headers["Access-Control-Allow-Private-Network"], "true")

    def test_wildcard_origin_never_receives_private_network_grant(self):
        status, headers = self.private_network_preflight("*")
        self.assertEqual(status, 204)
        self.assertEqual(headers["Access-Control-Allow-Origin"], "*")
        self.assertIsNone(headers["Access-Control-Allow-Private-Network"])

    def test_moderation_fails_closed_when_provider_is_offline(self):
        stopped_port = self.fake.server_port
        original = self.runtime.runtime.default_base
        self.runtime.runtime.default_base = f"http://127.0.0.1:{stopped_port + 1000}/v1"
        try:
            status, body = self.request("POST", "/v1/moderate/text", {"input": "Review me"})
            self.assertEqual(status, 503)
            self.assertEqual(body["decision"], "REVIEW_REQUIRED")
            self.assertTrue(body["failClosed"])
            self.assertFalse(body["providerReady"])
        finally:
            self.runtime.runtime.default_base = original


if __name__ == "__main__":
    unittest.main(verbosity=2)
