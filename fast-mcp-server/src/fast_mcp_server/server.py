"""Minimal FastMCP server."""

import argparse
import logging
import random
import sys
from datetime import datetime, timezone

from fastmcp import FastMCP

mcp = FastMCP("fast-mcp-server")


@mcp.tool()
def fastmcp_custom_hello(name: str = "world") -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"


@mcp.tool()
def fastmcp_custom_get_time() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


@mcp.tool()
def fastmcp_custom_random_number(min_val: int = 1, max_val: int = 100) -> int:
    """Generate a random integer between min_val and max_val (inclusive)."""
    return random.randint(min_val, max_val)


@mcp.tool()
def fastmcp_custom_echo(message: str) -> str:
    """Echo back the provided message. Useful for testing connectivity."""
    return message


@mcp.tool()
def fastmcp_custom_word_count(text: str) -> dict:
    """Count words, characters, and lines in the provided text."""
    return {
        "words": len(text.split()),
        "characters": len(text),
        "lines": text.count("\n") + 1,
    }


def main() -> None:
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Fast MCP Server")
    parser.add_argument("--transport", choices=["stdio", "http", "sse"], default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    logger = logging.getLogger(__name__)

    logger.info(f"Starting Fast MCP Server (transport={args.transport})")

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        logger.info(f"{args.transport.upper()} transport on {args.host}:{args.port}")
        mcp.run(transport=args.transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
