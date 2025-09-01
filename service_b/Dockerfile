FROM python:3.12.11-alpine3.22

RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev \
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

WORKDIR /service_b/app

COPY service_b/ .

EXPOSE 8081

ENV PYTHONPATH=/service_b/app

ENTRYPOINT ["/service_b/wait_for.sh", "rabbitmq:5672", "--"]
CMD ["poetry", "run", "python", "main.py"]