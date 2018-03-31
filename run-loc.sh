#!/usr/bin/env bash
docker-compose stop django-dev && docker-compose rm -f django-dev && docker-compose up django-dev