# ImRabo Connectors

Versioned public catalog of connector definitions consumed by the ImRabo application.

## Connector model

| Type | Execution |
|---|---|
| `mcp` | MCP protocol (currently hosted Streamable HTTP) |
| `api` | Direct declarative HTTP API calls; no MCP server required |
| `builtin` | Native tool implementation already shipped with ImRabo |

Authentication is orthogonal to connector type. The schema recognizes `none`, `bearer`, `apiKey`, `oauth2`, `basic`, and constrained `custom` authentication. See [SCHEMA.md](SCHEMA.md).

## Layout

```
registry.json
connectors/<connector-id>/connector.json
schemas/connector.schema.json
scripts/validate_registry.py
```

## Validate locally

Run `python scripts/validate_registry.py`. GitHub Actions runs the same check for every pull request and push to main. The validator checks registry uniqueness, manifest paths, ID consistency, execution/auth modes, API HTTP methods and safe paths, declarative templates, and common accidental secret fields.

## Publish

1. Add a manifest under `connectors/<connector-id>/connector.json`.
2. Add its entry to `registry.json`.
3. Run the validator.
4. Confirm ImRabo implements the selected type, transport and authentication mode.
5. Never include credentials or user-specific data.
6. Open a pull request and describe tool permissions, side effects, provider terms and pricing.

## Security

Manifests are untrusted configuration. The app validates endpoint schemes, methods, paths, schemas and supported authentication. API templates support data substitution only; executable scripts are prohibited. Secrets are collected by the app and stored in secure storage. Never put secrets in URLs or manifests. CI validation is a publishing safeguard, not a replacement for runtime validation.

## Web search API connectors

- **Brave Search** — subscription token in `X-Subscription-Token`.
- **Tavily Search** — API key using bearer authentication.
- **Serper** — API key in `X-API-KEY`.

Each exposes `web_search(query)`. These are API connectors, not MCP servers. Provider accounts, free credits, quotas and pricing depend on provider terms.
