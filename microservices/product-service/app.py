import os
import socket
from flask import Flask, jsonify

app = Flask(__name__)
VERSION = os.environ.get("VERSION", "v1")
PRODUCTS = [
    {"id": 1, "name": "Áo thun ULSA", "price": 150000},
    {"id": 2, "name": "Balo laptop", "price": 450000},
    {"id": 3, "name": "Bình nước giữ nhiệt", "price": 120000},
]

def info():
    return {
        "service": "product-service",
        "language": "Python",
        "version": VERSION,
        "served_by": socket.gethostname()
    }

@app.get("/products/health")
def health():
    return jsonify(status="ok", **info())

@app.get("/products")
def list_products():
    return jsonify(products=PRODUCTS, **info())

@app.get("/products/<int:pid>")
def get_product(pid):
    for p in PRODUCTS:
        if p["id"] == pid:
            return jsonify(product=p, **info())
    return jsonify(error="Không tìm thấy sản phẩm"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))