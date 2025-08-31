#!/bin/sh

host=$(echo "$1" | cut -d ':' -f 1)
port=$(echo "$1" | cut -d ':' -f 2)

echo "Waiting for $host:$port to be available..."

while ! nc -z "$host" "$port"; do
  sleep 1
done

echo "$host:$port is available! Starting application..."

shift 2

exec "$@"