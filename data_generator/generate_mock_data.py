import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


OUTPUT_DIR = "data/raw"
random.seed(42)
np.random.seed(42)


def generate_customers(n=500):
    states = ["CA", "TX", "NY", "FL", "WA", "IL", "AZ", "GA"]
    return pd.DataFrame({
        "customer_id": range(1, n + 1),
        "first_name": [f"First{i}" for i in range(1, n + 1)],
        "last_name": [f"Last{i}" for i in range(1, n + 1)],
        "email": [f"user{i}@example.com" for i in range(1, n + 1)],
        "state": np.random.choice(states, n),
        "signup_date": [
            (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 700))).date()
            for _ in range(n)
        ],
    })


def generate_products(n=100):
    categories = ["Electronics", "Home", "Clothing", "Books", "Sports"]
    return pd.DataFrame({
        "product_id": range(1, n + 1),
        "product_name": [f"Product_{i}" for i in range(1, n + 1)],
        "category": np.random.choice(categories, n),
        "unit_price": np.round(np.random.uniform(5, 500, n), 2),
    })


def generate_orders(n=3000, customer_count=500, product_count=100):
    start = datetime(2024, 1, 1)
    statuses = ["completed", "cancelled", "returned", "pending"]
    orders = pd.DataFrame({
        "order_id": range(1, n + 1),
        "customer_id": np.random.randint(1, customer_count + 1, n),
        "product_id": np.random.randint(1, product_count + 1, n),
        "order_date": [
            (start + timedelta(days=random.randint(0, 365))).date()
            for _ in range(n)
        ],
        "quantity": np.random.randint(1, 6, n),
        "order_status": np.random.choice(statuses, n, p=[0.72, 0.08, 0.07, 0.13]),
    })
    return orders


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    generate_customers().to_csv(f"{OUTPUT_DIR}/customers.csv", index=False)
    generate_products().to_csv(f"{OUTPUT_DIR}/products.csv", index=False)
    generate_orders().to_csv(f"{OUTPUT_DIR}/orders.csv", index=False)

    print("Generated mock e-commerce files:")
    print(f"- {OUTPUT_DIR}/customers.csv")
    print(f"- {OUTPUT_DIR}/products.csv")
    print(f"- {OUTPUT_DIR}/orders.csv")


if __name__ == "__main__":
    main()
