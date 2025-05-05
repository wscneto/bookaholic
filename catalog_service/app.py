import sys, os, jwt
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.db import get_connection

load_dotenv()

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")

@app.route('/', methods=['GET'])
def index():
    return jsonify({"service": "catalog", "status": "running"})

@app.route('/books', methods=['GET'])
def get_books():
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    return jsonify(cursor.fetchall())

@app.route('/books/search', methods=['GET'])
def search_books():
    query = request.args.get('q', '')
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE title LIKE %s", (f"%{query}%",))
    return jsonify(cursor.fetchall())

@app.route('/books', methods=['POST'])
def add_book():
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

    if not payload.get('is_admin'):
        return jsonify({'error': 'Only admins can add books'}), 403

    data = request.json
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO books (title, author, description, price, stock, cover_url) VALUES (%s, %s, %s, %s, %s, %s)", (data['title'], data['author'], data['description'], data['price'], data['stock'], data['cover_url']))
    db.commit()
    return jsonify({"message": "Book added"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)