#!/bin/sh -ex

sqlite3 \
  -batch \
  ${SQLITE_PATH} \
  "CREATE TABLE tasks (
      url TEXT NOT NULL PRIMARY KEY,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
      status TEXT NOT NULL DEFAULT 'WAIT'
  );"

pwd
ls -lAh ./

gunicorn \
  --bind 0.0.0.0:5000 \
  --workers 4 \
  --umask 007 \
  --max-requests 16 \
  --graceful-timeout 30 \
  --preload \
  wsgi:app
