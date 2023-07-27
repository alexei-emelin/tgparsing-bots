FROM python:3.11-alpine



ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

WORKDIR /app
