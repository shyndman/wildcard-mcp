"""Pytest configuration and fixtures for wildcard-mcp tests."""

from pathlib import Path

import pytest
from fastmcp import Client

from wildcard_mcp.server import create_server

FIXTURES_DIR = Path(__file__).parent / "fixtures"
TEST_CONFIG_PATH = FIXTURES_DIR / "config.toml"


@pytest.fixture
def mcp():
  """Create a test server with test fixtures config."""
  return create_server(TEST_CONFIG_PATH)


@pytest.fixture
async def client(mcp):
  """Create a FastMCP client connected to the test server."""
  async with Client(transport=mcp) as mcp_client:
    yield mcp_client
