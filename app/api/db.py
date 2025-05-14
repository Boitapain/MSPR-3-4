import sqlite3
import bcrypt
import pandas as pd
from io import StringIO

# filepath: /workspaces/MSPR-3-4/app/api/db.py
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
                Id INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Date DATE NOT NULL,
                Country TEXT NOT NULL,
                Confirmed INT NOT NULL,
                Deaths INT NOT NULL,
                Recovered INT NOT NULL,
                New_cases INT NOT NULL,
                New_deaths INT NOT NULL,
                New_recovered INT NOT NULL
            );
        ''')
    conn.commit()
    conn.close()

def populate_disease_table():
    """Populate the Disease table with sample data."""
    conn = create_connection()
    with conn:
        conn.execute('''
            INSERT INTO Disease (Name, Date, Country, Confirmed, Deaths, Recovered, New_cases, New_deaths, New_recovered)
            VALUES 
            (COVID-19,22/1/2020,Afghanistan,0,0,0,0,0,0),
            (COVID-19,22/1/2020,Albania,0,0,0,0,0,0),
            (COVID-19,22/1/2020,Algeria,0,0,0,0,0,0)
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

def update_diseases(df):
    """Update diseases in the database."""
    conn = create_connection()
    df = pd.read_json(StringIO(df))

# Check if 'Id' column exists, if not, generate IDs
    df['Id'] = range(1, len(df) + 1)

    df.to_sql('Disease', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
    # populate_disease_table()