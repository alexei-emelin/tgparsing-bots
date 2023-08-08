#!bin/sh
gunicorn server:app --workers 5 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0