#!/usr/bin/env bash
set -e

# wait for Postgres
host="$DATABASE_HOST"
port="${DATABASE_PORT:-5432}"

echo "Waiting for Postgres at $host:$port..."
until nc -z "$host" "$port"; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Run migrations
python manage.py migrate --noinput

# Collect static (optional)
# python manage.py collectstatic --noinput

# Decide runtime: if CMD is "gunicorn" we'll start the web server (compose passes args)
exec "$@"
