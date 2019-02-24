import sqlite3
import gc
from flask import Flask, render_template, request, url_for, redirect, session
from wtforms import Form, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from model import create_connection, close_connection, insert_user, retrieve_users

app = Flask(__name__)


app.env = 'development'
app.config['SECRET_KEY'] = 'asd'
app.config['SESSION_TYPE'] = 'memcache'


app.debug = True


class RegistrationForm(Form):
    username = TextField('username', [
        validators.Length(min=4, max=20),
        validators.Required()
    ])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = TextField('username', [
        validators.Length(min=4, max=20),
        validators.Required()
    ])
    password = PasswordField('New Password', [validators.Required()])

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/beerlist')
def beerlist():
    conn, c = create_connection()
    conn.row_factory = sqlite3.Row

    c.execute('SELECT * FROM bajer')

    rows = c.fetchall()

    close_connection(conn)
    return render_template('bajerlist.html', posts=rows)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm(request.form)

    if request.method == 'POST':
        print(form.username.data, form.email.data, form.password.data)
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        conn, c = create_connection()

        c.execute('SELECT count(*) FROM users WHERE username = (?)', (username,))
        x = c.fetchone()

        if x[0] > 0:
            print("User already found")
            return render_template('register.html', form=form)
        else:
            c.execute('INSERT INTO users (username, password, email) VALUES (?,?,?)', 
                      (username, password, email))

            conn.commit()
            print("Added user")
            c.close()
            conn.close()
            gc.collect()

            session['logged_in'] = True
            session['username'] = username

            return redirect(url_for('index'))
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn, c = create_connection()
    error = ''
    if request.method == 'POST':
        c.execute('SELECT * FROM users WHERE username = (?)', (request.form['username'],))
        data = c.fetchone()

        if sha256_crypt.verify(request.form['password'], data):
            session['logged_in'] = True
            session['username'] = request.form['username']

            print('Logged in')
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials, try again'
            print('Invalid credentials')

        gc.collect()

        return render_template('login.hmtl', error=error)

if __name__ == "__main__":
    app.run()
