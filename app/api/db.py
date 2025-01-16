import sqlite3
import bcrypt



def create_connection():
    """Create a database connection and return the connection object."""
    return sqlite3.connect('app/disease_track.db')

def initialize_db():
    """Initialize the database with the required tables."""
    conn = create_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                isAdmin BOOLEAN NOT NULL DEFAULT 0
            );
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Disease (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Nom TEXT NOT NULL,
                Country_Region TEXT NOT NULL,
                Confirmed INT NOT NULL,
                Deaths INT NOT NULL,
                Recovered INT NOT NULL,
                Active INT NOT NULL,
                New_cases INT NOT NULL,
                New_deaths INT NOT NULL,
                New_recovered INT NOT NULL
            );
        ''')
    conn.commit()
    conn.close()


############### User functions ###############

def add_user(name, email, password, is_admin=False):
    """Add a new user to the database."""
    conn = create_connection()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with conn:
        conn.execute('''
            INSERT INTO users (name, email, password, isAdmin)
            VALUES (?, ?, ?, ?)
        ''', (name, email, hashed_password, is_admin))
    conn.commit()
    conn.close()

def get_user(email):
    """Retrieve a user from the database by email."""
    conn = create_connection()
    with conn:
        user = conn.execute('''
            SELECT * FROM users WHERE email = ?
        ''', (email,)).fetchone()
    conn.close()
    return user

def authenticate_user(email, password):
    """Authenticate a user by email and password."""
    user = get_user(email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user[3]):
        return {"id": user[0], "name": user[1], "email": user[2], "isAdmin": user[4]}
    return None

def get_users():
    """Retrieve all users from the database."""
    conn = create_connection()
    users = conn.execute('''
        SELECT id, name, email, isAdmin FROM users;
    ''').fetchall()
    conn.close()
    return [{"id": user[0], "name": user[1], "email": user[2], "isAdmin": user[3]} for user in users]

############### Disease functions ###############

def get_diseases():
    """Retrieve all diseases from the database."""
    conn = create_connection()
    diseases = conn.execute('''
        SELECT * FROM Disease;
    ''').fetchall()
    conn.close()
    return diseases

if __name__ == "__main__":
    initialize_db()