#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate

# waffle switches
python manage.py create_waffle_switches

# Create superuser if it doesn't exist
python manage.py create_superuser admin@admin.com adminpass

exec "$@"
