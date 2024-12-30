#!/bin/bash
# Healthcheck script to wait for the PostgreSQL database to be ready

until pg_isready -h db -U "$POSTGRES_USER"; do
  echo "Waiting for database..."
  sleep 2
done

exec "$@"