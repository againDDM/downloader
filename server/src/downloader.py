#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sqlite3
import youtube_dl


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


def report(target:str, result:bool) -> None:
    with sqlite3.connect("/opt/db/app-db.sqlite3") as db_connection:
        db_connection.execute(
            "UPDATE tasks SET status=? WHERE url=?",
            ["SUCCESS" if result else "FAILED", target]
            )
        db_connection.commit()

def download(target:str) -> bool:
    dow_dir = os.getenv('DOWNLOADS_DIR', '/opt/downloads')
    os.makedirs(dow_dir, mode=0o755, exist_ok=True)
    ydl_opts = {'outtmpl': '{}/%(title)s.%(ext)s'.format(dow_dir)}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print(f"My target is {target}")
            ydl.download((target,))
    except Exception as err:
        print(target, err)
        return False
    else:
        return True


def main():
    task = get_task()
    if not task:
        return
    report(task, download(task))


if __name__ == "__main__":
    main()
