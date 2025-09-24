# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# System deps (for psycopg2 etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev gcc curl netcat \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first to cache pip install
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copy project
COPY . /app

# Make entrypoint executable
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
