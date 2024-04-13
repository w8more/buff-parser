#!/bin/bash

gunicorn src.entry:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000