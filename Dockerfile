FROM python:3.13-slim

WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy only the application code
COPY pyproject.toml .
COPY src/ src/

# Install dependencies
RUN uv pip install --system .

# Create config directory for volume mounts
RUN mkdir /config

# Mount your config and data at runtime:
#   -v /path/to/config:/config
# The config.toml and data files should be in /config

USER root

ENTRYPOINT ["python", "-m", "wildcard_mcp"]
