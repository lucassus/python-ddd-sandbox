FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /usr/src/app

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen
