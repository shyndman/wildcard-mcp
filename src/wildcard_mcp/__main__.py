"""CLI entry point for Wildcard MCP server."""

from wildcard_mcp.server import create_server, find_config_path

if __name__ == "__main__":
  mcp = create_server(find_config_path())
  mcp.run()
