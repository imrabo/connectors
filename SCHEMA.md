# Connector registry schema

## registry.json

The root registry is a JSON object with:
- `schemaVersion`: integer; currently `1`.
- `name`: registry display name.
- `description`: short registry description.
- `connectors`: array of catalog entries.

Each entry contains `id`, `name`, and `manifest`; `description`, `category`, and `version` are optional.

Example:

```json
{
  "id": "example-service",
  "name": "Example Service",
  "description": "Connect ImRabo to Example Service.",
  "category": "Productivity",
  "version": "1.0.0",
  "manifest": "connectors/example-service/connector.json"
}
```

## Connector manifest

Required fields: `id`, `name`, and absolute HTTP(S) `endpoint`.
Optional fields: `description`, `version`, `transport` (defaults to `streamableHttp`), and `authentication.type` (`none` or `bearer`).

```json
{
  "id": "example-service",
  "name": "Example Service",
  "description": "Example MCP integration.",
  "version": "1.0.0",
  "transport": "streamableHttp",
  "endpoint": "https://mcp.example.com/mcp",
  "authentication": { "type": "bearer" }
}
```

## Security and review

- Publish HTTPS endpoints controlled by the connector publisher.
- Never commit credentials, tokens, OAuth secrets, or private user data.
- Never put secrets in endpoint URL user-info, query strings, or fragments.
- Keep manifest paths relative and inside this repository.
- Describe the scopes and data exposed by connector tools in the pull request.
- Do not advertise transports or authentication modes unsupported by the current app.
- Breaking manifest changes require a schema-version change and app compatibility review.

The first app integration supports Streamable HTTP and no-auth or bearer-token authentication only.
