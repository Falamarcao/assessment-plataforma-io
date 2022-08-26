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
#python manage.py loaddata users.json posts.json reposts.json quote-postings.json

# CREATE SUPER USER
echo "Creating Super User..."
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

# RUN TESTS EVERYTIME
#python manage.py test small_business.users small_business.posts &> test.log

history -c

exec "$@"