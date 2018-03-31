#!/usr/bin/env bash
set -e
cmd="$@"

# Install npm packages
npm install

echo "Run gulp $RUN_GULP"
if [ "$RUN_GULP" != "" ];
then
    nohup ./node_modules/.bin/gulp $RUN_GULP&> output &
else
    nohup ./node_modules/.bin/gulp&> output &
fi

nginx -g "daemon off;"

exec $cmd
