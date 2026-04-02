import json

DATA_FILE = "data.json"

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def track_order(order_id):
    data = load_data()
    orders = data["orders"]

    if order_id in orders:
        return f"Order {order_id} is {orders[order_id]['status']}"
    else:
        return "Order not found"


def cancel_order(order_id):
    data = load_data()
    orders = data["orders"]

    if order_id in orders:
        orders[order_id]["status"] = "cancelled"
        save_data(data)  # ✅ persist change
        return f"Order {order_id} has been cancelled"
    else:
        return "Order not found"


def return_policy():
    return "You can return products within 7 days of delivery."