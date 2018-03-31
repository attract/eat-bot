#!/bin/bash
docker exec -it petrater_django_dev bash -c "python /app/manage.py shell < /app/scripts/create_superuser.py"