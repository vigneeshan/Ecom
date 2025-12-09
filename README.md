PROMPTS USED:

PROMPT 1:
Write Python code to generate synthetic e-commerce data and save it as 5 CSV files:
customers.csv, products.csv, orders.csv, order_items.csv, and reviews.csv.
Generate at least 50 rows per file and make sure all foreign keys (customer_id, order_id, product_id) match correctly.
Use only Python standard libraries and save the CSVs in the data/ folder.

PROMPT 2:
Write Python code that loads the CSV files (customers.csv, products.csv, orders.csv, order_items.csv, and reviews.csv) into a SQLite database called ecommerce.db.
Create tables with the correct schema, enable foreign keys, drop existing data if needed, and insert all rows from the CSVs.
Use only sqlite and csv modules.

PROMPT 3:
Write a Python script that connects to ecommerce.db and runs SQL queries that join multiple tables: customers, orders, order_items, products, and reviews.
The script should output analytics such as total amount spent per customer, top products by revenue, and order-level summaries.
