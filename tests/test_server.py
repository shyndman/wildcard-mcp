"""Tests for the Wildcard MCP server."""

import pytest
from fastmcp import Client


async def test_list_tools(client: Client):
  """Verify the randomize tool is registered."""
  tools = await client.list_tools()
  tool_names = [t.name for t in tools]
  assert "randomize" in tool_names


async def test_randomize_single_item(client: Client, mcp):
  """Randomize with count=1 returns a single item from the category."""
  result = await client.call_tool("randomize", {"category": "colors"})
  assert result.data in mcp._wildcard_category_data["colors"]["items"]


async def test_randomize_multiple_items(client: Client, mcp):
  """Randomize with count>1 returns multiple newline-separated items."""
  result = await client.call_tool("randomize", {"category": "colors", "count": 5})
  items = result.data.split("\n")
  assert len(items) == 5
  for item in items:
    assert item in mcp._wildcard_category_data["colors"]["items"]


async def test_randomize_no_duplicates(client: Client):
  """Randomize should not return duplicate items."""
  result = await client.call_tool("randomize", {"category": "colors", "count": 8})
  items = result.data.split("\n")
  assert len(items) == len(set(items)), "Duplicates found in results"


async def test_randomize_invalid_category(client: Client):
  """Randomize with invalid category raises validation error."""
  with pytest.raises(Exception) as exc_info:
    await client.call_tool("randomize", {"category": "nonexistent"})
  assert "nonexistent" in str(exc_info.value).lower()


async def test_randomize_count_exceeds_items(client: Client):
  """Randomize with count > available items returns error message."""
  # animals.txt has only 5 items
  result = await client.call_tool("randomize", {"category": "animals", "count": 100})
  assert "Error" in result.data
  assert "100" in result.data


def test_categories_loaded(mcp):
  """Verify categories are loaded from test config."""
  assert "colors" in mcp._wildcard_category_names
  assert "animals" in mcp._wildcard_category_names


def test_category_data_not_empty(mcp):
  """Verify category data files have content."""
  for name in mcp._wildcard_category_names:
    items = mcp._wildcard_category_data[name]["items"]
    assert len(items) > 0, f"Category '{name}' has no items"
