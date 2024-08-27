import sqlite3
from flask import g, Flask, render_template, request, redirect, url_for
import time

DATABASE = 'data.sqlite'
UPDATES = {
    "level" : "UPDATE friendship SET level = :value WHERE rowid=:rid;",
    "gift" : "UPDATE friendship SET gift = :value WHERE rowid=:rid;",
    "lock" : "UPDATE friendship SET locked = :value WHERE rowid=:rid;",
}
DEFAULT_SETTINGS = [
    ["UPDATERATE", 2000],
]
SELECT_FRIENDS = '''SELECT rowid,* FROM friendship ORDER BY name COLLATE NOCASE ASC;'''
NEW_FRIEND = "INSERT INTO friendship VALUES(:name, :level, :gift, :locked);"
DEL_FRIEND = "DELETE FROM friendship WHERE rowid=:rid;"
TABLE_CREATE = "CREATE TABLE friendship(name TEXT, level INT, gift INT, locked INT);"
TABLE_CREATE_SETTINGS = "CREATE TABLE settings(key TEXT PRIMARY KEY, value);"
SETTING_GET = "SELECT key,value FROM settings WHERE key=:key;"
SETTING_SET = "INSERT OR REPLACE INTO settings VALUES (:key, :value);"

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        res = db.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='friendship';''').fetchone()
        if res is None:
            db.execute(TABLE_CREATE)
            db.commit()
        res = db.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='settings';''').fetchone()
        if res is None:
            db.execute(TABLE_CREATE_SETTINGS)
            db.executemany(SETTING_SET, DEFAULT_SETTINGS)
            db.commit()
    db.row_factory = sqlite3.Row
    return db

def getSetting(db: sqlite3.Connection, key, default=None):
    res = db.execute(SETTING_GET, {"key": key}).fetchone()
    if res is None: return default
    else: return res["value"]
def setSetting(db: sqlite3.Connection, key, value):
    db.execute(SETTING_SET, {"key": key, "value": value})
    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.get('/')
def index():
    db = get_db()
    data = db.execute(SELECT_FRIENDS).fetchall()
    return render_template('render.jinja', friendship=data, updaterate=getSetting(db, "UPDATERATE"))

@app.get('/refresh')
def refresh():
    db = get_db()
    data = db.execute(SELECT_FRIENDS).fetchall()
    return {"updaterate" : getSetting(db, "UPDATERATE"), "items": [dict(d) for d in data]} # that latter part is lame and annoying.


@app.get('/adminpanel')
def admin():
    db = get_db()
    data = db.execute(SELECT_FRIENDS).fetchall()
    return render_template('controlpanel.jinja', friendship=data, updaterate=getSetting(db, "UPDATERATE"))
@app.post('/adminpanel')
def newfriend():
    data = request.form
    db = get_db()
    db.execute(NEW_FRIEND, data)
    db.commit()
    return redirect(url_for('admin'))

@app.post('/adminpanel/refreshtimer')
def refreshtimer():
    data = request.form
    setSetting(get_db(), "UPDATERATE", int(data["refreshtime"]))
    return redirect(url_for('admin'))

@app.get('/adminpanel/<iid>/<attr>/<value>')
def update(iid, attr, value):
    db = get_db()
    db.execute(UPDATES[attr], {"value": value, "rid": iid})
    db.commit()
    return redirect(url_for('admin'))

@app.get('/adminpanel/newday')
def newday():
    db = get_db()
    db.execute("UPDATE friendship SET gift = 0;")
    db.commit()
    return redirect(url_for('admin'))

@app.get('/adminpanel/delete/<iid>')
def delfriend(iid):
    db = get_db()
    db.execute(DEL_FRIEND, {"rid": iid})
    db.commit()
    return redirect(url_for('admin'))
