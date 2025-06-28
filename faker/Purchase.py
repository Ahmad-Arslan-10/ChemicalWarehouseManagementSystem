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

supplier_ids = [1, 2, 3, 4]
material_ids = [1, 2, 3, 4]
employee_ids = [3, 4]

cursor.execute("SELECT ISNULL(MAX(purchase_id), 0) FROM Purchases")
purchase_id = cursor.fetchone()[0] + 1

for year in range(2022, 2024):
    for month in range(1, 13):
        purchase_date = datetime(year, month, 1).strftime('%Y-%m-%d')

        for material_id in material_ids:
            supplier_id = random.choice(supplier_ids)
            employee_id = random.choice(employee_ids)
            price_per_unit = round(random.uniform(250.00, 500.00), 2)
            quantity = random.randint(100, 150)
            total_price = round(price_per_unit * quantity, 2)

            try:
                cursor.execute("EXEC InsertPurchase ?, ?, ?, ?, ?, ?, ?, ?", 
                             purchase_id, purchase_date, quantity, price_per_unit,
                             total_price, employee_id, supplier_id, material_id)
                
                print(f"✅ Purchase {purchase_id}: {quantity}x Material {material_id} on {purchase_date}")
                purchase_id += 1
                
                conn.commit()
                
            except Exception as e:
                print(f"❌ Failed to insert purchase {purchase_id} on {purchase_date}: {e}")
                conn.rollback()

cursor.close()
conn.close()
print("✅ All purchase data processing completed.")