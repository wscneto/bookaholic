import sys, os
from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.db import get_connection

app = Flask(__name__)
CORS(app)

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

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
    orders = cursor.fetchall()

    for order in orders:
        cursor.execute("""
            SELECT 
                oi.book_id, 
                oi.quantity, 
                oi.price, 
                b.title, 
                b.cover_url 
            FROM order_items oi
            JOIN books b ON oi.book_id = b.id
            WHERE oi.order_id = %s
        """, (order['id'],))
        order['items'] = cursor.fetchall()

    return jsonify(orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)