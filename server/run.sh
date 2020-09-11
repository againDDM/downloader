#!/bin/sh -x

mkdir -p "/opt/db"
sqlite3 \
  -batch \
  "/opt/db/app-db.sqlite3" \
  "CREATE TABLE IF NOT EXISTS tasks (
      url TEXT NOT NULL PRIMARY KEY,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
      status TEXT NOT NULL DEFAULT 'WAIT'
  );"
chown -R nobody "/opt/db"

downloader () {
    python3 downloader.py
}

downloader &
