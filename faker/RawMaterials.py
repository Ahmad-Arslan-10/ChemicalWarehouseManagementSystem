import pyodbc

# SQL Server connection
server = 'ARSLAN-LAPTOP\\SQLEXPRESS'
database = 'CWMS'

conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Raw materials with assigned supplier_id
raw_materials = [
    (1, "Chemical A", 1),
    (2, "Chemical B", 2),
    (3, "Chemical C", 3),
    (4, "Chemical D", 4),
    (5, "Chemical E", 3),
    (6, "Chemical F", 4),
    (7, "Chemical G", 1),
    (8, "Chemical H", 2),
    (9, "Chemical I", 4),
    (10, "Chemical J", 1),
    (11, "Chemical D", 4),
    (12, "Chemical D", 3)
]

# Stored procedure
sql_insert = "{CALL Insert_Raw_Material (?, ?, ?)}"

# Insert materials
for material_id, name, supplier_id in raw_materials:
    try:
        cursor.execute(sql_insert, material_id, name, supplier_id)
        print(f"✅ Inserted: {material_id} - {name} (Supplier {supplier_id})")
    except Exception as e:
        print(f"❌ Failed to insert {material_id} - {name}: {e}")

conn.commit()
cursor.close()
conn.close()

print("✅ All raw materials inserted successfully.")