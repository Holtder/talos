#!/bin/bash
# Work in progress, intent of this file is to check for all necessary services
# And to start any missing services
source .env/bin activate
resp = redis-cli ping

if ["$resp" != "PONG"]
    redis-server start

celery -A talos control shutdown
celery -A talos worker

python run.py