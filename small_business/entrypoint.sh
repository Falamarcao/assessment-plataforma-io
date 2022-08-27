#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate --noinput

# CREATE GROUPS
python manage.py create_groups

# ADD DATA - fixtures
python manage.py loaddata customers.json staff.json rooms.json events.json

# RUN TESTS EVERYTIME
python manage.py test small_business.rooms small_business.events &> test.log

# CREATE SUPER USER
echo "Creating Super User..."
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

history -c

exec "$@"