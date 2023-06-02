FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn server:app --reload --host 0.0.0.0  && \
    gunicorn -k uvicorn.workers.UvicornWorker