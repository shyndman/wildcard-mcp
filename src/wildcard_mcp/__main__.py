"""CLI entry point for Wildcard MCP server."""

import os

from wildcard_mcp.server import create_server, find_config_path

DEFAULT_TRANSPORT = "sse"


def get_transport() -> str:
  """Get the MCP transport from environment or default to SSE."""
  return os.environ.get("WILDCARD_TRANSPORT", DEFAULT_TRANSPORT)


if __name__ == "__main__":
  mcp = create_server(find_config_path())
  mcp.run(transport=get_transport())
