#!/bin/sh
set -e

echo "Waiting for database..."
until pg_isready -h db -U "$POSTGRES_USER"
do
  sleep 1
done

echo "Database is ready, initializing..."
python init_db.py

echo "Starting application..."
exec gunicorn --bind 0.0.0.0:5000 app:app
