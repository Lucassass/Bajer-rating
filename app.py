import sqlite3

def create_connection():
    conn = sqlite3.connect('db.db')
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

conn = create_connection()
create_table(conn)

c = conn.cursor()

try:
    c.execute('''
        INSERT INTO Bajer (navn, rating) VALUES ('Carlsberg pilser', 6), ('Carlsberg nordic', 5)
    ''')
except:
    pass

c.execute('''
SELECT * FROM Bajer
''')

rows = c.fetchall()

print(rows)

#c.execute('''DROP TABLE Bajer''')

print('It\'s Alive')

close_connection(conn)
