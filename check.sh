#!/bin/bash

URL="https://www.google.com"

echo "Checking $URL ..."
STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" $URL)

if [ "$STATUS_CODE" -eq 200 ]; then
  echo "$URL is up! Status: $STATUS_CODE"
else
  echo "$URL might be down. Status: $STATUS_CODE"
  exit 1
fi
