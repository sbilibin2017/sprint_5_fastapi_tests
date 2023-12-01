#!/bin/bash


echo "Waiting for redis..."
while ! nc -z redis $REDIS_PORT; do
  sleep 1
done
echo "Redis started"

echo "Waiting for elasticsearch..."
while ! nc -z elasticsearch $ELASTIC_PORT; do
  sleep 1
done
echo "Elasticsearch started"

echo "Waiting for api..."
while ! nc -z api 8000; do
  sleep 1
done
echo "Api started"

python3 main.py