# Zepto Clone (Quick Commerce Backend)

A learning project: a Zepto-style quick-commerce backend built with Python.

## Files

| File | What it is |
|------|------------|
| `zepto_api_simple.py` | Flask REST API with JWT login, products, cart and orders (in-memory data) |
| `zepto_oop_models.ipynb` | OOP models: User/Customer/Rider, Product types, Inventory, Cart, Order, Delivery |

## Features (API)

- `POST /login` - JWT token
- `GET/POST /products`, `GET/PUT/PATCH/DELETE /products/<id>` - with `category` and `max_price` filters
- `GET/POST /cart`, `DELETE /cart/<product_id>`
- `GET/POST /orders`, `GET/PATCH /orders/<id>`

## Run

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python zepto_api_simple.py
```

API runs at `http://127.0.0.1:5000`.

## Concepts practised

OOP (abstraction, encapsulation, inheritance, polymorphism), REST APIs, JWT auth, Git/GitHub.

## Author

Prince Kumar (Billa) - [princekumar-ds](https://github.com/princekumar-ds)

## Configuration

Set a real JWT secret before running (the built-in default is for local demo only):

```bash
# Windows (cmd)
set JWT_SECRET_KEY=your-own-long-random-string
# Mac/Linux
export JWT_SECRET_KEY=your-own-long-random-string
```

> The users in `zepto_api_simple.py` are demo data with plain-text passwords. Do not reuse them anywhere real.
