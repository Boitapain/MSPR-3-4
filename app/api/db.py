import sqlite3
import bcrypt

def create_connection():
    conn = sqlite3.connect('disease_track.db')
    return conn

def create_user_table():
    conn = create_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                isAdmin BOOLEAN NOT NULL CHECK (isAdmin IN (0, 1))
            );
        ''')
    conn.close()

def add_user(name, email, password, is_admin=False):
    conn = create_connection()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with conn:
        conn.execute('''
            INSERT INTO users (name, email, password, isAdmin)
            VALUES (?, ?, ?, ?)
        ''', (name, email, hashed_password, is_admin))
    conn.close()

def get_user(email):
    conn = create_connection()
    user = conn.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,)).fetchone()
    conn.close()
    if user:
        return user
    return None

def authenticate_user(email, password):
    conn = create_connection()
    user = conn.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,)).fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[3]):
        return user
    return None

create_user_table()