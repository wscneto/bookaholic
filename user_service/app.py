import sys, os, jwt
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import check_password_hash, generate_password_hash
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.db import get_connection

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")

@app.route('/', methods=['GET'])
def index():
    return jsonify({"service": "user", "status": "running"})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    db = get_connection()
    cursor = db.cursor()
    hashed_pw = generate_password_hash(data['password']).decode('utf-8')
    cursor.execute("INSERT INTO users (name, email, password_hash, is_admin) VALUES (%s, %s, %s, %s)", (data['name'], data['email'], hashed_pw, data.get('is_admin', False)))
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

@app.route('/wishlist', methods=['POST', 'OPTIONS'])
def add_to_wishlist():
    if request.method == 'OPTIONS':
        return '', 200

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization token required'}), 401

    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

    user_id = payload['user_id']

    data = request.get_json()
    if not data or 'book_id' not in data:
        return jsonify({'error': 'Missing book_id in request'}), 400

    book_id = data['book_id']

    db = get_connection()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO wishlist (user_id, book_id) VALUES (%s, %s)", (user_id, book_id))
        db.commit()
        return jsonify({'message': 'Book added to wishlist'}), 201
    except:
        return jsonify({'error': 'Book already in wishlist or other error'}), 400


@app.route('/wishlist', methods=['GET'])
def get_wishlist():
    token = request.headers.get('Authorization', '').split(' ')[-1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
    except:
        return jsonify({'error': 'Invalid or missing token'}), 401

    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.* FROM books b
        JOIN wishlist w ON b.id = w.book_id
        WHERE w.user_id = %s
    """, (user_id,))
    return jsonify(cursor.fetchall())

@app.route('/wishlist/<int:book_id>', methods=['DELETE'])
def remove_from_wishlist(book_id):
    token = request.headers.get('Authorization', '').split(' ')[-1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
    except:
        return jsonify({'error': 'Invalid or missing token'}), 401

    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM wishlist WHERE user_id = %s AND book_id = %s", (user_id, book_id))
    db.commit()
    return jsonify({'message': 'Book removed from wishlist'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)