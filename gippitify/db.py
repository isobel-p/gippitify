import sqlite3
from datetime import datetime, date

import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

def get_user(id):
    db = get_db()
    user = db.execute("SELECT * FROM user WHERE id = ?", (id,)).fetchone()

    if user is None:
        return None


    # last = datetime.fromisoformat(user["reset_timestamp"]).date()
    reset_timestamp = user["reset_timestamp"]
    if isinstance(reset_timestamp, datetime):
        last = reset_timestamp.date()
    else:
        last = datetime.fromisoformat(reset_timestamp).date()

    current = date.today()
    
    if last < current:
        db.execute("UPDATE user SET requests = 0, reset_timestamp = CURRENT_TIMESTAMP WHERE id = ?", (user["id"],))
        db.commit()
        user = db.execute("SELECT * FROM user WHERE id = ?", (id,)).fetchone()
    return user
    
def daily_limit():
    db = get_db()
    row = db.execute("SELECT SUM(requests) as total FROM user WHERE date(reset_timestamp) = date('now')").fetchone()
    total = row["total"]
    return total >= 2500

@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)