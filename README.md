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

▶️ How to Run This Project
1. Generate the CSV data
python generate_ecommerce_data.py

2. Ingest into SQLite
python ingest_to_sqlite.py

3. Run analysis queries
python query.py

🌐 Version Control

All code and generated project files are committed to GitHub using:

git add .
git commit -m "AI-SDLC e-commerce project completed"
git push origin main
