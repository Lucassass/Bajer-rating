import sqlite3

def create_connection():
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    print('Database connected')
    return conn, c

def close_connection(conn):
    conn.commit()
    conn.close()
    print("Database closed")

def insert_user(username, password, email=None):
    conn, c = create_connection()
    c.execute('INSERT INTO users (username, password, email) VALUES (?,?,?)', (username, password, email))
    close_connection(conn)

def retrieve_users():
    conn, c = create_connection()
    c.execute('SELECT username, password, email FROM users')
    users = c.fetchall()
    close_connection(conn)
    return users

def add_beer(producer, name, rating, poster):
    conn, c = create_connection()
    c.execute('INSERT INTO bajer (producer, name, rating, poster) VALUES (?,?,?,?)',
              (producer, name, rating, poster))
    close_connection(conn)
