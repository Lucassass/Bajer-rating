import gc
from flask import Flask, render_template, request, url_for, redirect, session
from wtforms import Form, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from model import create_connection, close_connection, create_tables, insert_user, retrieve_user
from model import get_beer

app = Flask(__name__)

app.env = 'development'
app.config['SECRET_KEY'] = 'asd'
app.config['SESSION_TYPE'] = 'memcache'

app.debug = True

create_tables()

class RegistrationForm(Form):
    username = TextField('Username', [
        validators.Length(min=3, max=20),
        validators.DataRequired()
    ])
    name = TextField('Name', [validators.DataRequired()])
    email = TextField('Email Address', [])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = TextField('Username', [
        validators.Length(min=3, max=20),
        validators.DataRequired()
    ])
    password = PasswordField('Password', [validators.DataRequired()])

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/beerlist')
def beerlist():
    rows = get_beer()
    return render_template('bajerlist.html', posts=rows)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        print(form.username.data, form.email.data, form.password.data)
        username = form.username.data
        name = form.name.data
        password = sha256_crypt.encrypt(str(form.password.data))
        email = form.email.data

        conn, c = create_connection()
        c.execute('SELECT count(*) FROM users WHERE username = (?)', (username,))
        x = c.fetchone()
        close_connection(conn)

        if x[0] > 0:
            print("User already found")
            return render_template('register.html', form=form)
        else:
            insert_user(username, password, name, email)
            print("Added user")
            gc.collect()

            session['logged_in'] = True
            session['username'] = username

            return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if request.method == 'POST':# and form.validate():
        data = retrieve_user(request.form['username'])
        if sha256_crypt.verify(request.form['password'], data[2]):
            session['logged_in'] = True
            session['username'] = request.form['username']

            print('Logged in')
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials, try again'
            print('Invalid credentials')

        gc.collect()
        return render_template('login.hmtl', error=error)
    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run()
