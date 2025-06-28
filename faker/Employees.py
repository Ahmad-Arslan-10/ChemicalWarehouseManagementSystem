import pyodbc
import random

# SQL Server connection
server = 'ARSLAN-LAPTOP\\SQLEXPRESS'
database = 'CWMS'

conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
cursor = conn.cursor()

# List of employee names
employee_names = [
    "Ahmad Khan", "Bilal Ahmad", "Hamza Sheikh", "Usman Tariq", "Ali Raza",
    "Hassan Nawaz", "Salman Zafar", "Kashif Saeed", "Arslan Malik", "Shahid Qureshi",
]

# Generate 11-digit contact number
def generate_random_contact_info():
    return "03" + ''.join(random.choices('0123456789', k=9))

# Generate employee type by slot availability
def generate_random_employee_type(sales, purchase, finance, supervisors):
    if sales < 2:
        return 'Sales-Manager'
    elif purchase < 2:
        return 'Purchase-Manager'
    elif finance < 2:
        return 'Finance-Manager'
    elif supervisors < 4:
        return 'Supervisor'
    else:
        return 'Supervisor'  # fallback if counts exceeded

# Get starting employee ID
cursor.execute("SELECT ISNULL(MAX(employee_id), 0) FROM Employees")
start_id = cursor.fetchone()[0] + 1

# Initialize role counts
sales_manager_count = 0
purchase_manager_count = 0
finance_manager_count = 0
supervisor_count = 0

# SQL procedure call
sql = "{CALL InsertEmployee (?, ?, ?, ?)}"

for i, name in enumerate(employee_names):
    eid = start_id + i
    contact = generate_random_contact_info()
    emp_type = generate_random_employee_type(
        sales_manager_count,
        purchase_manager_count,
        finance_manager_count,
        supervisor_count
    )

    if emp_type == 'Sales-Manager': sales_manager_count += 1
    elif emp_type == 'Purchase-Manager': purchase_manager_count += 1
    elif emp_type == 'Finance-Manager': finance_manager_count += 1
    elif emp_type == 'Supervisor': supervisor_count += 1

    try:
        cursor.execute(sql, eid, name, contact, emp_type)
        print(f"✅ Inserted Employee {eid}: {name} as {emp_type}")
    except Exception as e:
        print(f"❌ Failed to insert {name} - {e}")

conn.commit()
cursor.close()
conn.close()