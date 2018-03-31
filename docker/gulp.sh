#!/usr/bin/env bash
docker exec -it eatbot_nginx bash -c "npm i && ./node_modules/.bin/gulp"