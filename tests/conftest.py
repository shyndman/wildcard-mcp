"""Pytest configuration and fixtures for wildcard-mcp tests."""

import os
from pathlib import Path

# Set config path BEFORE importing the server module
_FIXTURES_DIR = Path(__file__).parent / "fixtures"
os.environ["WILDCARD_CONFIG_PATH"] = str(_FIXTURES_DIR / "config.toml")

import pytest
from fastmcp import Client

from wildcard_mcp.server import mcp


@pytest.fixture
async def client():
    """Create a FastMCP client connected to the server."""
    async with Client(transport=mcp) as mcp_client:
        yield mcp_client
