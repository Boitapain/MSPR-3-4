from flask import Flask, request, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from .db import add_user, get_users, authenticate_user, get_diseases, update_diseases, initialize_db
import os
from io import StringIO
import pandas as pd

app = Flask(__name__)

# Initialize the database
initialize_db()

# Swagger UI setup
SWAGGER_URL = '/swagger'
API_URL = '/static/openapi.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Disease Track API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

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

@app.route('/diseases', methods=['GET'])
def diseases():
    try:
        diseases = get_diseases()
        if not diseases:
            return jsonify({"message": "No diseases found"}), 404
        return jsonify({"diseases": diseases}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/update_diseases_route', methods=['PUT'])
def update_diseases_route():
    data = request.get_json()
    df = data.get('diseases')
    
    if df is None or not df:
        return jsonify({"message": "No data provided"}), 400
    if pd.read_json(StringIO(df)).isnull().values.any():
        return jsonify({"message": "Data contains null values"}), 400
    
    try:
        update_diseases(df)
        return jsonify({"message": "Diseases updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)