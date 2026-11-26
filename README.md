# ImRabo Connectors

Official connector registry for the ImRabo application.

The registry is a versioned static JSON catalog. ImRabo reads `registry.json`, then fetches each connector manifest from this repository's `main` branch.

## Current catalog

This catalog intentionally lists **hosted Streamable HTTP MCP endpoints**. The current ImRabo MCP client supports Streamable HTTP with either no authentication or a bearer token. It does not yet support OAuth browser authorization or local stdio process launch, so OAuth-only and stdio-only servers are not listed as installable connectors.

| Connector | What it provides | Access |
|---|---|---|
| [GitHub](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/set-up-the-github-mcp-server) | Repositories, issues, pull requests, code search, and Actions | Free GitHub account + user-provided fine-grained PAT (bearer token) |
| [Cloudflare Documentation](https://developers.cloudflare.com/agents/model-context-protocol/) | Search and read Cloudflare developer documentation | Public; no sign-in |
| [Context7](https://github.com/upstash/context7) | Current, version-specific library and framework documentation | Public basic access; no API key required |
| [draw.io](https://www.drawio.com/docs/manual/generate/drawio-mcp-server/) | Create editable diagrams | Public; no sign-in |
| [DeepWiki](https://mcp.deepwiki.com/mcp) | Ask questions about public GitHub repositories and generated repository documentation | Public; no sign-in; community-hosted |

**Pricing note:** “Free” here means the MCP endpoint can be connected without buying an MCP product subscription or paid API credits for the listed basic use. A service may apply rate limits, fair-use restrictions, or change its access policy. GitHub requires a GitHub account and a PAT; the token's permissions determine what the connector can access. DeepWiki is community-hosted rather than an official GitHub service.

## Repository layout

```
registry.json
connectors/
  <connector-id>/
    connector.json
    icon.svg (optional)
SCHEMA.md
```

## Publishing a connector

1. Add a manifest at `connectors/<connector-id>/connector.json`.
2. Add an entry to `registry.json` with the same ID and manifest path.
3. Validate the manifest against [SCHEMA.md](SCHEMA.md).
4. Confirm that the endpoint is a hosted Streamable HTTP MCP endpoint.
5. Confirm that authentication is supported by the current app (`none` or `bearer`).
6. Open a pull request; do not publish unreviewed endpoints.

Never commit access tokens, API keys, OAuth secrets, passwords, or other credentials. Credentials are collected by ImRabo at install time and stored locally in platform secure storage.

## Compatibility and security

- Only publish HTTPS endpoints controlled by or clearly attributed to the provider.
- Never put secrets in endpoint URL user-info, query strings, or fragments.
- Never hardcode user credentials in a manifest.
- Describe whether the endpoint is official or community-maintained, and state account and pricing requirements accurately.
- Review tool capabilities and permissions before users enable a connector. MCP tools can read or modify external data.
- Do not advertise OAuth or local stdio support until the ImRabo app implements those capabilities.
