#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "waiting for postgres..."

  while  ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
  done

  echo "postgres started"
fi


alembic upgrade head

exec "$@"
