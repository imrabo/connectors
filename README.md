# ImRabo Connectors

Versioned public catalog of connector definitions consumed by the ImRabo application.

## Connector model

ImRabo supports exactly three execution types:

| Type | Execution |
|---|---|
| `mcp` | MCP protocol (currently hosted Streamable HTTP) |
| `api` | Direct declarative HTTP API calls; no MCP server required |
| `builtin` | Native tool implementation already shipped with ImRabo |

Authentication is orthogonal to connector type. The schema recognizes `none`, `bearer`, `apiKey`, `oauth2`, `basic`, and constrained `custom` authentication. See [SCHEMA.md](SCHEMA.md) for exact support and limitations.

## Repository layout

```
registry.json
connectors/<connector-id>/connector.json
SCHEMA.md
```

## Publishing

1. Add a manifest under `connectors/<connector-id>/connector.json`.
2. Add its entry to `registry.json`.
3. Validate it against [SCHEMA.md](SCHEMA.md).
4. Confirm the app implements the selected type, transport and authentication mode.
5. Never include credentials or user-specific data.
6. Open a pull request and describe tool permissions, side effects, provider terms and pricing.

## Security

Manifests are untrusted configuration. The app validates endpoint schemes, methods, paths, schemas and supported authentication. API templates support data substitution only; executable scripts are prohibited. Secrets are collected by the app and stored in secure storage. Never put secrets in URLs or manifests.


## Web search API connectors

Three direct REST API search providers are included in the catalog:

- **Brave Search** — subscription token in `X-Subscription-Token`.
- **Tavily Search** — API key using bearer authentication.
- **Serper** — API key in `X-API-KEY`.

Each provides a `web_search(query)` tool. These are API connectors, not MCP servers. Users need credentials from the relevant provider; availability, free credits, quotas and pricing depend on provider account terms. See [SCHEMA.md](SCHEMA.md) for the manifest and secure credential contract.
