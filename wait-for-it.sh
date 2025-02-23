#!/usr/bin/env bash
# wait-for-it.sh

HOST="$1"
PORT="$2"
TIMEOUT="${3:-15}"

echo "Waiting for $HOST:$PORT with timeout $TIMEOUT seconds..."
for i in $(seq 1 $TIMEOUT); do
    nc -z "$HOST" "$PORT" && exit 0
    sleep 1
done
echo "Timeout waiting for $HOST:$PORT"
exit 1
