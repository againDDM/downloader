#!/usr/bin/env python3
import os
import sqlite3
import youtube_dl
from flask import Flask, url_for, \
    redirect, request, g, jsonify
from flask_cors import CORS


###  >>> CONFIG SECTION <<<

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(
    dict(
        DATABASE=os.getenv('SQLITE_PATH', 'app-db.sqlite3'),
        DEBUG=True,   # will be switched to False
        PAGE_LIMIT=20,
    )
)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
CORS(app, resources={r"/*": {"origins": "*"}})


### <<<------ end of section ------>>>


###  >>> DATABASE SECTION <<<
### --- global subsection ---

def connect_db():
    """Connects to the specified database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """If there is no connection to the database yet,
    open a new one - for the current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

### --- buisness logical subsection ---

def validate_task(url):
    try:
        with youtube_dl.YoutubeDL() as yadl:
            yadl.extract_info(url, download=False)
    except Exception as err:
        return err.args[0]
    else:
        return None

def show_tasks(limit):
    """Send last tasks in JSON format"""
    db = get_db()
    cur = db.execute(
        'SELECT url, status FROM tasks ORDER BY timestamp DESC LIMIT ?',
        (limit,)
    )
    tasks = [
        {
            "url": row[0],
            "status": row[1],
        } 
            for row in cur.fetchall()
              ]
    return jsonify({'result': 'success', 'tasks': tasks})

def add_task(url):
    """Add new task to database with specified url,
    current timestamp and WAIT status.
    """
    invalid = validate_task(url)
    if invalid:
        return jsonify({'result': str(invalid)}), 400
    db = get_db()
    try:
        db.execute("INSERT INTO tasks (url) values (?)", (url,))
    except sqlite3.IntegrityError:
        db.execute(
            "UPDATE tasks SET timestamp=CURRENT_TIMESTAMP WHERE url=?",
            (url,)
            )
        return jsonify({'result': 'exist', 'task': url}), 201
    else:
        return jsonify({'result': 'success', 'task': url}), 201
    finally:
        db.commit()

def delete_task(url):
    """Delete task specified by url from database."""
    db = get_db()
    db.execute("DELETE FROM tasks WHERE url=?", (url,))
    db.commit()
    return jsonify({'result': 'deleted', 'task': url}), 200

### <<<------ end of section ------>>>

### >>> ROUTER SECTION <<<
### --- api subsection ---

@app.route('/api/tasks/', methods=['GET', 'POST', 'DELETE'])
def handle_tasks():
    """Methods router"""
    if request.method == 'GET':
        return show_tasks(app.config['PAGE_LIMIT'])
    if request.method == 'POST':
        return add_task(request.json['url'])
    elif request.method == 'DELETE':
        return delete_task(request.json['url'])

@app.route('/ping', methods=['GET'])
def ping_pong():
    """sanity check route"""
    return jsonify('pong!')

### <<<------ end of section ------>>>

if __name__ == "__main__":
    app.run(host='0.0.0.0')
