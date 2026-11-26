# ImRabo Connectors

Official connector registry for the ImRabo application.

The registry is a versioned static JSON catalog. ImRabo reads `registry.json`, then fetches each connector manifest from this repository's `main` branch.

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
4. Open a pull request; do not publish unreviewed endpoints.

Never commit access tokens, API keys, OAuth secrets, passwords, or other credentials. Credentials are collected by ImRabo at install time and stored locally in platform secure storage.

The current app supports Streamable HTTP MCP endpoints with no authentication or bearer-token authentication.
