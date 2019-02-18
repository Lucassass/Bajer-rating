from flask import Flask, render_template, g
from model import Model
app = Flask(__name__)

app.env = 'development'

model = Model()

def get_db():
    return model.db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/db')
def db():
    conn = get_db()
    return render_template('data_test.html')

if __name__ == "__main__":
    app.run(debug=True)
