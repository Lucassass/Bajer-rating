import sqlite3

def create_connection():
    conn = sqlite3.connect('db.db')
    print('Database connected')
    return conn

def close_connection(conn):
    conn.commit()
    conn.close()
    print("Database closed")
