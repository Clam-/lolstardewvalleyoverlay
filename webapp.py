import sqlite3
from flask import g, Flask, render_template, request, redirect, url_for
import time

DATABASE = 'settings.sqlite'
UPDATES = {
    "level" : "UPDATE friendship SET level = :value WHERE rowid=:rid;",
    "gift" : "UPDATE friendship SET gift = :value WHERE rowid=:rid;",
    "lock" : "UPDATE friendship SET locked = :value WHERE rowid=:rid;",
}
SELECT_FRIENDS = '''SELECT rowid,* FROM friendship ORDER BY name;'''
NEW_FRIEND = "INSERT INTO friendship VALUES(:name, :level, :gift, :locked);"
TABLE_CREATE = "CREATE TABLE friendship(name TEXT, level INT, gift INT, locked INT);"

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        res = db.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='friendship';''').fetchone()
        if res is None:
            db.execute(TABLE_CREATE)
            db.commit()
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.get('/')
def index():
    data = get_db().execute(SELECT_FRIENDS).fetchall()
    return render_template('render.jinja', friendship=data)

@app.get('/refresh')
def refresh():
    data = get_db().execute(SELECT_FRIENDS).fetchall()
    return [dict(d) for d in data] # lame and annoying.


@app.get('/adminpanel')
def admin():
    data = get_db().execute(SELECT_FRIENDS).fetchall()
    return render_template('controlpanel.jinja', friendship=data)

@app.get('/adminpanel/<iid>/<attr>/<value>')
def update(iid, attr, value):
    con = get_db()
    con.execute(UPDATES[attr], {"value": value, "rid": iid})
    con.commit()
    return redirect(url_for('admin'))

@app.post('/adminpanel')
def newfriend():
    data = request.form
    con = get_db()
    con.execute(NEW_FRIEND, data)
    con.commit()
    return redirect(url_for('admin'))
