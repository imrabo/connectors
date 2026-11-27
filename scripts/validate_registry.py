#!/usr/bin/env python3
"""Validate the ImRabo connector registry and every referenced manifest."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.json"
ALLOWED_TYPES = {"mcp", "api", "builtin"}
ALLOWED_AUTH = {"none", "bearer", "apiKey", "oauth2", "basic", "custom"}
ALLOWED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}
PLACEHOLDER = re.compile(r"\{\{input\.[a-zA-Z0-9_.-]+\}\}")

def fail(message):
    raise ValueError(message)

def safe_http_url(value, label):
    if not isinstance(value, str):
        fail(f"{label} must be a URL string")
    parsed = urlparse(value)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc or parsed.username or parsed.password or parsed.fragment:
        fail(f"{label} must be an absolute HTTP(S) URL without credentials or fragment")

def validate_template(value, where):
    if isinstance(value, str):
        stripped = PLACEHOLDER.sub("", value)
        if "{{" in stripped or "}}" in stripped:
            fail(f"{where} contains an unsupported template expression")
    elif isinstance(value, dict):
        for key, child in value.items():
            validate_template(child, f"{where}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            validate_template(child, f"{where}[{index}]")

def validate_manifest(entry):
    manifest_path = entry.get("manifest")
    if not isinstance(manifest_path, str) or not manifest_path:
        fail(f"{entry.get('id')}: missing manifest path")
    rel = Path(manifest_path)
    if rel.is_absolute() or ".." in rel.parts:
        fail(f"{entry.get('id')}: manifest path must stay inside repository")
    path = (ROOT / rel).resolve()
    if ROOT.resolve() not in path.parents or not path.is_file():
        fail(f"{entry.get('id')}: manifest does not exist inside repository: {manifest_path}")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("schemaVersion", 1) != 1:
        fail(f"{entry.get('id')}: unsupported schemaVersion")
    if manifest.get("id") != entry.get("id"):
        fail(f"{entry.get('id')}: registry ID does not match manifest ID")
    if manifest.get("type") not in ALLOWED_TYPES:
        fail(f"{entry.get('id')}: type must be one of {sorted(ALLOWED_TYPES)}")
    auth = manifest.get("auth", manifest.get("authentication", {"type": "none"}))
    if not isinstance(auth, dict) or auth.get("type", "none") not in ALLOWED_AUTH:
        fail(f"{entry.get('id')}: unsupported authentication configuration")
    if manifest.get("type") == "mcp":
        connection = manifest.get("connection", {})
        endpoint = connection.get("endpoint", manifest.get("endpoint"))
        safe_http_url(endpoint, f"{entry['id']} endpoint")
        transport = connection.get("transport", manifest.get("transport", "streamableHttp"))
        if transport != "streamableHttp":
            fail(f"{entry['id']}: only streamableHttp is supported")
    if manifest.get("type") == "api":
        connection = manifest.get("connection", {})
        safe_http_url(connection.get("baseUrl"), f"{entry['id']} baseUrl")
        tools = manifest.get("tools")
        if not isinstance(tools, list) or not tools:
            fail(f"{entry['id']}: API connector requires at least one tool")
        for tool in tools:
            if not isinstance(tool, dict) or not all(isinstance(tool.get(key), str) for key in ("name", "method", "path")):
                fail(f"{entry['id']}: every API tool requires name, method and path")
            if tool["method"].upper() not in ALLOWED_METHODS:
                fail(f"{entry['id']}: unsupported HTTP method {tool['method']}")
            if not tool["path"].startswith("/") or "://" in tool["path"] or ".." in tool["path"]:
                fail(f"{entry['id']}: tool path must be a safe absolute path on the declared host")
            if "inputSchema" not in tool or not isinstance(tool["inputSchema"], dict):
                fail(f"{entry['id']}: tool inputSchema must be an object")
            validate_template(tool.get("headers", {}), f"{entry['id']}.{tool['name']}.headers")
            validate_template(tool.get("queryParams", {}), f"{entry['id']}.{tool['name']}.queryParams")
            validate_template(tool.get("body"), f"{entry['id']}.{tool['name']}.body")
    if manifest.get("type") == "builtin" and not manifest.get("tools"):
        fail(f"{entry['id']}: builtin connector must reference at least one tool")
    encoded = json.dumps(manifest).lower()
    for marker in ('"api_key":', '"apikeyvalue":', '"access_token":', '"client_secret":', '"password":'):
        if marker in encoded:
            fail(f"{entry['id']}: possible credential value in manifest; use secretRef")

def main():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if registry.get("schemaVersion") != 1 or not isinstance(registry.get("connectors"), list):
        fail("registry.json must have schemaVersion 1 and a connectors array")
    seen = set()
    for entry in registry["connectors"]:
        connector_id = entry.get("id")
        if not isinstance(connector_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,62}", connector_id):
            fail(f"invalid connector ID: {connector_id!r}")
        if connector_id in seen:
            fail(f"duplicate connector ID: {connector_id}")
        seen.add(connector_id)
        validate_manifest(entry)
    print(f"Validated {len(seen)} connector manifests.")

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
