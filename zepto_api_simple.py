from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

app = Flask(__name__)
CORS(app, origins = ["http://localhost:5000", "http://localhost:5010"])
app.config["JWT_SECRET_KEY"] = "zepto-clone-secret-key-change-me-in-production-123"

jwt = JWTManager(app)

import traceback

products = [
    {
        "id": 1,
        "name": "Amul Milk 1L",
        "price": 30,
        "category": "Dairy",
        "stock": 50
    },
    {
        "id": 2,
        "name": "Banana 1kg",
        "price": 40,
        "category": "Fruits",
        "stock": 30
    },
    {
        "id": 3,
        "name": "Lays Classic",
        "price": 20,
        "category": "Snacks",
        "stock": 100
    }
]

users = [
         {"username" : "admin",
          "password" : "admin@123",
          "role" : "admin"},

         {"username" : "billa",
          "password" : "billa@123",
          "role" : "customer"},

         {"username" : "ramesh",
          "password" : "ramesh@123",
          "role" : "rider"}
]

# cart = {username : [ {"product_id" : 1, "qty" : 2} ]}
carts = {}

orders = []


@app.route("/login", methods = ["POST"])
def login():

    data = request.get_json()

    username = data["username"]
    password = data["password"]

    for user in users:

        if (user["username"] == username) and (user["password"] == password):

            token = create_access_token(identity = username)

            return jsonify({"message" : "Login Successful",
                            "access_token" : token}), 200

    return jsonify({"message" : "Invalid username or password"}), 401


@app.route("/products/<int:id>", methods = ["GET", "PUT", "PATCH", "DELETE"])
@jwt_required()
def product_by_id(id):

    username = get_jwt_identity()
    print("api called by user : ", username)

    #id in <int:id> is path parameter
    if request.method == "GET":
        for product in products:
            if product["id"] == id:
                return jsonify(product), 200

        return jsonify({"message" : "Product not found!"}), 404

    if request.method == "PUT":

        data = request.get_json()
        try:
            name = data["name"]
            price = data["price"]
            category = data["category"]
            stock = data["stock"]

            for product in products:

                if id == product["id"]:
                    product["name"] = name
                    product["price"] = price
                    product["category"] = category
                    product["stock"] = stock

                    return jsonify(product), 200

            return jsonify({"message" : "Product not found!"}), 404

        except Exception as e:
            return traceback.format_exc()

    if request.method == "PATCH":
        data = request.get_json()

        for product in products:

            if product["id"] == id:

                if "name" in data:
                    product["name"] = data["name"]

                if "price" in data:
                    product["price"] = data["price"]

                if "category" in data:
                    product["category"] = data["category"]

                if "stock" in data:
                    product["stock"] = data["stock"]

                return jsonify(product), 200

        return jsonify({"message" : "Product not found!, cannot update!"}), 404

    if request.method == "DELETE":

        for product in products:
            if product["id"] == id:
                products.remove(product)

                return jsonify({"message" : "Product deleted successfully"}), 200

        return jsonify({"message" : "Product not found!"}), 404


@app.route("/products", methods = ["GET", "POST"])
@jwt_required()
def products_api():

    username = get_jwt_identity()
    print("api called by user : ", username)

    if request.method == "GET":

        #query parameters are category and max_price (both optional)
        category = request.args.get("category", None)
        max_price = request.args.get("max_price", None)

        result = []

        for product in products:

            if category and product["category"].lower() != category.lower():
                continue

            if max_price and product["price"] > float(max_price):
                continue

            result.append(product)

        return jsonify(result), 200

    if request.method == "POST":

        data = request.get_json()

        id = data["id"]

        for product in products:
            if id == product["id"]:
                return jsonify({"message" : "id already exists, cannot create with this id!"}), 409

        name = data["name"]
        price = data["price"]
        category = data["category"]
        stock = data["stock"]

        product = { "id" : id,
                    "name" : name,
                    "price" : price,
                    "category" : category,
                    "stock" : stock
                    }

        products.append(product)

        return jsonify(product), 201


@app.route("/cart/<int:product_id>", methods = ["DELETE"])
@jwt_required()
def cart_remove(product_id):

    username = get_jwt_identity()
    print("api called by user : ", username)

    cart = carts.get(username, [])

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)

            return jsonify({"message" : "Item removed from cart"}), 200

    return jsonify({"message" : "Item not in cart!"}), 404


@app.route("/cart", methods = ["GET", "POST"])
@jwt_required()
def cart_api():

    username = get_jwt_identity()
    print("api called by user : ", username)

    if username not in carts:
        carts[username] = []

    cart = carts[username]

    if request.method == "GET":

        items = []
        total = 0

        for item in cart:
            for product in products:
                if product["id"] == item["product_id"]:
                    items.append({"product_id" : product["id"],
                                  "name" : product["name"],
                                  "price" : product["price"],
                                  "qty" : item["qty"]})
                    total = total + product["price"] * item["qty"]

        return jsonify({"items" : items, "total" : total}), 200

    if request.method == "POST":

        data = request.get_json()

        product_id = data["product_id"]
        qty = data["qty"]

        for product in products:

            if product["id"] == product_id:

                if qty > product["stock"]:
                    return jsonify({"message" : "Not enough stock!"}), 400

                for item in cart:
                    if item["product_id"] == product_id:
                        item["qty"] = item["qty"] + qty
                        return jsonify(item), 200

                item = {"product_id" : product_id, "qty" : qty}
                cart.append(item)

                return jsonify(item), 201

        return jsonify({"message" : "Product not found!"}), 404


@app.route("/orders/<int:id>", methods = ["GET", "PATCH"])
@jwt_required()
def order_by_id(id):

    username = get_jwt_identity()
    print("api called by user : ", username)

    for order in orders:

        if order["id"] == id:

            if request.method == "GET":
                return jsonify(order), 200

            if request.method == "PATCH":
                data = request.get_json()

                if "status" in data:
                    order["status"] = data["status"]

                return jsonify(order), 200

    return jsonify({"message" : "Order not found!"}), 404


@app.route("/orders", methods = ["GET", "POST"])
@jwt_required()
def orders_api():

    username = get_jwt_identity()
    print("api called by user : ", username)

    if request.method == "GET":

        result = []

        for order in orders:
            if order["username"] == username:
                result.append(order)

        return jsonify(result), 200

    if request.method == "POST":

        cart = carts.get(username, [])

        if len(cart) == 0:
            return jsonify({"message" : "Cart is empty!"}), 400

        items = []
        total = 0

        for item in cart:
            for product in products:
                if product["id"] == item["product_id"]:

                    if item["qty"] > product["stock"]:
                        return jsonify({"message" : "Not enough stock for " + product["name"]}), 400

                    items.append({"product_id" : product["id"],
                                  "name" : product["name"],
                                  "price" : product["price"],
                                  "qty" : item["qty"]})
                    total = total + product["price"] * item["qty"]

        for item in cart:
            for product in products:
                if product["id"] == item["product_id"]:
                    product["stock"] = product["stock"] - item["qty"]

        order = { "id" : len(orders) + 1,
                  "username" : username,
                  "items" : items,
                  "total" : total,
                  "status" : "placed"
                  }

        orders.append(order)
        carts[username] = []

        return jsonify(order), 201


if __name__ == "__main__":
   app.run(debug=True)
