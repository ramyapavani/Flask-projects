from flask import Flask, request, render_template,redirect, url_for, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
app=Flask(__name__)
app.secret_key="wela_secret"
users={}

def insert_chat(user_id, message, response):
    conn = sqlite3.connect('assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history (user_id, message, response, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (user_id, message, response, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def get_chat_history(user_id):
    conn = sqlite3.connect('assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT message, response, timestamp FROM chat_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
    ''', (user_id,))
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_message = request.form['message']
    bot_response = f"You said: {user_message}"  # Replace with actual bot logic later

    insert_chat(session['user_id'], user_message, bot_response)
    return redirect(url_for('home'))


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]

    users = session.get("users", {})

    if username in users:
        return "Username already exists!"

    users[username] = password
    
    session["users"] = users
    session["username"] = username
    return redirect(url_for("index"))

@app.route("/signin", methods=["POST"])
def signin():
    username = request.form["username"]
    password = request.form["password"]

    users = session.get("users", {})
    if username in users and users[username] == password:
        session["username"] = username
        return redirect(url_for("index"))

    return "Invalid username or password"

@app.route('/login',methods=['POST'])
def login():
    username=request.form.get('username')
    password=request.form.get('password')
    stored_password=users.get(username)
    if stored_password and check_password_hash(stored_password, password):
        session['username']=username
        return redirect(url_for('index'))
    else:
        return "Invalid username or password", 401
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.config['SESSION_TYPE']='filesystem'
app.secret_key='Past Queries'
Session(app)

@app.route('/',methods=['GET','POST','PUT','PATCH','DELETE'])
def index():
    if'query_history' not in session:
        session['query_history']=[]
    if request.method=='POST':
        user_query=request.form.get('userquery')
        if user_query:
            history=session['query_history']
            history.insert(0, user_query)
            session['query_history']=history[:15]
            return redirect(url_for('index',show_history=request.args.get('show_history')))
            
    return render_template("chat.html",chat_history=[], queries=session.get('query_history',[]))
@app.route('/clear_history')
def clear_history():
    session['query_history']=[]
    return redirect(url_for('index'))
@app.route('/hearts')
def hearts():
    return render_template('chat.html', queries=session.get('query_history', []), show_hearts=True)
if __name__ == "__main__":
    app.run(debug=True) 