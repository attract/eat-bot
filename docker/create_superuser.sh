#!/bin/bash
docker exec -it eatbot_django_dev bash -c "python /app/manage.py shell < /app/scripts/create_superuser.py"