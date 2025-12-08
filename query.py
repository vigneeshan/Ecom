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
    ORDER BY revenue DESC, orders_count DESC;
    """

    cur.execute(query)
    rows = cur.fetchall()

    # Print column headers
    col_names = [desc[0] for desc in cur.description]
    print("\t".join(col_names))

    # Print rows
    for row in rows:
        print("\t".join(str(x) for x in row))

    conn.close()

if __name__ == "__main__":
    main()
