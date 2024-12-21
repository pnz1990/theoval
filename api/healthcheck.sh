#!/bin/bash

# Wait for the database to be ready
until pg_isready -h db -U "$POSTGRES_USER"; do
  echo "Waiting for database..."
  sleep 2
done

# Run the provided command
exec "$@"