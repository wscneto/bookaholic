import sys, os
from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.db import get_connection

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"service": "review", "status": "running"})

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.json
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO reviews (user_id, book_id, rating, comment) VALUES (%s, %s, %s, %s)", (data['user_id'], data['book_id'], data['rating'], data['comment']))
    db.commit()
    return jsonify({"message": "Review added"}), 201

@app.route('/reviews/book/<int:book_id>', methods=['GET'])
def get_reviews(book_id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reviews WHERE book_id=%s", (book_id,))
    return jsonify(cursor.fetchall())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)