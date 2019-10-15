#!/bin/bash
source .env/bin activate
resp = redis-cli ping

if ["$resp" != "PONG"]
    redis-server start

celery -A talos control shutdown
celery -A talos worker

python run.py