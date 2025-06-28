import pyodbc
import random
from datetime import datetime, timedelta

# DB Connection
server = 'ARSLAN-LAPTOP\\SQLEXPRESS'
database = 'CWMS'

conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Get purchase IDs to pick from (limit to recent 100)
cursor.execute("SELECT TOP 100 purchase_id, date, quantity FROM Purchases ORDER BY NEWID()")
purchases = cursor.fetchall()

# Get current max return_id
cursor.execute("SELECT ISNULL(MAX(return_id), 0) FROM Purchase_Returns")
return_id = cursor.fetchone()[0] + 1

# Stored procedure
sql_insert = "{CALL InsertPurchaseReturn (?, ?, ?, ?)}"

for row in purchases:
    purchase_id = row[0]
    purchase_date = row[1]
    quantity_purchased = row[2]

    return_date = purchase_date + timedelta(days=random.randint(3, 5))
    return_quantity = random.randint(1, quantity_purchased)

    try:
        cursor.execute(sql_insert, return_id, purchase_id, return_date, return_quantity)
        print(f"✅ Return {return_id}: Purchase {purchase_id} | Qty: {return_quantity} on {return_date.strftime('%Y-%m-%d')}")
        return_id += 1
    except Exception as e:
        print(f"❌ Failed for Purchase {purchase_id}: {e}")

conn.commit()
cursor.close()
conn.close()

print("✅ All purchase return records inserted.")