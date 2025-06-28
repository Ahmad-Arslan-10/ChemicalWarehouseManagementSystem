from flask import Flask, render_template
import pyodbc

app = Flask(__name__)

# Database connection
conn_str = (
    "DRIVER={SQL Server};"
    "SERVER=ARSLAN-LAPTOP\\SQLEXPRESS;"
    "DATABASE=CWMS;"
    "Trusted_Connection=yes;"
)

@app.route("/")
def index():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Customers")
    customer_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Sales")
    sales_count = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total_price) FROM Purchases")
    total_purchase = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM Products")
    product_count = cursor.fetchone()[0]

    conn.close()

    return render_template("index.html",
        customer_count=customer_count,
        sales_count=sales_count,
        total_purchase=total_purchase,
        product_count=product_count
    )

if __name__ == "__main__":
    app.run(debug=True)