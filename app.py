import gc
from flask import Flask, render_template, request, url_for, redirect, session
from wtforms import Form, TextField, PasswordField, SelectField, validators
from passlib.hash import sha256_crypt
from model import create_connection, close_connection, create_tables, insert_user, retrieve_user
from model import get_beer, add_beer

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

class BeerForm(Form):
    producer = TextField('producer', [validators.DataRequired()])
    name = TextField('name', [validators.DataRequired()])
    rating = SelectField('rating', choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',])


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html', user=session.get('username', None))

@app.route('/beerlist', methods=['GET', 'POST'])
def beerlist():
    if request.method == 'POST':
        producer = request.form['producer']
        name = request.form['name']
        rating = request.form['rating']
        if session.get('username', None) is not None:
            poster = retrieve_user(session.get('username'))
            poster = poster[3]
            add_beer(producer, name, rating, poster)
        else:
            return redirect(url_for('login'))

    rows = get_beer()
    return render_template('bajerlist.html', posts=rows, user=session.get('username', None))

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/addbajer')
def tilføj_bajer():
    return render_template('addbajer.html')

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
            return render_template('register.html', form=form,
                                   user=session.get('username', None))
        else:
            insert_user(username, password, name, email)
            print("Added user")
            gc.collect()

            session['logged_in'] = True
            session['username'] = username

            return redirect(url_for('index'))

    return render_template('register.html', form=form, user=session.get('username', None))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if request.method == 'POST':
        data = retrieve_user(request.form['username'])
        if data is not None:
            if sha256_crypt.verify(request.form['password'], data[2]):

                session['logged_in'] = True
                session['username'] = request.form['username']

                print('Logged in')
                return redirect(url_for('index'))
            else:
                error = 'Invalid credentials, try again'
                print('Invalid credentials')

        gc.collect()
        return render_template('login.html', error=error, form=form,
                               user=session.get('username', None))
    return render_template('login.html', form=form, user=session.get('username', None))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
