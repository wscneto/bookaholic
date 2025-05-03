import sys, os
from flask import Flask, request, jsonify
from shared.db import get_connection
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"service": "order", "status": "running"})

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, %s)", (data['user_id'], data['total_amount'], 'created'))
    order_id = cursor.lastrowid

    for item in data['items']:
        cursor.execute("INSERT INTO order_items (order_id, book_id, quantity, price) VALUES (%s, %s, %s, %s)", (order_id, item['book_id'], item['quantity'], item['price']))
    db.commit()
    return jsonify({"message": "Order created", "order_id": order_id}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE id=%s", (order_id,))
    order = cursor.fetchone()
    cursor.execute("SELECT * FROM order_items WHERE order_id=%s", (order_id,))
    order['items'] = cursor.fetchall()
    return jsonify(order)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)