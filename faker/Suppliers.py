import pyodbc
import random

# SQL Server connection
server = 'ARSLAN-LAPTOP\\SQLEXPRESS'
database = 'CWMS'

conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Supplier names
supplier_names = [
    "ChemicalCompany",
    "Khawaja Aweosols Pvt. Limited.",
    "IndustryNet",
    "Kolvoi Shop"
]

random.shuffle(supplier_names)

# Contact generator
def generate_contact_info():
    return "03" + ''.join(random.choices('0123456789', k=9))

# Get starting supplier ID
cursor.execute("SELECT ISNULL(MAX(supplier_id), 0) FROM Suppliers")
start_supplier_id = cursor.fetchone()[0] + 1

# Stored procedure
sql_insert = "{CALL InsertSupplier (?, ?, ?)}"

# Insert suppliers
for i, name in enumerate(supplier_names):
    sid = start_supplier_id + i
    contact = generate_contact_info()

    try:
        cursor.execute(sql_insert, sid, name, contact)
        print(f"✅ Supplier {sid}: {name} ({contact})")
    except Exception as e:
        print(f"❌ Failed to insert {name}: {e}")

conn.commit()
cursor.close()
conn.close()

print("✅ All suppliers inserted successfully.")