#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

CONTAINER_ALREADY_STARTED="CONTAINER_ALREADY_STARTED_PLACEHOLDER"
if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    touch $CONTAINER_ALREADY_STARTED
    echo "-- First container startup --"
    # YOUR_JUST_ONCE_LOGIC_HERE
    python manage.py flush --no-input
    python manage.py makemigrations
    python manage.py migrate --noinput
    python manage.py collectstatic
    #python manage.py loaddata users.json posts.json reposts.json quote-postings.json

    # CREATE SUPER USER
    # Look at .env.prod file to setup username and password
    echo "Creating Super User - remember to change the .env.prod file"
    python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
else
    echo "-- Not first container startup --"
fi

history -c

exec "$@"