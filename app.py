from flask import Flask, g, render_template

import sqlite3

DATABASE = 'database.db'


#initialize app
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    #home page
    db = get_db()
    cursor = db.cursor()
    sql = "SELECT * FROM books;"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("home.html", results=results)

def query_db(query, args=(), one=False):
    cursor = get_db().execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/book/<int:id>")
def book(id):
    sql = """
            SELECT * FROM Books 
            JOIN Authors ON Books.author_ID = Authors.author_ID
            WHERE Books.book_ID = ?;
            """
    result = query_db(sql, (id,), True)
    return str(result) 

if __name__ == "__main__": 
    app.run(debug=True)