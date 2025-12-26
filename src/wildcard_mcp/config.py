"""Configuration loading for Wildcard MCP."""

import logging
import tomllib
from pathlib import Path

from pydantic import BaseModel, ConfigDict

logger = logging.getLogger("wildcard_mcp")


class CategoryConfig(BaseModel):
  """Configuration for a single category."""

  model_config = ConfigDict(extra="forbid")

  name: str
  path: str


class WildcardConfig(BaseModel):
  """Root configuration structure."""

  model_config = ConfigDict(extra="forbid")

  category: list[CategoryConfig]


class CategoryData:
  """Loaded category data."""

  def __init__(self, items: list[str], file_path: str):
    self.items = items
    self.file_path = file_path


def load_config(config_path: Path) -> WildcardConfig:
  """Load and validate the TOML configuration file.

  Args:
      config_path: Path to the config.toml file.

  Returns:
      Parsed and validated configuration.

  Raises:
      FileNotFoundError: If config file doesn't exist.
      tomllib.TOMLDecodeError: If config file is invalid TOML.
      pydantic.ValidationError: If config structure is invalid or has unknown keys.
  """
  if not config_path.exists():
    raise FileNotFoundError(f"Config file not found: {config_path}")

  logger.info("Loading config from %s", config_path)

  with open(config_path, "rb") as f:
    raw_config = tomllib.load(f)

  config = WildcardConfig.model_validate(raw_config)

  logger.info(
    "Loaded %d categories: %s", len(config.category), ", ".join(c.name for c in config.category)
  )

  return config


def load_category_data(config: WildcardConfig, base_path: Path) -> dict[str, CategoryData]:
  """Load all category data files.

  Args:
      config: Parsed configuration.
      base_path: Base path for resolving relative file paths.

  Returns:
      Dict mapping category names to their loaded items.

  Raises:
      FileNotFoundError: If a category file doesn't exist.
      ValueError: If a category file is empty.
  """
  data: dict[str, CategoryData] = {}

  for category in config.category:
    file_path = base_path / category.path

    if not file_path.exists():
      raise FileNotFoundError(f"Category file not found for '{category.name}': {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
      items = [line.strip() for line in f if line.strip()]

    if not items:
      raise ValueError(f"Category file for '{category.name}' is empty: {file_path}")

    logger.debug("Loaded category '%s': %d items from %s", category.name, len(items), file_path)

    data[category.name] = CategoryData(items=items, file_path=str(file_path))

  return data
