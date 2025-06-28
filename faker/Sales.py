import random
import pyodbc
from datetime import datetime
import calendar

# SQL Server connection
server = 'ARSLAN-LAPTOP\\SQLEXPRESS'
database = 'CWMS'

conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
cursor = conn.cursor()
print("Connected to:", conn.getinfo(pyodbc.SQL_SERVER_NAME), conn.getinfo(pyodbc.SQL_DATABASE_NAME))

# Products, customers, employees
product_ids = list(range(1, 13))
customer_ids = list(range(1, 1030))  # assuming 1029 customers
employee_ids = [1, 2]

# Get starting sale_id
cursor.execute("SELECT ISNULL(MAX(sales_id), 0) FROM Sales")
sale_id = cursor.fetchone()[0] + 1

# Prepare stored procedure call
sql_insert_sale = "{CALL InsertSale (?, ?, ?, ?, ?, ?)}"

years = [2022, 2023]

for year in years:
    for month in range(1, 13):
        days_in_month = calendar.monthrange(year, month)[1]

        print(f"Inserting sales for {datetime(year, month, 1).strftime('%B %Y')}")

        for day in range(1, days_in_month + 1):
            current_date = datetime(year, month, day)

            for _ in range(random.randint(5, 15)):  # multiple sales per day
                product_id = random.choice(product_ids)
                customer_id = random.choice(customer_ids)
                employee_id = random.choice(employee_ids)

                # Check inventory for chosen product
                cursor.execute("SELECT quantity_available FROM Inventory WHERE product_id = ?", (product_id,))
                row = cursor.fetchone()

                if row and row[0] > 0:
                    available_quantity = row[0]
                    quantity_sold = random.randint(1, min(20, available_quantity))

                    try:
                        cursor.execute(sql_insert_sale, (
                            sale_id, current_date, quantity_sold,
                            customer_id, product_id, employee_id
                        ))
                        sale_id += 1
                    except Exception as e:
                        print(f"❌ Failed on sale {sale_id} (Product {product_id}): {e}")

# Final commit and cleanup
conn.commit()
cursor.close()
conn.close()
print("Sales insertion completed.")