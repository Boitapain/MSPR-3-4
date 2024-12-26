import sqlite3
import bcrypt

def create_connection():
    """Create a database connection and return the connection object."""
    return sqlite3.connect('your_database.db')

def add_user(name, email, password, is_admin=False):
    """Add a new user to the database."""
    conn = create_connection()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with conn:
        conn.execute('''
            INSERT INTO users (name, email, password, isAdmin)
            VALUES (?, ?, ?, ?)
        ''', (name, email, hashed_password, is_admin))
    conn.close()

def get_user(email):
    """Retrieve a user from the database by email."""
    conn = create_connection()
    user = conn.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,)).fetchone()
    conn.close()
    if user:
        return user
    return None

def authenticate_user(email, password):
    """Authenticate a user by email and password."""
    conn = create_connection()
    user = conn.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,)).fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[3]):
        return user
    return None