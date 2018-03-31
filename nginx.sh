#!/usr/bin/env bash
docker-compose stop django nginx && docker-compose rm -f django nginx && docker-compose up -d django nginx