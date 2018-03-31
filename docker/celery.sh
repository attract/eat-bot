#!/usr/bin/env bash

COMMAND=$1

##### Run celery
if [ "$COMMAND" == "" ];
then
    echo "Run celery"
    docker exec -it eatbot_celeryworker bash -c "export C_FORCE_ROOT=1 && celery -A config worker -l info -B --autoreload --broker=amqp://guest:guest@rabbitmq:5672//"
fi

##### Stop celery
if [ "$COMMAND" == "stop" ];
then
    echo "Stop celery"
    docker exec -it eatbot_celeryworker bash -c "pkill -9 -f celery"
fi
