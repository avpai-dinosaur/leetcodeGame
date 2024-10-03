import flask
import sqlite3

app = flask.Flask(__name__)

@app.route("/")
def index():
    board_html = "<h1>Leaderboard</h1>"
    for user in query_db("select * from scores"):
        board_html += f"<p>{user["username"]}, {user["score"]}</p>"
    return board_html


@app.route("/upload/", methods=["POST"])
def post_score():
    username = flask.request.form["username"]
    score = flask.request.form["score"]
    query_db("INSERT INTO scores (username, score) VALUES (?, ?)", [username, score])
    return flask.redirect(flask.url_for('index'))

### ==================== DATABASE API ==================== ###


DATABASE_FILENAME = "var/leaderboard.sqlite3"


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Open a new database connection.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if 'sqlite_db' not in flask.g:
        db_filename = DATABASE_FILENAME
        flask.g.sqlite_db = sqlite3.connect(str(db_filename))
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db


def query_db(query, args=(), one=False):
    """Query function that combines getting the cursor, executing, and fetching the results.

    Set one=True for getting one result back

    Example usage 1:
    for user in query_db('select * from scores'):
        print(user['username'], 'has the score', user['score'])

    Example usage 2:
    user = query_db('select * from score where username = ?',
                [the_username], one=True)
    if user is None:
        print('No such user')
    else:
        print(the_username, 'has the score', user['score'])

    Flask docs reccomends using this query function instead of working with
    raw cursor and conection objects:
    https://flask.palletsprojects.com/en/3.0.x/patterns/sqlite3/
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()
