#!/usr/bin/env python3
"""Validate the ImRabo connector registry and every referenced manifest."""
import ipaddress
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
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


def fail(message):
    raise ValueError(message)


def safe_http_url(value, label):
    if not isinstance(value, str):
        fail(f"{label} must be a URL string")
    parsed = urlparse(value)
    if parsed.scheme not in {"https", "http"} or not parsed.hostname:
        fail(f"{label} must be an absolute HTTP(S) URL")
    if parsed.username or parsed.password or parsed.fragment:
        fail(f"{label} cannot include credentials or a fragment")
    hostname = parsed.hostname.lower()
    if hostname in {"localhost"} or hostname.endswith((".localhost", ".local", ".internal")):
        fail(f"{label} cannot target a local hostname")
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        fail(f"{label} cannot target a non-public IP address")


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

    # Legacy MCP manifests predate the explicit type field. Root endpoint +
    # transport, or connection.endpoint, are interpreted as type=mcp.
    manifest_type = manifest.get("type")
    if manifest_type is None:
        connection = manifest.get("connection", {})
        if isinstance(connection, dict) and connection.get("endpoint"):
            manifest_type = "mcp"
        elif manifest.get("endpoint"):
            manifest_type = "mcp"
        else:
            fail(f"{entry.get('id')}: manifest must declare type or a legacy MCP endpoint")
    if entry.get("type") not in ALLOWED_TYPES:
        fail(f"{entry.get('id')}: registry type must be one of {sorted(ALLOWED_TYPES)}")
    if manifest_type not in ALLOWED_TYPES:
        fail(f"{entry.get('id')}: unsupported manifest type {manifest_type!r}")
    if manifest_type != entry.get("type"):
        fail(f"{entry.get('id')}: registry type does not match manifest type")

    auth = manifest.get("auth", manifest.get("authentication", {"type": "none"}))
    if not isinstance(auth, dict) or auth.get("type", "none") not in ALLOWED_AUTH:
        fail(f"{entry.get('id')}: unsupported authentication configuration")

    if manifest_type == "mcp":
        connection = manifest.get("connection", {})
        if not isinstance(connection, dict):
            fail(f"{entry['id']}: connection must be an object")
        endpoint = connection.get("endpoint", manifest.get("endpoint"))
        safe_http_url(endpoint, f"{entry['id']} endpoint")
        transport = connection.get("transport", manifest.get("transport", "streamableHttp"))
        if transport != "streamableHttp":
            fail(f"{entry['id']}: only streamableHttp is supported")

    if manifest_type == "api":
        connection = manifest.get("connection", {})
        if not isinstance(connection, dict):
            fail(f"{entry['id']}: API connection must be an object")
        safe_http_url(connection.get("baseUrl"), f"{entry['id']} baseUrl")
        tools = manifest.get("tools")
        if not isinstance(tools, list) or not tools:
            fail(f"{entry['id']}: API connector requires at least one tool")
        for tool in tools:
            if not isinstance(tool, dict) or not all(
                isinstance(tool.get(key), str) for key in ("name", "method", "path")
            ):
                fail(f"{entry['id']}: every API tool requires name, method and path")
            if tool["method"].upper() not in ALLOWED_METHODS:
                fail(f"{entry['id']}: unsupported HTTP method {tool['method']}")
            tool_path = tool["path"]
            if (
                not tool_path.startswith("/")
                or tool_path.startswith("//")
                or "://" in tool_path
                or "\\" in tool_path
                or "?" in tool_path
                or "#" in tool_path
                or any(part in {".", ".."} for part in tool_path.split("/"))
            ):
                fail(f"{entry['id']}: tool path must be a safe absolute path on the declared host")
            if not isinstance(tool.get("inputSchema"), dict):
                fail(f"{entry['id']}: tool inputSchema must be an object")
            validate_template(tool.get("headers", {}), f"{entry['id']}.{tool['name']}.headers")
            validate_template(tool.get("queryParams", {}), f"{entry['id']}.{tool['name']}.queryParams")
            validate_template(tool.get("body"), f"{entry['id']}.{tool['name']}.body")

    if manifest_type == "builtin" and not manifest.get("tools"):
        fail(f"{entry['id']}: builtin connector must reference at least one tool")

    encoded = json.dumps(manifest).lower()
    for marker in (
        '"api_key":',
        '"apikeyvalue":',
        '"access_token":',
        '"client_secret":',
        '"password":',
    ):
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
        version = entry.get("version")
        if version is not None and not SEMVER.fullmatch(str(version)):
            fail(f"{connector_id}: invalid registry semantic version")
        validate_manifest(entry)

    version_feed = ROOT / "app-version.json"
    if version_feed.exists():
        feed = json.loads(version_feed.read_text(encoding="utf-8"))
        if feed.get("schemaVersion") != 1 or feed.get("appId") != "imrabo":
            fail("app-version.json has an unsupported schema or appId")
        for key in ("latestVersion", "minimumSupportedVersion"):
            if not SEMVER.fullmatch(str(feed.get(key, ""))):
                fail(f"app-version.json: {key} must be semantic version")
        for key in ("downloadUrl", "releaseNotesUrl"):
            value = feed.get(key)
            if value:
                safe_http_url(value, f"app-version.json {key}")

    print(f"Validated {len(seen)} connector manifests.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
