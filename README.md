Main Prompts Used in Cursor IDE

The following prompts were used to build the project, as required by the assignment.

Prompt 1 — Project Setup
You are an expert Python and SQL developer. 
Create a Python project structure that includes:
- a data/ folder
- generate_ecommerce_data.py
- load_into_sqlite.py
- query.py
Add README.md and .gitignore.

Prompt 2 — Generate Synthetic E-Commerce Data
Generate around 5 synthetic e-commerce CSV files using only Python standard libraries.
Create customers.csv, products.csv, orders.csv, order_items.csv, and reviews.csv.
Ensure realistic columns, valid relationships, and save files into data/.

Prompt 3 — SQLite Ingestion Script
Write a script load_into_sqlite.py that:
- creates ecommerce.db
- creates tables: customers, products, orders, order_items, reviews
- loads all CSV files from data/
- enables foreign keys
- commits and prints counts.
Use only sqlite3 and csv.

Prompt 4 — SQL JOIN Query Script
Create a Python script query.py that connects to ecommerce.db and runs SQL queries:
1. Total spent per customer.
2. Top products by sales revenue.
3. Order summary with customer details.
Use JOINs and print readable results.

MAIN SHORTER PROMPTS ARE:
You are an expert Python and SQL developer. I am doing an assignment with these requirements:

Generate around 5 synthetic e-commerce CSV files.

Ingest those CSVs into a SQLite database.

Write an SQL query that joins multiple tables and prints some result.

All code and generated project files are committed to GitHub using:

git add .
git commit -m "AI-SDLC e-commerce project completed"
git push origin main
