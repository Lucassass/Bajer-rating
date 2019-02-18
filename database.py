import sqlite3

def create_connection():
    conn = sqlite3.connect('db.db')
    print('Database connected')
    return conn

def create_table(conn):
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS Bajer (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        navn TEXT NOT NULL UNIQUE,
        rating INTEGER NOT NULL
        )
    ''')

def close_connection(conn):
    conn.commit()
    conn.close()
