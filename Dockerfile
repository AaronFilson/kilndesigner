# The server image: the API, the worker, migrations and the CLI, run with different commands
# (see compose.yaml). The web app has its own image, web/Dockerfile.

FROM python:3.14-slim-trixie AS build
COPY --from=ghcr.io/astral-sh/uv:0.13.4 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
WORKDIR /app

# The dependencies first, so a change to the code doesn't reinstall them
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=core/pyproject.toml,target=core/pyproject.toml \
    --mount=type=bind,source=cli/pyproject.toml,target=cli/pyproject.toml \
    --mount=type=bind,source=api/pyproject.toml,target=api/pyproject.toml \
    --mount=type=bind,source=worker/pyproject.toml,target=worker/pyproject.toml \
    uv sync --locked --no-dev --no-install-workspace

COPY pyproject.toml uv.lock ./
COPY core core
COPY cli cli
COPY api api
COPY worker worker
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-dev --no-editable


FROM python:3.14-slim-trixie
# OpenCascade links against OpenGL and X11, though nothing here draws on a screen
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends \
        libgl1 libx11-6 libexpat1 \
    && rm -rf /var/lib/apt/lists/*
RUN useradd --uid 10001 --create-home kilndesigner \
    && mkdir /data && chown kilndesigner /data
COPY --from=build /app/.venv /app/.venv
ENV PATH=/app/.venv/bin:$PATH PYTHONUNBUFFERED=1 KILNDESIGNER_DATA_DIR=/data
USER kilndesigner
WORKDIR /home/kilndesigner
EXPOSE 8000
CMD ["uvicorn", "kilndesigner_api.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
