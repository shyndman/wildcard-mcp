"""Wildcard MCP Server - Inject true randomness into LLM conversations."""

import logging
import os
import random
from pathlib import Path
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from wildcard_mcp.config import load_category_data, load_config

logger = logging.getLogger("wildcard_mcp")

DEFAULT_CONFIG_PATH = "/config/config.toml"
_LOCAL_DEV_PATH = Path(__file__).parent.parent.parent / "config.toml"


def find_config_path() -> Path:
  """Find the config file path using default discovery."""
  config_path = Path(os.environ.get("WILDCARD_CONFIG_PATH", DEFAULT_CONFIG_PATH))

  if config_path.exists():
    return config_path

  # Fallback for local development
  if _LOCAL_DEV_PATH.exists():
    return _LOCAL_DEV_PATH

  raise FileNotFoundError(
    f"Config file not found at {config_path}. Set WILDCARD_CONFIG_PATH or mount to /config."
  )


def create_server(config_path: Path) -> FastMCP:
  """Create a configured Wildcard MCP server.

  Args:
      config_path: Path to the TOML config file.

  Returns:
      Configured FastMCP server instance.
  """
  logger.info("Creating Wildcard MCP server")

  config = load_config(config_path)
  category_data = load_category_data(config, config_path.parent)
  category_names = list(category_data.keys())

  if not category_names:
    raise ValueError("No categories defined in config")

  logger.info("Server ready with %d categories", len(category_names))

  mcp = FastMCP("wildcard_mcp")

  @mcp.tool(
    name="randomize",
    annotations={
      "title": "Random Selection",
      "readOnlyHint": True,
      "destructiveHint": False,
      "idempotentHint": False,
      "openWorldHint": False,
    },
  )
  async def randomize(
    category: Annotated[
      str, Field(description=f"Category to select from. Available: {', '.join(category_names)}")
    ],
    count: Annotated[
      int, Field(default=1, description="Number of items to select (no duplicates)", ge=1)
    ] = 1,
  ) -> str:
    """Select random items from a category.

    Use this tool to get truly random selections that break typical LLM output
    patterns. Each call returns different results.
    """
    if category not in category_names:
      raise ValueError(f"Unknown category '{category}'. Available: {', '.join(category_names)}")

    items = category_data[category].items

    if count > len(items):
      return (
        f"Error: Requested {count} items but category '{category}' "
        f"only has {len(items)} items available."
      )

    selected = random.sample(items, count)

    if count == 1:
      return selected[0]

    return "\n".join(selected)

  # Attach metadata for testing
  mcp._wildcard_category_names = category_names
  mcp._wildcard_category_data = category_data

  return mcp
