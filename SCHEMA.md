# ImRabo connector registry schema

The connector platform has exactly three execution types: `mcp`, `api`, and `builtin`. Authentication is independent of execution type.

## Registry

The root `registry.json` contains `schemaVersion` (integer), `name`, `description`, and `connectors`. Each catalog entry contains `id`, `name`, and a repository-relative `manifest` path; `description`, `category`, and `version` are optional.

## Common connector manifest

Required: `id`, `name`, `type`. Optional: `description`, `version`, `enabled`, `configuration`, and `tools`.

```json
{
  "schemaVersion": 1,
  "id": "example",
  "name": "Example",
  "description": "Example connector",
  "version": "1.0.0",
  "type": "mcp",
  "connection": {
    "transport": "streamableHttp",
    "endpoint": "https://mcp.example.com/mcp"
  },
  "auth": { "type": "bearer", "secretRef": "example-token" },
  "configuration": {},
  "tools": []
}
```

Legacy MCP manifests using root-level `endpoint`, `transport`, and `authentication` remain valid for compatibility.

## Connector types

### `mcp`

Uses the MCP protocol. `connection.endpoint` must be an absolute HTTP(S) URL. Currently supported transport: `streamableHttp`.

### `api`

Executes declarative HTTP tools directly; no MCP server is required. `connection.baseUrl` must be an absolute HTTP(S) URL. Each tool declares `name`, `description`, `method` (GET, POST, PUT, PATCH, DELETE), `path`, `inputSchema`, and optional `headers`, `queryParams`, and `body`.

Templates may use only `{{input.property.path}}` substitutions. Manifests must not contain executable scripts.

### `builtin`

References a tool implementation already registered by the ImRabo application. Each tool entry declares the registered tool name and optional description/schema metadata. A manifest cannot ship executable code.

## Authentication types

Authentication is independent from connector type. Supported schema values:

- `none`: no credentials.
- `bearer`: secret sent as an Authorization Bearer token.
- `apiKey`: secret sent in a named HTTP header (query/cookie placement is intentionally disallowed by the secure default).
- `oauth2`: OAuth 2.0 account authorization; requires app-side authorization-code + PKCE, state validation, refresh and per-user token storage.
- `basic`: base64-encoded username:password credential stored as a secret.
- `custom`: explicitly declared static headers and secret references; no scripts.

The app's current API executor supports `none`, `bearer`, header `apiKey`, `basic`, and constrained `custom`. OAuth2 is defined for forward compatibility but must not be advertised as operational until the OAuth account manager is implemented. MCP catalog installation currently supports `none` and bearer credentials.

## Security and review

- Publish HTTPS endpoints controlled by the provider.
- Never commit credentials, API keys, OAuth client secrets, passwords, or user tokens.
- Use secret references; collect and store actual values in platform secure storage.
- Never put secrets in URLs, query strings, fragments, or repository manifests.
- Keep manifest paths relative and inside this repository.
- Validate URLs, HTTP methods, tool schemas, and templates before execution.
- Do not evaluate scripts or arbitrary expressions from manifests.
- Describe scopes, data access, side effects, account requirements and pricing accurately.
- Breaking changes require a schema-version change and app compatibility review.
