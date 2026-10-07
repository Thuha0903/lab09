import os
import socket
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static")

PRODUCTS = [
    {"id": 1, "name": "Áo thun ULSA", "price": 150000},
    {"id": 2, "name": "Balo laptop", "price": 450000},
    {"id": 3, "name": "Bình nước giữ nhiệt", "price": 120000},
]

orders = []

def info():
    return {
        "architecture": "Monolith (1 khối duy nhất)",
        "language": "Python",
        "version": "v1",
        "served_by": socket.gethostname()
    }

@app.get("/")
def index():
    return send_from_directory("static", "index.html")

# ---- Module SẢN PHẨM ----
@app.get("/api/products")
def list_products():
    return jsonify(products=PRODUCTS, **info())

# ---- Module ĐƠN HÀNG ----
@app.get("/api/orders")
def list_orders():
    return jsonify(orders=orders, **info())

@app.post("/api/orders")
def create_order():
    data = request.get_json(force=True)
    pid, qty = int(data.get("product_id")), int(data.get("qty", 1))
    product = next((p for p in PRODUCTS if p["id"] == pid), None)
    if not product:
        return jsonify(error="Sản phẩm không tồn tại"), 404
    order = {
        "id": len(orders) + 1,
        "product": product["name"],
        "qty": qty,
        "total": product["price"] * qty,
        "time": datetime.now().isoformat()
    }
    orders.append(order)
    return jsonify(order=order, **info()), 201

@app.post("/api/orders/crash")
def crash():
    os._exit(1)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  