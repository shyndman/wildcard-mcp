FROM python:3.13-slim

WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy only the application code
COPY pyproject.toml .
COPY src/ src/

# Install dependencies
RUN uv pip install --system .

# Config and data are mounted at runtime:
#   -v /path/to/config.toml:/app/config.toml
#   -v /path/to/data:/app/data
# Or set WILDCARD_CONFIG_PATH to a custom location

ENTRYPOINT ["python", "-m", "wildcard_mcp.server"]
