import requests
import random

BASE_URL = "http://127.0.0.1:8000"

def populate():
    for i in range(1, 101):
        payload = {
            "name": f"Product_{i}",
            "price": round(random.uniform(10.0, 1000.0), 2),
            "category_id": 1,
            "details": {
                "brand": "BrandName",
                "weight": f"{random.randint(1, 5)}kg",
                "in_stock": True
            }
        }
        requests.post(f"{BASE_URL}/products/", json=payload)

if __name__ == "__main__":
    populate()