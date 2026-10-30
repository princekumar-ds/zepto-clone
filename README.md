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
