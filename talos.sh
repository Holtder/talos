#!/bin/bash

envname=".env"
# If the virtual environment folder does not exist, stop the process
if [ ! -d "$envname" ]; then
    echo "Warning: Virtual Environment (.env) not properly set up, please check if you followed the installation instructions in README.MD!"
    exit 1
fi
source "$envname"/bin/activate || exit 1

case "$0" in

"start")   
    echo "Initializing Talos";

    pyv="$(redis-cli ping)"
    if [ "$pyv" != "PONG" ]; then
        echo "No Redis found, starting.."
        redis-server --daemonize yes || exit 1
    fi

    echo "Killing all existing Talos celery workers (if any) and restarting.."
    celery -A entrypoint_celery control shutdown > /dev/null 2>&1
    celery -A entrypoint_celery.celery --detach worker || exit 1

    echo "Killing Talos webserver(if any) and restarting.."

    python entrypoint_app.py &

    echo "Successfully started Talos; you can now access it on 127.0.0.1:5000"

"stop")
    echo
esac