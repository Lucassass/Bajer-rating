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

def create_tables():
    conn, c = create_connection()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT
    );
    CREATE TABLE IF NOT EXISTS bajer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producer TEXT NOT NULL,
        name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        poster TEXT NOT NULL
    )
    ''')
    print("Tables created")
    close_connection(conn)

def insert_user(username, password, name, email=None):
    conn, c = create_connection()
    c.execute('INSERT INTO users (username, password, name, email) VALUES (?,?,?,?)',
              (username, password, name, email))
    close_connection(conn)

def retrieve_users():
    conn, c = create_connection()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    close_connection(conn)
    return users

def retrieve_user(username):
    conn, c = create_connection()
    c.execute('SELECT * FROM users WHERE username = (?)', (username,))
    user = c.fetchone()
    print(user, username)
    close_connection(conn)
    return user

def add_beer(producer, name, rating, poster):
    conn, c = create_connection()
    c.execute('INSERT INTO bajer (producer, name, rating, poster) VALUES (?,?,?,?)',
              (producer, name, rating, poster))
    close_connection(conn)

def get_beer():
    conn, c = create_connection()
    conn.row_factory = sqlite3.Row

    c.execute('SELECT * FROM bajer')

    beer = c.fetchall()

    close_connection(conn)
    return beer
