from flask import Flask, request, jsonify
from db import add_user, get_users, authenticate_user, initialize_db

app = Flask(__name__)

# Initialize the database
initialize_db()

@app.route('/users', methods=['GET'])
def users():
    try:
        users = get_users()
        if not users:
            return jsonify({"message": "No users found"}), 404
        return jsonify({"users": users}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400
    try:
        add_user(name, email, password)
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = authenticate_user(email, password)
    if user:
        return jsonify({"user": user}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)