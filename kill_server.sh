#!/bin/bash
redis-server stop
celery -A talos control shutdown