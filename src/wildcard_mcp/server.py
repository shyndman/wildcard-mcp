"""Wildcard MCP Server - Inject true randomness into LLM conversations."""

import os
import random
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from wildcard_mcp.config import CategoryData, load_category_data, load_config

# Config path: env var > /app/config.toml (Docker) > local config.toml
_DEFAULT_PATHS = [
    Path("/app/config.toml"),  # Docker mount point
    Path(__file__).parent.parent.parent / "config.toml",  # Local dev
]


def _find_config_path() -> Path:
    """Find the config file path."""
    if env_path := os.environ.get("WILDCARD_CONFIG_PATH"):
        return Path(env_path)

    for path in _DEFAULT_PATHS:
        if path.exists():
            return path

    raise FileNotFoundError(
        "Config file not found. Set WILDCARD_CONFIG_PATH or mount config.toml"
    )


CONFIG_PATH = _find_config_path()


def _load_data() -> tuple[list[str], dict[str, CategoryData]]:
    """Load configuration and category data.

    Returns:
        Tuple of (category_names, category_data).
    """
    config = load_config(CONFIG_PATH)
    base_path = CONFIG_PATH.parent
    data = load_category_data(config, base_path)
    category_names = list(data.keys())
    return category_names, data


# Load at module level to build the schema
_CATEGORY_NAMES, _CATEGORY_DATA = _load_data()

if not _CATEGORY_NAMES:
    raise ValueError("No categories defined in config")

mcp = FastMCP("wildcard_mcp")


@mcp.tool(
    name="randomize",
    annotations={
        "title": "Random Selection",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,  # Different result each call
        "openWorldHint": False,
    },
)
async def randomize(
    category: Annotated[
        str, Field(description=f"Category to select from. Available: {', '.join(_CATEGORY_NAMES)}")
    ],
    count: Annotated[
        int, Field(default=1, description="Number of items to select (no duplicates)", ge=1)
    ] = 1,
) -> str:
    """Select random items from a category.

    Use this tool to get truly random selections that break typical LLM output
    patterns. Each call returns different results.
    """
    if category not in _CATEGORY_NAMES:
        raise ValueError(f"Unknown category '{category}'. Available: {', '.join(_CATEGORY_NAMES)}")

    category_data = _CATEGORY_DATA[category]
    items = category_data["items"]

    if count > len(items):
        return (
            f"Error: Requested {count} items but category '{category}' "
            f"only has {len(items)} items available."
        )

    selected = random.sample(items, count)

    if count == 1:
        return selected[0]

    return "\n".join(selected)


if __name__ == "__main__":
    mcp.run()
