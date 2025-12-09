import sqlite3

def main():
    conn = sqlite3.connect("ecommerce.db")
    cur = conn.cursor()

    # SQL query as a string
    query = """
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        p.category,
        COUNT(DISTINCT o.order_id) AS orders_count,
        SUM(oi.quantity) AS units_purchased,
        SUM(oi.line_total) AS revenue,
        AVG(r.rating) AS avg_rating,
        COUNT(r.review_id) AS reviews_count
    FROM customers c
    JOIN orders o
      ON o.customer_id = c.customer_id
    JOIN order_items oi
      ON oi.order_id = o.order_id
    JOIN products p
      ON p.product_id = oi.product_id
    LEFT JOIN reviews r
      ON r.product_id = p.product_id
     AND r.customer_id = c.customer_id
    GROUP BY
        c.customer_id,
        c.first_name,
        c.last_name,
        p.category
    ORDER BY revenue DESC, orders_count DESC
    LIMIT 10;
    """

    cur.execute(query)
    rows = cur.fetchall()

    # Column names
    headers = [desc[0] for desc in cur.description]

    # Print header row with alignment
    print("\n=== QUERY RESULT (Top 10 Rows) ===\n")
    print(" | ".join(h.ljust(15) for h in headers))
    print("-" * (len(headers) * 18))

    # Print each row
    for row in rows:
        print(" | ".join(str(col).ljust(15) for col in row))

    conn.close()

if __name__ == "__main__":
    main()
