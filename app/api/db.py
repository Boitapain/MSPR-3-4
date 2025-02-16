import sqlite3
import bcrypt
import pandas as pd
from io import StringIO

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

def update_diseases(df):
    """Update diseases in the database."""
    conn = create_connection()
    df = pd.read_json(StringIO(df))

# Check if 'Id' column exists, if not, generate IDs
    if 'Id' not in df.columns:
        df['Id'] = range(1, len(df) + 1)

    df.to_sql('Disease', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
    
    diseases = get_diseases()
    print(diseases)
    
    json_df = '[{"Nom":"COVID-19","Country_Region":"USA","Confirmed":5000000,"Deaths":150000,"Recovered":2500000,"Active":2350000,"New_cases":50000,"New_deaths":1000,"New_recovered":20000},{"Nom":"Ebola","Country_Region":"Congo","Confirmed":3000,"Deaths":2000,"Recovered":800,"Active":200,"New_cases":50,"New_deaths":20,"New_recovered":30},{"Nom":"SARS","Country_Region":"China","Confirmed":8000,"Deaths":774,"Recovered":7000,"Active":226,"New_cases":100,"New_deaths":10,"New_recovered":50},{"Nom":"MERS","Country_Region":"Saudi Arabia","Confirmed":2600,"Deaths":858,"Recovered":1400,"Active":242,"New_cases":20,"New_deaths":5,"New_recovered":10}]'
    update_diseases(json_df)
    
    diseases = get_diseases()
    print("\n\n\nUpdated Diseases:", diseases)