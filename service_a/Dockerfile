FROM python:3.12.11-alpine3.22

RUN apk add --no-cache \
    postgresql-dev \
    postgresql-client \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev \
    netcat-openbsd \
    && rm -rf /var/cache/apk/*

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /service_a

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY /service_a/tests ./tests/
COPY /service_a/migrations ./migrations/

WORKDIR /service_a/web_app
COPY /service_a/web_app/ .

EXPOSE 8080

ENV PYTHONPATH=/service_a

WORKDIR /service_a

ENTRYPOINT ["poetry", "run"]
CMD ["gunicorn", "-b", "0.0.0.0:8080", "web_app.main:app"]
