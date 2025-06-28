import pyodbc
import random

# SQL Server connection
server = 'ARSLAN-LAPTOP\\SQLEXPRESS'
database = 'CWMS'

conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Product IDs to link with inventory
product_ids = list(range(1, 13))  # Products 1 to 12

# Get current max inventory ID
cursor.execute("SELECT ISNULL(MAX(inventory_id), 0) FROM Inventory")
start_inventory_id = cursor.fetchone()[0] + 1

# Stored procedure
sql_insert_inventory = "{CALL InsertInventory (?, ?, ?)}"

# Insert inventory records
for i, product_id in enumerate(product_ids):
    inventory_id = start_inventory_id + i
    quantity = random.randint(500, 1000)

    try:
        cursor.execute(sql_insert_inventory, inventory_id, product_id, quantity)
        print(f"✅ Inventory ID {inventory_id}: Product {product_id} - Qty {quantity}")
    except Exception as e:
        print(f"❌ Failed for Product {product_id}: {e}")

# Finalize
conn.commit()
cursor.close()
conn.close()