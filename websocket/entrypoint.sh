#!/bin/sh
set -e

# Wait for the PostgreSQL database to be ready
echo "Waiting for database..."
until pg_isready -h db -U "$POSTGRES_USER"
do
  sleep 1
done

# Initialize the database
echo "Database is ready, initializing..."
python init_db.py

# Start the Gunicorn application server
echo "Starting application..."
exec gunicorn --bind 0.0.0.0:5000 app:app
