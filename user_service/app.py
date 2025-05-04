import sys, os, jwt
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import check_password_hash
from datetime import datetime, timedelta, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.db import get_connection

app = Flask(__name__)
CORS(app)

SECRET_KEY = "your-secret-key"

@app.route('/', methods=['GET'])
def index():
    return jsonify({"service": "user", "status": "running"})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, email, password_hash, is_admin) VALUES (%s, %s, %s, %s)", (data['name'], data['email'], data['password_hash'], data.get('is_admin', False)))
    db.commit()
    return jsonify({"message": "User created"}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, is_admin, created_at FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    return jsonify(user) if user else ("User not found", 404)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (data['email'],))
    user = cursor.fetchone()

    if not user or not check_password_hash(user['password_hash'], data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = jwt.encode({
        'user_id': user['id'],
        'is_admin': user['is_admin'],
        'exp': datetime.now(timezone.utc) + timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({'token': token})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)