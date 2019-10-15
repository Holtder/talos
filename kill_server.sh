#!/bin/bash
# WiP, script that allows users to kill any running service in relation to this applet
redis-server stop
celery -A talos control shutdown