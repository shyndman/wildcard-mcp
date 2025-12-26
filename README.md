# Wildcard MCP

An MCP server that provides true randomness to expose new output pathways in LLM conversations.

LLMs tend to gravitate toward common outputs — ask for a "random name" and you'll get one of the same 10 names every time, even with a random seed. Wildcard injects actual randomness by selecting from user-provided lists, opening up output pathways that would otherwise remain unexplored.

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
docker run -p 80:80 \
           -v $(pwd):/config \
           ghcr.io/shyndman/wildcard-mcp:latest
```

The server listens on `http://localhost/sse` for MCP clients. Mount a directory containing `config.toml` and your data files to `/config`.

**Docker Compose:**

```yaml
services:
  wildcard:
    image: ghcr.io/shyndman/wildcard-mcp:latest
    ports:
      - "80:80"
    volumes:
      - ./:/config:ro
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

The server looks for config at `WILDCARD_CONFIG_PATH` (defaults to `/config/config.toml`), with a fallback to `config.toml` in the project root for local development.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WILDCARD_CONFIG_PATH` | `/config/config.toml` | Config file location |
| `WILDCARD_TRANSPORT` | `sse` | MCP transport: `sse` or `stdio` |
| `WILDCARD_PORT` | `80` | Server port (SSE transport only) |
