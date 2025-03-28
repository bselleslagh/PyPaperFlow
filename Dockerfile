FROM python:3.13-slim-bookworm

# Install curl for UV installation and browser dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    # Browser dependencies
    glib-2.0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libexpat1 \
    libatspi2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project into the intermediate image
COPY src/html2pdf/ /app/src/html2pdf/
COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock
COPY README.md /app/README.md

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache --no-dev

# Install playwright.
RUN uv run playwright install

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "/app/src/html2pdf/main.py", "--port", "8000", "--host", "0.0.0.0"]