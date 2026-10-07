const express = require("express");
const os = require("os");
const app = express();

app.use(express.json());

const PRODUCT_URL = process.env.PRODUCT_URL || "http://product-service:5000";
const PORT = process.env.PORT || 3000;
const orders = [];

const info = () => ({ service: "order-service", language: "Node.js", served_by: os.hostname() });

app.get("/orders/health", (req, res) => res.json({ status: "ok", ...info() }));
app.get("/orders", (req, res) => res.json({ orders, ...info() }));

app.post("/orders", async (req, res) => {
  const productId = Number(req.body.product_id);
  const qty = Number(req.body.qty || 1);
  try {
    const r = await fetch(`${PRODUCT_URL}/products/${productId}`);
    if (!r.ok) return res.status(404).json({ error: "Sản phẩm không tồn tại" });
    const { product } = await r.json();
    const order = {
      id: orders.length + 1,
      product: product.name,
      qty,
      total: product.price * qty,
      time: new Date().toISOString()
    };
    orders.push(order);
    res.status(201).json({ order, ...info() });
  } catch (err) {
    res.status(503).json({ error: "Không gọi được product-service", detail: err.message });
  }
});

app.post("/orders/crash", (req, res) => {
  res.json({ message: "order-service sẽ sập sau 0,5 giây..." });
  setTimeout(() => process.exit(1), 500);
});

app.listen(PORT, () => console.log(`order-service chạy ở cổng ${PORT}`));
