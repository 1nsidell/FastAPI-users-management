FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev 

FROM python:3.12.9-alpine3.20 AS runner

WORKDIR /app

COPY --from=builder /app /app

RUN rm -rf /root/.cache \
    && addgroup -S appgroup \
    && adduser -S appuser -G appgroup \
    && chown -R appuser:appgroup /app \
    && apk add --no-cache curl

USER appuser

ENV PATH="/app/.venv/bin:$PATH"

CMD ["sh", "-c", "python -m uvicorn users_management.main:app --host 0.0.0.0 --port 8000 --workers ${APP_WORKERS:-4}"]