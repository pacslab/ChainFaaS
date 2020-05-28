#!/bin/sh

apt-get update
apt-get install -qy netcat

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Waiting for rabbitmq..."

while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
  sleep 0.1
done

echo "RabbitMQ started"

# python manage.py flush --no-input
python manage.py makemigrations --no-input
python manage.py migrate --noinput
python manage.py collectstatic --no-input

exec "$@"