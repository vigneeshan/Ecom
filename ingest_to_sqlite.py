"""
Load generated e-commerce CSVs into a SQLite database.

Usage:
    python ingest_to_sqlite.py [--data-dir data] [--db ecommerce.db]
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path
from typing import Iterable, Mapping, Sequence


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON;")

    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            city TEXT,
            state TEXT,
            segment TEXT,
            signup_date TEXT
        );

        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            subcategory TEXT,
            price REAL,
            cost REAL,
            is_active INTEGER
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT,
            status TEXT,
            payment_method TEXT,
            subtotal REAL,
            shipping_cost REAL,
            tax REAL,
            total REAL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER,
            unit_price REAL,
            discount REAL,
            line_total REAL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );

        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            rating INTEGER,
            title TEXT,
            comment TEXT,
            review_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """
    )


def parse_bool(value: str | int | None) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return 1 if value else 0
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y"}:
        return 1
    if text in {"0", "false", "f", "no", "n"}:
        return 0
    return None


def load_csv(
    conn: sqlite3.Connection,
    table: str,
    path: Path,
    columns: Sequence[str],
    converters: Mapping[str, callable] | None = None,
) -> None:
    converters = converters or {}
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            parsed = []
            for col in columns:
                raw = row[col]
                if col in converters:
                    parsed.append(converters[col](raw))
                else:
                    parsed.append(raw)
            rows.append(tuple(parsed))

    placeholders = ",".join(["?"] * len(columns))
    sql = f"INSERT OR REPLACE INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
    conn.executemany(sql, rows)


def ingest(data_dir: Path, db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    try:
        ensure_tables(conn)

        load_csv(
            conn,
            "customers",
            data_dir / "customers.csv",
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
            converters={"customer_id": int},
        )
        load_csv(
            conn,
            "products",
            data_dir / "products.csv",
            ["product_id", "name", "category", "subcategory", "price", "cost", "is_active"],
            converters={
                "product_id": int,
                "price": float,
                "cost": float,
                "is_active": parse_bool,
            },
        )
        load_csv(
            conn,
            "orders",
            data_dir / "orders.csv",
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
            converters={
                "order_id": int,
                "customer_id": int,
                "subtotal": float,
                "shipping_cost": float,
                "tax": float,
                "total": float,
            },
        )
        load_csv(
            conn,
            "order_items",
            data_dir / "order_items.csv",
            [
                "order_item_id",
                "order_id",
                "product_id",
                "quantity",
                "unit_price",
                "discount",
                "line_total",
            ],
            converters={
                "order_item_id": int,
                "order_id": int,
                "product_id": int,
                "quantity": int,
                "unit_price": float,
                "discount": float,
                "line_total": float,
            },
        )
        load_csv(
            conn,
            "reviews",
            data_dir / "reviews.csv",
            [
                "review_id",
                "customer_id",
                "product_id",
                "rating",
                "title",
                "comment",
                "review_date",
            ],
            converters={
                "review_id": int,
                "customer_id": int,
                "product_id": int,
                "rating": int,
            },
        )

        conn.commit()
    finally:
        conn.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest CSVs into SQLite.")
    parser.add_argument("--data-dir", type=Path, default=Path("data"), help="Directory containing CSV files.")
    parser.add_argument("--db", type=Path, default=Path("ecommerce.db"), help="SQLite database path to create/write.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ingest(args.data_dir, args.db)
    print(f"Loaded CSVs from {args.data_dir} into {args.db}")


if __name__ == "__main__":
    main()

