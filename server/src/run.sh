#!/bin/sh -x

mkdir -p /opt/db
sqlite3 \
  -batch \
  /opt/db/app-db.sqlite3 \
  "CREATE TABLE tasks (
      url TEXT NOT NULL PRIMARY KEY,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
      status TEXT NOT NULL DEFAULT 'WAIT'
  );"

downloader () {
  while sleep 1; do
    python3 downloader.py
  done
}

downloader &

gunicorn \
  --bind 0.0.0.0:5000 \
  --workers 4 \
  --umask 007 \
  --max-requests 64 \
  --graceful-timeout 60 \
  --preload \
  wsgi:app
