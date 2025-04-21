from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# DB setup
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
init_db()

@app.route('/')
def home():
    return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    if 'username' not in session:
        return render_template('chat.html')
    return render_template('chat.html', username=session['username'])

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    hashed_pw = generate_password_hash(password)

    try:
        with sqlite3.connect('database.db') as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        return redirect(url_for('chat'))
    except sqlite3.IntegrityError:
        return "Username already exists!"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    with sqlite3.connect('database.db') as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['username'] = user[1]
        return redirect(url_for('chat'))
    else:
        return "Invalid credentials!"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run(debug=True)
