"""
Generate synthetic e-commerce CSV datasets for quick experiments.

Outputs are written to the `data/` directory relative to this file:
- customers.csv
- products.csv
- orders.csv
- order_items.csv
- reviews.csv
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Sequence


DATA_DIR = Path(__file__).parent / "data"


def write_csv(path: Path, fieldnames: Sequence[str], rows: Sequence[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_customers(count: int = 120) -> List[Dict]:
    first_names = [
        "Alex",
        "Taylor",
        "Jordan",
        "Casey",
        "Morgan",
        "Riley",
        "Quinn",
        "Jamie",
        "Robin",
        "Avery",
    ]
    last_names = [
        "Smith",
        "Johnson",
        "Garcia",
        "Brown",
        "Lee",
        "Martinez",
        "Davis",
        "Lopez",
        "Clark",
        "Walker",
    ]
    cities = [
        ("Seattle", "WA"),
        ("Portland", "OR"),
        ("San Francisco", "CA"),
        ("Los Angeles", "CA"),
        ("Denver", "CO"),
        ("Austin", "TX"),
        ("Chicago", "IL"),
        ("Atlanta", "GA"),
        ("Miami", "FL"),
        ("New York", "NY"),
    ]
    segments = ["consumer", "small_business", "enterprise"]

    customers: List[Dict] = []
    for customer_id in range(1, count + 1):
        first = random.choice(first_names)
        last = random.choice(last_names)
        city, state = random.choice(cities)
        signup_offset = random.randint(90, 720)
        signup_dt = date.today() - timedelta(days=signup_offset)

        customers.append(
            {
                "customer_id": customer_id,
                "first_name": first,
                "last_name": last,
                "email": f"{first.lower()}.{last.lower()}{customer_id}@example.com",
                "city": city,
                "state": state,
                "segment": random.choice(segments),
                "signup_date": signup_dt.isoformat(),
            }
        )

    return customers


def generate_products(count: int = 60) -> List[Dict]:
    categories = {
        "Electronics": ["Headphones", "Laptop", "Smartwatch", "Camera", "Speaker"],
        "Home": ["Vacuum", "Coffee Maker", "Air Fryer", "Blender", "Desk Lamp"],
        "Outdoors": ["Tent", "Backpack", "Water Bottle", "Hiking Boots", "Cooler"],
        "Beauty": ["Serum", "Moisturizer", "Hair Dryer", "Trimmer", "Sunscreen"],
        "Toys": ["Board Game", "Drone", "RC Car", "Puzzle", "Building Set"],
    }
    adjectives = ["Pro", "Lite", "Max", "Plus", "Mini", "Go", "Prime", "Studio"]

    products: List[Dict] = []
    for product_id in range(1, count + 1):
        category = random.choice(list(categories.keys()))
        subcategory = random.choice(categories[category])
        name = f"{subcategory} {random.choice(adjectives)}"
        price = round(random.uniform(9.5, 350.0), 2)
        cost = round(price * random.uniform(0.4, 0.7), 2)

        products.append(
            {
                "product_id": product_id,
                "name": name,
                "category": category,
                "subcategory": subcategory,
                "price": price,
                "cost": cost,
                "is_active": random.choice([True, True, True, False]),
            }
        )

    return products


def generate_orders(
    customers: Sequence[Dict], products: Sequence[Dict], num_orders: int = 240
) -> tuple[List[Dict], List[Dict]]:
    statuses = ["pending", "processing", "shipped", "delivered", "returned", "canceled"]
    status_weights = [5, 15, 25, 45, 5, 5]
    payment_methods = ["card", "paypal", "bank_transfer", "apple_pay", "google_pay"]
    start_date = date.today() - timedelta(days=300)

    orders: List[Dict] = []
    order_items: List[Dict] = []
    order_item_id = 1

    for order_id in range(1, num_orders + 1):
        customer = random.choice(customers)
        order_dt = start_date + timedelta(days=random.randint(0, 300))
        status = random.choices(statuses, weights=status_weights, k=1)[0]
        shipping_cost = random.choice([0.0, 4.99, 7.99, 12.99])

        items_in_order = random.randint(1, 5)
        subtotal = 0.0

        for _ in range(items_in_order):
            product = random.choice(products)
            quantity = random.randint(1, 3)
            discount = random.choice([0, 0, 0.05, 0.1, 0.15, 0.2])
            unit_price = product["price"]
            line_total = round(quantity * unit_price * (1 - discount), 2)
            subtotal = round(subtotal + line_total, 2)

            order_items.append(
                {
                    "order_item_id": order_item_id,
                    "order_id": order_id,
                    "product_id": product["product_id"],
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount": discount,
                    "line_total": line_total,
                }
            )
            order_item_id += 1

        tax = round(subtotal * 0.07, 2)
        total = round(subtotal + shipping_cost + tax, 2)

        orders.append(
            {
                "order_id": order_id,
                "customer_id": customer["customer_id"],
                "order_date": order_dt.isoformat(),
                "status": status,
                "payment_method": random.choice(payment_methods),
                "subtotal": subtotal,
                "shipping_cost": shipping_cost,
                "tax": tax,
                "total": total,
            }
        )

    return orders, order_items


def generate_reviews(
    customers: Sequence[Dict], products: Sequence[Dict], count: int = 150
) -> List[Dict]:
    comments = [
        "Great quality and fast shipping.",
        "Item as described. Would buy again.",
        "Decent value for the price.",
        "Packaging could be better.",
        "Exceeded expectations!",
        "Arrived late but product is good.",
        "Not as durable as I hoped.",
        "Fantastic customer service.",
        "Works as advertised.",
        "Returned for a refund.",
    ]

    reviews: List[Dict] = []
    for review_id in range(1, count + 1):
        customer = random.choice(customers)
        product = random.choice(products)
        rating = random.randint(1, 5)
        review_dt = date.today() - timedelta(days=random.randint(1, 280))

        reviews.append(
            {
                "review_id": review_id,
                "customer_id": customer["customer_id"],
                "product_id": product["product_id"],
                "rating": rating,
                "title": random.choice(
                    ["Excellent", "Good", "Okay", "Poor", "Skip this"]
                ),
                "comment": random.choice(comments),
                "review_date": review_dt.isoformat(),
            }
        )

    return reviews


def main() -> None:
    random.seed(42)

    customers = generate_customers()
    products = generate_products()
    orders, order_items = generate_orders(customers, products)
    reviews = generate_reviews(customers, products)

    write_csv(
        DATA_DIR / "customers.csv",
        [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "city",
            "state",
            "segment",
            "signup_date",
        ],
        customers,
    )
    write_csv(
        DATA_DIR / "products.csv",
        [
            "product_id",
            "name",
            "category",
            "subcategory",
            "price",
            "cost",
            "is_active",
        ],
        products,
    )
    write_csv(
        DATA_DIR / "orders.csv",
        [
            "order_id",
            "customer_id",
            "order_date",
            "status",
            "payment_method",
            "subtotal",
            "shipping_cost",
            "tax",
            "total",
        ],
        orders,
    )
    write_csv(
        DATA_DIR / "order_items.csv",
        [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
            "discount",
            "line_total",
        ],
        order_items,
    )
    write_csv(
        DATA_DIR / "reviews.csv",
        [
            "review_id",
            "customer_id",
            "product_id",
            "rating",
            "title",
            "comment",
            "review_date",
        ],
        reviews,
    )

    print(f"Wrote data to {DATA_DIR.resolve()}")


if __name__ == "__main__":
    main()

