# [2026-05-26] spice-mcp-netbox

Spice.ai MCP gateway demo with Hermes agent and a custom FastMCP tool server.

## Architecture

- **spice** — Spice.ai runtime (`spiceai.org/spiceai:local`) serving as an MCP gateway on port 8090. Exposes built-in tools (SQL, search, memory, etc.) and proxies tools from the fast-mcp-server.
- **fast-mcp-server** — Python FastMCP server providing custom tools via Streamable HTTP on port 8000.
- **hermes** — Hermes AI agent connecting to Spice's MCP endpoint to use all available tools.
- **dashboard** — Hermes dashboard UI on port 9119.

## Setup

1. Copy `.env.example` to `.env` and set:
   ```
   OPENROUTER_API_KEY=<your-key>
   SPICE_API_KEY=<any-secret-for-spice-auth>
   ```

2. Start all services:
   ```
   docker compose up -d
   ```

3. Run chat:
   ```
   docker compose run --rm -it hermes chat
   ```

## Custom MCP Tools

The `fast-mcp-server` exposes the following tools (prefixed with `fast_mcp/`):

| Tool | Description |
|------|-------------|
| `fastmcp_custom_hello` | Say hello to someone |
| `fastmcp_custom_get_time` | Return current UTC time |
| `fastmcp_custom_random_number` | Generate a random integer in a range |
| `fastmcp_custom_echo` | Echo back a message |
| `fastmcp_custom_word_count` | Count words, characters, and lines |

## API Key Auth

Spice is configured with API key authentication. Pass `x-api-key` header:

```
curl -H "x-api-key: $SPICE_API_KEY" http://localhost:8090/v1/tools
```

## Ports

| Service | Port |
|---------|------|
| Spice HTTP | 8090 |
| Spice Flight | 50051 |
| Fast MCP Server | 8000 |
| Hermes Gateway | 8642 |
| Hermes Dashboard | 9119 |
