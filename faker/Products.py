import pyodbc

# SQL Server connection
server = 'ARSLAN-LAPTOP\\SQLEXPRESS'
database = 'CWMS'

conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Products: (product_id, product_name, price)
products = [
    (1, "Drain Opener", 500.00),
    (2, "Clenx Glass Cleaner", 299.00),
    (3, "Power Blue Neel", 400.00),
    (4, "Insect Killer Powder", 350.00),
    (5, "Dishwash Liquid", 550.00),
    (6, "Bed Bug Cleaner", 100.00),
    (7, "Sweep Toilet Cleaner", 1000.00),
    (8, "Cockroach Killer Gel", 1000.00),
    (9, "Active Liquid Bleach", 950.00),
    (10, "Maxon", 100.00),
    (11, "Phenyl Floor Cleaner", 200.00),
    (12, "Mosquito Repellent", 700.00)
]

# Stored procedure
sql_insert_product = "{CALL InsertProduct (?, ?, ?)}"

# Insert all products
for pid, name, price in products:
    try:
        cursor.execute(sql_insert_product, pid, name, price)
        print(f"✅ Inserted Product {pid}: {name} @ Rs. {price}")
    except Exception as e:
        print(f"❌ Failed to insert {name}: {e}")

conn.commit()
cursor.close()
conn.close()

print("✅ All products inserted successfully.")