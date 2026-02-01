import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run_poc_test():
    print("🚀 Starting FastAPI POC Consumer Test...\n")

    # 1. Create a User
    user_data = {"name": "Surabhi Verma", "email": "surabhi@example.com", "role": "Admin"}
    user_res = requests.post(f"{BASE_URL}/users/", json=user_data)
    user = user_res.json()
    user_id = user.get("id")
    print(f"✅ User Created: {user['name']} (ID: {user_id})")

    # 2. Create Products
    products = [
        {"name": "Laptop", "price": 1200.0, "category": "Electronics"},
        {"name": "Mouse", "price": 25.0, "category": "Accessories"}
    ]
    product_ids = []
    for p in products:
        p_res = requests.post(f"{BASE_URL}/products/", json=p)
        product_ids.append(p_res.json().get("id"))
    print(f"✅ Products Created: {len(product_ids)} items")

    # 3. Create an Order (Linking User and Products)
    order_data = {
        "user_id": user_id,
        "items": [
            {"product_id": product_ids[0], "quantity": 1},
            {"product_id": product_ids[1], "quantity": 2}
        ]
    }
    order_res = requests.post(f"{BASE_URL}/orders/", json=order_data)
    print(f"✅ Order Placed: ID {order_res.json().get('id')}")

    # 4. Fetch the Complex Summary (Data Massage)
    summary_res = requests.get(f"{BASE_URL}/users/{user_id}/orders-summary")
    print("\n📊 USER ORDER SUMMARY (Massaged Data):")
    print(json.dumps(summary_res.json(), indent=4))

if __name__ == "__main__":
    try:
        run_poc_test()
    except Exception as e:
        print(f"❌ Connection failed. Is the FastAPI server running? \nError: {e}")