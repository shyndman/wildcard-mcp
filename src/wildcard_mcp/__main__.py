"""CLI entry point for Wildcard MCP server."""

import os

from wildcard_mcp.server import create_server, find_config_path

DEFAULT_TRANSPORT = "sse"
DEFAULT_PORT = 80


def get_transport() -> str:
  """Get the MCP transport from environment or default to SSE."""
  return os.environ.get("WILDCARD_TRANSPORT", DEFAULT_TRANSPORT)


def get_port() -> int:
  """Get the server port from environment or default to 80."""
  return int(os.environ.get("WILDCARD_PORT", DEFAULT_PORT))


if __name__ == "__main__":
  mcp = create_server(find_config_path())
  mcp.run(transport=get_transport(), port=get_port())
