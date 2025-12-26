"""Configuration loading for Wildcard MCP."""

import tomllib
from pathlib import Path
from typing import TypedDict


class WildcardConfig(TypedDict):
    """Configuration structure for wildcard categories."""

    categories: dict[str, str]  # category_name -> file_path


class CategoryData(TypedDict):
    """Loaded category data."""

    items: list[str]
    file_path: str


def load_config(config_path: Path) -> WildcardConfig:
    """Load and validate the TOML configuration file.

    Args:
        config_path: Path to the config.toml file.

    Returns:
        Parsed configuration.

    Raises:
        FileNotFoundError: If config file doesn't exist.
        tomllib.TOMLDecodeError: If config file is invalid TOML.
        ValueError: If config structure is invalid.
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    if "categories" not in config:
        raise ValueError("Config must have a [categories] section")

    if not isinstance(config["categories"], dict):
        raise ValueError("[categories] must be a table of category_name = file_path")

    for name, file_path in config["categories"].items():
        if not isinstance(file_path, str):
            raise ValueError(f"Category '{name}' must map to a file path string")

    return WildcardConfig(categories=config["categories"])


def load_category_data(
    config: WildcardConfig, base_path: Path
) -> dict[str, CategoryData]:
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

    for category_name, file_path_str in config["categories"].items():
        file_path = base_path / file_path_str

        if not file_path.exists():
            raise FileNotFoundError(
                f"Category file not found for '{category_name}': {file_path}"
            )

        with open(file_path, "r", encoding="utf-8") as f:
            items = [line.strip() for line in f if line.strip()]

        if not items:
            raise ValueError(f"Category file for '{category_name}' is empty: {file_path}")

        data[category_name] = CategoryData(items=items, file_path=str(file_path))

    return data
