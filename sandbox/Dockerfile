# shipharness sandbox images. Build from the repository root:
#   docker build -f sandbox/Dockerfile --target agent   -t shipharness-agent:1 .
#   docker build -f sandbox/Dockerfile --target referee -t shipharness-referee:1 .
# Dependencies are baked in at build time; containers run with --network none.
# .dockerignore keeps .env and other local state out of the build context: no key enters an image.

FROM python:3.12-slim AS base
COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /usr/local/bin/uv
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    PATH=/opt/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /opt/build
COPY pyproject.toml uv.lock ./
# [walkthrough:S3:dockerfile] start
RUN uv sync --frozen --no-install-project --group dev
# Non-root user; the workspace is bind-mounted at /work and is the only writable path besides /tmp.
RUN useradd --uid 1000 --create-home agent \
    && git config --system user.name "agent" \
    && git config --system user.email "agent@sandbox.invalid" \
    && git config --system --add safe.directory /work

FROM base AS agent
USER 1000:1000
WORKDIR /work
# [walkthrough:S3:dockerfile] end

FROM base AS referee
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright
RUN playwright install --with-deps chromium && chmod -R a+rX /opt/ms-playwright
USER 1000:1000
WORKDIR /work
