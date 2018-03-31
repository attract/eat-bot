#!/usr/bin/env bash
docker exec -it petrater_nginx bash -c "npm i && ./node_modules/.bin/gulp"