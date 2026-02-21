# ---- Build stage: install dependencies ----
FROM python:3.13-slim AS builder

# System deps for building Python packages (psycopg2, asyncpg, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=2.1.1
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR /app

# Copy dependency files first (cache layer)
COPY pyproject.toml poetry.lock ./

# Install dependencies into a virtual env inside the project
# --no-root: don't install the project itself yet (source isn't copied)
# --only main: skip dev dependencies
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root --only main

# ---- Runtime stage: slim final image ----
FROM python:3.13-slim

# Runtime system deps
# - libpq5: PostgreSQL client lib (needed by psycopg2/asyncpg at runtime)
# - android-tools-adb: ADB for DroidRun device communication
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    android-tools-adb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the virtual env from builder
COPY --from=builder /app/.venv .venv

# Copy source code
COPY src/ src/
COPY pyproject.toml ./

# Install the project package itself (editable-style, into the existing venv)
ENV PATH="/app/.venv/bin:$PATH"
RUN pip install --no-cache-dir --no-deps -e .

# Default env vars (override at runtime via Akash env or .env mount)
ENV APP_ENV=dev \
    INCLUDE_DOCS=false \
    HEALTH_CHECK_LLM=false

EXPOSE 8000

# Health check using the /health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "portable_brain.app:app", "--host", "0.0.0.0", "--port", "8000"]