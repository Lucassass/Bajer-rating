import sqlite3
from database import create_connection, close_connection
from flask import Flask, render_template

app = Flask(__name__)

app.env = 'development'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/beerlist')
def beerlist():
    conn = create_connection()
    conn.row_factory = sqlite3.Row

    c = conn.cursor()
    c.execute('SELECT * FROM bajer')

    rows = c.fetchall()

    close_connection(conn)
    return render_template('bajerlist.html', posts=rows)

if __name__ == "__main__":
    app.run(debug=True)
