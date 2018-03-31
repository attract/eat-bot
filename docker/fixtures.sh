#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

ARGS=$@

FIXTURES="test.json test.json"

if [ "$ARGS" == "" ];
then
    echo "Loading fixtures:"
    echo ""
    echo "${FIXTURES}"
    echo ""

    ${DIR}/manage.sh loaddata ${FIXTURES}
else
    ${DIR}/manage.sh loaddata ${ARGS}
fi