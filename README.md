# Wildcard MCP

An MCP server that provides true randomness to break LLM output patterns.

LLMs tend to gravitate toward common outputs — ask for a "random name" and you'll get one of the same 10 names every time. Wildcard injects actual randomness by selecting from user-provided lists.

## Setup

### 1. Create your config file

Copy the sample config:

```bash
cp config.sample.toml config.toml
```

Edit `config.toml` to define your categories:

```toml
[categories]
male_names = "data/male_names.txt"
female_names = "data/female_names.txt"
colors = "data/colors.txt"
adjectives = "data/adjectives.txt"
```

### 2. Create your data files

Each category points to a text file with one item per line:

```bash
mkdir -p data
```

**data/male_names.txt:**
```
Liam
Noah
Oliver
Theodore
James
...
```

**data/female_names.txt:**
```
Olivia
Emma
Amelia
Charlotte
Mia
...
```

You can find comprehensive name lists at [ssa.gov/oact/babynames](https://www.ssa.gov/oact/babynames/limits.html).

### 3. Run the server

**Local development:**

```bash
uv run python -m wildcard_mcp.server
```

**Docker:**

```bash
docker run -v $(pwd)/config.toml:/app/config.toml \
           -v $(pwd)/data:/app/data \
           ghcr.io/shyndman/wildcard-mcp:latest
```

## Tool

### `randomize`

Select random items from a configured category.

**Parameters:**
- `category` (required): Category name from your config
- `count` (optional, default 1): Number of items to select (no duplicates)

**Example:**
```
randomize(category="male_names", count=3)
→ "Theodore\nMiles\nCaleb"
```

## Configuration

The server looks for config in this order:
1. `WILDCARD_CONFIG_PATH` environment variable
2. `/app/config.toml` (Docker mount point)
3. `config.toml` in the project root (local dev)
