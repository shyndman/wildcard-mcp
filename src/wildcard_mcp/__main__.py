"""CLI entry point for Wildcard MCP server."""

import logging
import os

from wildcard_mcp.server import create_server, find_config_path

DEFAULT_TRANSPORT = "sse"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 80
DEFAULT_LOG_LEVEL = "INFO"


def configure_logging() -> None:
  """Configure logging for wildcard_mcp."""
  level_name = os.environ.get("WILDCARD_LOG_LEVEL", DEFAULT_LOG_LEVEL).upper()
  level = getattr(logging, level_name, logging.INFO)

  logging.basicConfig(
    level=level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
  )

  logger = logging.getLogger("wildcard_mcp")
  logger.setLevel(level)


def get_transport() -> str:
  """Get the MCP transport from environment or default to SSE."""
  return os.environ.get("WILDCARD_TRANSPORT", DEFAULT_TRANSPORT)


def get_host() -> str:
  """Get the server host from environment or default to 0.0.0.0."""
  return os.environ.get("WILDCARD_HOST", DEFAULT_HOST)


def get_port() -> int:
  """Get the server port from environment or default to 80."""
  return int(os.environ.get("WILDCARD_PORT", DEFAULT_PORT))


if __name__ == "__main__":
  configure_logging()
  mcp = create_server(find_config_path())
  mcp.run(transport=get_transport(), host=get_host(), port=get_port())
