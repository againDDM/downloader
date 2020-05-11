#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import sqlite3
import logging
import youtube_dl


def init_logger(name: str = "downloader") -> logging.Logger:
    "init_logger just init logger"
    log_format = "%(asctime)s <%(name)s> [%(levelname)s] %(message)s"
    log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format=log_format)
    return logging.getLogger(name)


def get_task():
    with sqlite3.connect("/opt/db/app-db.sqlite3") as db_connection:
        cursor = db_connection.cursor()
        query = "SELECT url FROM tasks WHERE STATUS IN ('PROCESSED', 'WAIT') " \
        "ORDER BY status, timestamp ASC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            return None
        query = "UPDATE tasks SET status='PROCESSED' WHERE url=?"
        cursor.execute(query, result)
        db_connection.commit()
        return result[0]


def report(target: str, result: bool) -> None:
    with sqlite3.connect("/opt/db/app-db.sqlite3") as db_connection:
        db_connection.execute(
            "UPDATE tasks SET status=? WHERE url=?",
            ["SUCCESS" if result else "FAILED", target]
            )
        db_connection.commit()


def download(target: str) -> bool:
    dow_dir = os.getenv('DOWNLOADS_DIR', '/opt/downloads')
    os.makedirs(dow_dir, mode=0o755, exist_ok=True)
    ydl_opts = {
        'outtmpl': '{}/%(title)s.%(ext)s'.format(dow_dir),
        'format_resolution': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'logger': LOGGER,
        }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            LOGGER.info("My target is %s", target)
            ydl.download((target,))
            LOGGER.info("Target -->%s<-- DONE", target)
    except Exception as err:
        LOGGER.error("%s :: %s", target, str(err))
        return False
    else:
        return True


def main():
    while True:
        try:
            task = get_task()
            if not task:
                time.sleep(5)
                continue
            report(task, download(task))
        except Exception as err:
            print(err.with_traceback())
            time.sleep(60)


if __name__ == "__main__":
    LOGGER = init_logger()
    main()
