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

WORKDIR /service_b

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY wait_for.sh ./
RUN chmod +x wait_for.sh

COPY /service_b/tests ./tests/
COPY /service_b/migrations ./migrations/

WORKDIR /service_b/web_app
COPY /service_b/web_app/ .

EXPOSE 8081

ENV PYTHONPATH=/service_b

WORKDIR /service_b

ENTRYPOINT ["/service_b/wait_for.sh", "rabbitmq:5672", "--"]
CMD ["poetry", "run", "python", "web_app/main.py"]