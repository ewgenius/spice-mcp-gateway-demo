# Spice MCP Gateway Demo

Demo showing Spice.ai as an MCP gateway that aggregates tools from multiple sources and exposes them to an AI agent.

## Architecture

```
┌─────────────┐       ┌─────────────────┐       ┌──────────────────┐
│   Hermes    │─MCP──▶│   Spice.ai      │─MCP──▶│  FastMCP Server  │
│   (Agent)   │       │   (Gateway)     │       │  (Custom Tools)  │
└─────────────┘       └─────────────────┘       └──────────────────┘
                              │
                              ├── Built-in tools (SQL, search, etc.)
                              └── Dataset: taxi_trips (S3 parquet)
```

**Flow:**

1. **FastMCP Server** — Python server exposing custom tools via Streamable HTTP
2. **Spice.ai** — MCP gateway that imports tools from FastMCP and adds its own built-in tools (SQL queries over datasets, etc.)
3. **Hermes** — AI agent (using OpenRouter/GPT-4.1-mini) that connects to Spice's MCP endpoint and can use all aggregated tools

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

## Services

| Service          | Port  | Description            |
| ---------------- | ----- | ---------------------- |
| Spice HTTP       | 8090  | MCP gateway + SQL API  |
| Spice Flight     | 50051 | Arrow Flight interface |
| FastMCP Server   | 8000  | Custom tool server     |
| Hermes Gateway   | 8642  | Agent API              |
| Hermes Dashboard | 9119  | Monitoring UI          |

## How It Works

- `spicepod.yaml` configures Spice to import tools from `fast-mcp-server` and serve a taxi trips dataset from S3
- `hermes-config.yaml` points Hermes at Spice's `/v1/mcp` endpoint with API key auth
- When the agent needs a tool, it calls Spice, which either handles it directly (SQL queries) or proxies the call to FastMCP
