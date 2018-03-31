#!/usr/bin/env bash
docker-compose -f docker-compose.loc-db-dev.yml stop django-dev && docker-compose -f docker-compose.loc-db-dev.yml rm -f django-dev && docker-compose -f docker-compose.loc-db-dev.yml up django-dev
