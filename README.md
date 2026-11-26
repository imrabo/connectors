# ImRabo Connectors

Official connector registry for the ImRabo application.

The registry is a versioned static JSON catalog. ImRabo reads `registry.json`, then fetches each connector manifest from this repository's `main` branch.

## Current catalog

This catalog intentionally lists **hosted Streamable HTTP MCP endpoints**. The current ImRabo MCP client supports Streamable HTTP with either no authentication or a bearer token. It does not yet support OAuth browser authorization or local stdio process launch, so OAuth-only and stdio-only servers are not listed as installable connectors.

| Connector | What it provides | Access |
|---|---|---|
| [GitHub](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/set-up-the-github-mcp-server) | Repositories, issues, pull requests, code search, and Actions | Free GitHub account + fine-grained PAT |
| [GitLab](https://docs.gitlab.com/user/model_context_protocol/mcp_server/) | Projects, issues, merge requests, and GitLab operations | GitLab Free tier; OAuth or fine-grained PAT |
| [Cloudflare Docs](https://github.com/cloudflare/mcp-server-cloudflare/tree/main/apps/docs-ai-search) | Search Cloudflare developer documentation | Public; no sign-in |
| [Microsoft Learn](https://learn.microsoft.com/en-us/training/support/mcp) | Search docs, retrieve articles, and code samples | Public; no authentication or charge |
| [OpenAI Developer Docs](https://developers.openai.com/resources/docs-mcp) | Search and read OpenAI developer documentation | Public; no authentication |
| [MDN](https://developer.mozilla.org/en-US/mcp) | Web platform docs and browser compatibility data | Public; experimental |
| [Context7](https://github.com/upstash/context7) | Current, version-specific library and framework documentation | Public basic access; API key increases limits |
| [draw.io](https://www.drawio.com/docs/manual/generate/drawio-mcp-server/) | Create editable diagrams | Public hosted app endpoint |
| [DeepWiki](https://docs.devin.ai/work-with-devin/deepwiki-mcp) | Explore documentation for public GitHub repositories | Public; no authentication |
| [Open Targets](https://platform-docs.opentargets.org/data-access/model-context-protocol) | Biomedical target-disease and drug-target evidence | Public platform data; experimental |
| [Microchip Product Data](https://www.microchip.com/en-us/resources/model-context-protocol-server) | Product specifications, stock, lead times, and compliance | Public; no authentication or charge |
| [Microchip MPLAB Docs](https://www.microchip.com/en-us/resources/model-context-protocol-server) | Technical docs, code examples, videos, and reference designs | Public; no authentication |
| [Renesas Web Data](https://www.renesas.com/en/design-resources/renesas-mcp-server) | Products, datasheets, lifecycle, pricing, inventory, and cross-references | Public; no account, API key, or charge |

**Pricing note:** “Free” here means the MCP endpoint can be connected without buying an MCP product subscription or paid API credits for the listed basic use. A service may apply rate limits, fair-use restrictions, or change its access policy. GitHub requires a GitHub account and a PAT; GitLab requires user authorization. Context7 offers higher limits with an API key. MDN and Open Targets are explicitly experimental. Always review the provider's terms and tool permissions before connecting.

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
