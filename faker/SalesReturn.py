import pyodbc
import random
from datetime import timedelta

# DB connection
server = 'ARSLAN-LAPTOP\\SQLEXPRESS'
database = 'CWMS'

conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Get 400 random sales with quantity > 0
cursor.execute("SELECT TOP 400 sales_id, date, quantity FROM Sales WHERE quantity > 0 ORDER BY NEWID()")
sales_data = cursor.fetchall()

# Get current max return_id
cursor.execute("SELECT ISNULL(MAX(return_id), 0) FROM Sales_Returns")
return_id = cursor.fetchone()[0] + 1

# Stored procedure
sql_insert_sales_return = "{CALL InsertSalesReturn (?, ?, ?, ?)}"

# Insert returns
for row in sales_data:
    sales_id = row[0]
    sale_date = row[1]  # Already a datetime object
    sale_quantity = row[2]

    return_date = sale_date + timedelta(days=random.randint(3, 5))
    quantity_returned = random.randint(1, sale_quantity)

    try:
        cursor.execute(sql_insert_sales_return, return_id, sales_id, return_date, quantity_returned)
        print(f"✅ Return {return_id}: Sale {sales_id} | Qty: {quantity_returned} on {return_date.date()}")
        return_id += 1
    except Exception as e:
        print(f"❌ Failed to insert return for Sale {sales_id}: {e}")

conn.commit()
cursor.close()
conn.close()

print("✅ All sales return records inserted successfully.")
