import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS',silent=True)
DATABSE = '/root/mydb'

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit
def add_entry():
    g.db.execute('insert into CA_Info(id, password)values(?, ?)',
                 ['hhh'])
    g.db.commit()
    print('inser ok')

def query():
    cur = g.db.execute('select id, password from CA_Info order by in desc')
    for row in cur.fetchall():
        print (row)
    print('quer ok')

def delete():
    g.db.execute('drop ')

if __name__ == '__main__':
    app.run()