import sqlite3

import click
from flask import current_app, g  #g is a special objects that stores a connection and prevents multiple connection if it has already been established
#current_app it is a special object that points application requesting teh connection. 
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db',None)

    if db is not None:
        db.close()