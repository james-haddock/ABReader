# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser --disabled-password --gecos "" --home "/app" --shell "/sbin/nologin" --uid "10001" appuser

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/

EXPOSE 8000

RUN chown -R appuser:appuser src/book

USER appuser

WORKDIR /app/src

CMD ["gunicorn", "controller:app", "--bind", "0.0.0.0:8000", "--timeout", "120"]

