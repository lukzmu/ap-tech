FROM python:3.12.2-slim AS python-base

WORKDIR /app

ENV PYTHONBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/device_monitor


FROM python-base AS builder

ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install -U pip wheel "poetry==1.8.3"

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev \
    && rm -rf ~/.cache


FROM builder AS development

RUN poetry install --only dev \
    && rm -rf ~/.cache
