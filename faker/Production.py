import pyodbc
import random
from datetime import datetime

# SQL Server connection
server = 'ARSLAN-LAPTOP\\SQLEXPRESS'
database = 'CWMS'

conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Product IDs that already exist
product_ids = list(range(1, 13))  # 1 to 12

# Employee IDs (assumed range)
employee_range = range(7, 11)

# Material IDs (assumed range)
material_range = range(1, 13)

# Get latest production_id to avoid conflict
cursor.execute("SELECT ISNULL(MAX(production_id), 0) FROM Production")
production_id = cursor.fetchone()[0] + 1

# Insert production data for each month between 2022–2023
for year in range(2022, 2024):
    for month in range(1, 13):
        production_date = datetime(year, month, 10).strftime('%Y-%m-%d')

        for product_id in product_ids:
            quantity = random.randint(100, 200)
            employee_id = random.choice(employee_range)
            material_id = random.choice(material_range)

            try:
                # FIX 3: Correct parameter passing
                cursor.execute("EXEC InsertProduction ?, ?, ?, ?, ?, ?",
                             production_id, production_date, product_id, quantity, employee_id, material_id)
                
                print(f"✅ {production_date} | ProdID: {production_id} | Product: {product_id} | Qty: {quantity}")
                production_id += 1
                
                # FIX 4: Commit after each insert
                conn.commit()
                
            except Exception as e:
                print(f"❌ Error on Product {product_id} ({production_date}): {e}")
                conn.rollback()

cursor.close()
conn.close()
print("✅ All production records processing completed.")