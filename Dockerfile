FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1
# Create virtual environment outside of the project directory
# to avoid conflicts with volume mounts
ENV UV_PROJECT_ENVIRONMENT="/venv"

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

ENV PATH="/venv/bin:$PATH"

COPY . .

RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.runner.asgi:app --host 0.0.0.0 --port 8000"]
