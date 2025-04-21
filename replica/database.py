import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT,
            created_at TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            response TEXT,
            timestamp TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

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
    chats = cursor.fetchall()
    conn.close()
    return chats
