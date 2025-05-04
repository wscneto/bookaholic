import sys, os
from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.db import get_connection

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"service": "recommendation", "status": "running"})

@app.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.* FROM books b
        JOIN recommendations r ON r.book_id = b.id
        WHERE r.user_id = %s
        ORDER BY r.created_at DESC LIMIT 5
    """, (user_id,))
    return jsonify(cursor.fetchall())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)