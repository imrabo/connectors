# MCP discovery sources

There is no single exhaustive list of every MCP server. Directories overlap, contain duplicates, and include local-only, OAuth-only, paid, abandoned, and community-submitted projects. Directory presence is not a security or compatibility endorsement.

Use these sources to discover candidates; verify each server against its publisher before adding it to the installable registry.

| Source | Coverage | Use |
|---|---|---|
| [Official MCP Registry](https://registry.modelcontextprotocol.io/) | Public server metadata submitted to the MCP ecosystem registry | Primary structured discovery source; inspect publisher, version, repository, and transport metadata |
| [Glama](https://glama.ai/mcp/servers) | Large directory of open-source MCP servers and hosted connectors | Broad discovery and category filtering |
| [Glama API](https://glama.ai/mcp/reference) | Searchable directory API | Programmatic discovery; API key and attribution/link-back requirements apply |
| [PulseMCP](https://www.pulsemcp.com/servers) | Daily-updated server directory with official/community classification | Find and compare candidates; verify status at upstream source |
| [mcp.so](https://mcp.so/servers) | Community directory with categories and collections | Discover remote and local servers |
| [mcpservers.org](https://mcpservers.org/all) | Category-based directory including remote and local listings | Find category-specific candidates |
| [Smithery](https://smithery.ai/servers) | Public directory of MCP servers | Additional community discovery; do not assume its former proxy/hosting features remain available |
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | Curated open-source list | Find upstream repositories, especially local/stdio implementations |
| [TensorBlock/awesome-mcp-servers](https://github.com/TensorBlock/awesome-mcp-servers) | Large categorized collection | Additional candidate discovery |

## Registry inclusion policy

An entry is installable from ImRabo only when it meets the current client contract:

- Hosted HTTPS Streamable HTTP endpoint.
- Authentication supported by the current app: `none` or `bearer`.
- Endpoint and auth requirements confirmed from provider documentation or the maintained upstream repository.
- Free/basic access conditions described accurately, including account, API-key, usage-limit, and plan requirements.
- No credentials or secrets stored in this repository.

Local STDIO servers and OAuth-only remote servers are useful discovery candidates but are not currently installable through the ImRabo hosted connector catalog. Keep those in a future compatibility backlog rather than publishing manifests that the current app cannot connect to.

## Important

This is a discovery index, not a claim that every listed server is free, safe, active, or maintained. Review upstream license, tool permissions, data handling, terms of use, endpoint availability, and maintenance before enabling a connector. Re-check endpoint and pricing information periodically.
