import sys, os, jwt
from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.db import get_connection

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")

@app.route('/', methods=['GET'])
def index():
    return jsonify({"service": "recommendation", "status": "running"})

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    # Retrieve token from Authorization header
    token = request.headers.get('Authorization', '').split(' ')[-1]
    
    if not token:
        return jsonify({'error': 'Authorization token is missing'}), 401

    try:
        # Decode the JWT token and get the user_id
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    # Retrieve the authors from the user's wishlist
    cursor.execute("""
        SELECT DISTINCT b.author
        FROM books b
        JOIN wishlist w ON b.id = w.book_id
        WHERE w.user_id = %s
    """, (user_id,))
    authors = [row['author'] for row in cursor.fetchall()]

    if not authors:
        return jsonify([])

    # Build the query to get recommendations based on these authors, excluding books in the user's wishlist
    format_strings = ','.join(['%s'] * len(authors))
    cursor.execute(f"""
        SELECT *
        FROM books
        WHERE author IN ({format_strings})
        AND id NOT IN (
            SELECT book_id FROM wishlist WHERE user_id = %s
        )
        LIMIT 10
    """, (*authors, user_id))

    # Return the list of recommended books
    return jsonify(cursor.fetchall())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
