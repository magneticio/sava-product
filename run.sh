#!/bin/sh

args="$@"

args="$@ --host 0.0.0.0 --port 8080 --routes /routes.json"

file=/data/db.json
if [ -f $file ]; then
    echo "Found db.json, trying to open"
    args="$args db.json"
else
    echo "Copying default db.json"
    mv /default-db.json /data/db.json
    args="$args db.json"
fi

file=/data/file.js
if [ -f $file ]; then
    echo "Found file.js seed file, trying to open"
    args="$args file.js"
fi

json-server $args
