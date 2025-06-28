import pyodbc
import random

# Setup connection
server = 'ARSLAN-LAPTOP\\SQLEXPRESS'
database = 'CWMS'

conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
cursor = conn.cursor()

# List of Pakistani names
names = [
"Ali", "Mohammad",  "Ahmad Khan", "Bilal Ahmad", "Hamza Sheikh", "Usman Tariq", "Ali Raza",
    "Hassan Nawaz", "Salman Zafar", "Kashif Saeed", "Arslan Malik", "Shahid Qureshi",
    "Muhammad Asif", "Irfan Ahmed", "Farhan Ali", "Rehan Siddiqui", "Adnan Akhtar",
    "Faizan Abbas", "Jawad Hussain", "Noman Khalid", "Tahir Shah", "Waqar Iqbal",
    "Zeeshan Javed", "Rizwan Arif", "Faisal Yousaf", "Qasim Imran", "Kamran Tariq",
    "Adeel Mustafa", "Saad Aftab", "Ammar Zubair", "Anas Sohail", "Haroon Shahid",
    "Wajid Bashir", "Zahid Anwar", "Yasir Mehmood", "Junaid Javed", "Sohail Abbas",
    "Sultan Raza", "Asad Sheikh", "Sajjad Rafiq", "Shahbaz Alam", "Zubair Ahmed",
    "Rafiq Khan", "Azhar Iqbal", "Shabbir Hussain", "Majid Farooq", "Babar Ali",
    "Nadeem Akhtar", "Shakir Ahmad", "Rizwan Shah", "Imran Qadir", "Rafaqat Ali",
    "Hameed Khan", "Atif Iqbal", "Asim Javed", "Nabeel Sheikh", "Naveed Raza",
    "Khalid Mehmood", "Amir Shahzad", "Shan Ahmed", "Samiullah Khan", "Nisar Ahmad",
    "Waseem Khan", "Shiraz Qureshi", "Rameez Akhtar", "Mubeen Khan", "Jibran Ali",
    "Rafay Hussain", "Usama Malik", "Uzair Farooq", "Mudassar Iqbal", "Furqan Shahid",
    "Sarfaraz Ahmed", "Humayun Khan", "Owais Raza", "Noman Rafiq", "Wasif Ali",
    "Sarmad Javed", "Nawaz Tariq", "Rizwan Anwar", "Anwar Hussain", "Ghulam Mustafa",
    "Shahid Mehmood", "Imtiaz Ali", "Danish Javed", "Akbar Khan", "Muzaffar Iqbal",
    "Ijaz Hussain", "Ahsan Raza", "Shafiq Ahmed", "Umer Farooq", "Akram Sheikh",
    "Amjad Hussain", "Salman Sheikh", "Ansar Iqbal", "Irfan Shahid", "Fahad Ahmed",
    "Saqib Ali", "Rauf Khan", "Kamal Ahmed", "Sohail Shah", "Murtaza Sheikh",
    "Jalal Ahmed", "Zahid Bashir", "Rashid Hussain", "Basit Khan", "Fayaz Qureshi",
    "Rauf Iqbal", "Munir Ahmed", "Niaz Khan", "Shafqat Ali", "Arif Raza",
    "Salman Khan", "Azam Qureshi", "Arif Anwar", "Iqbal Khan", "Wasim Iqbal",
    "Asif Hussain", "Kamran Sheikh", "Tariq Mehmood", "Farooq Ahmed", "Javed Khan",
    "Yousuf Ali", "Tanveer Qadir", "Mansoor Ahmed", "Bashir Khan", "Irfan Raza",
    "Kashif Shah", "Azmat Ali", "Arif Khan", "Rehman Tariq", "Riaz Hussain",
    "Naseem Ahmed", "Waheed Raza", "Aftab Iqbal", "Farhan Sheikh", "Jamshed Khan",
    "Arif Sheikh", "Akhtar Hussain", "Salim Ahmed", "Shakil Qureshi", "Kashif Ali",
    "Mubashir Ahmed", "Aqeel Khan", "Umar Sheikh", "Anwar Qadir", "Noman Ali",
    "Tariq Raza", "Usman Ali", "Hammad Ahmed", "Rashid Mehmood", "Farooq Khan",
    "Nasir Iqbal", "Ashraf Sheikh", "Adil Hussain", "Naeem Ahmed", "Faraz Khan",
    "Sohail Qureshi", "Shahid Iqbal", "Riaz Ali", "Bilal Sheikh", "Irfan Khan",
    "Wajid Ali", "Sami Raza", "Ashfaq Ahmed", "Riaz Ahmed", "Naseer Sheikh",
    "Tahir Ali", "Nisar Raza", "Mubashir Hussain", "Shahid Qadir", "Rafay Sheikh",
    "Irfan Qureshi", "Kamran Raza", "Munir Khan", "Aqeel Ali", "Fayaz Sheikh",
    "Akbar Sheikh", "Sami Ahmed", "Faisal Iqbal", "Zeeshan Sheikh", "Nadeem Raza",
    "Aslam Hussain", "Sajid Qureshi", "Adnan Iqbal", "Javed Sheikh", "Adeel Raza",
    "Farhan Khan", "Anwar Ali", "Noman Mehmood", "Kashif Qureshi", "Rafaqat Hussain",
    "Umar Khan", "Imtiaz Sheikh", "Mansoor Raza", "Kashif Mehmood", "Hassan Sheikh",
    "Zahid Khan", "Jibran Sheikh", "Furqan Iqbal", "Rizwan Raza", "Samiullah Sheikh",
    "Waqar Sheikh", "Naveed Qureshi", "Hameed Sheikh", "Jawad Iqbal", "Saad Raza",
    "Zubair Khan", "Waseem Qureshi", "Basit Sheikh", "Saeed Ahmed", "Naveed Iqbal",
    "Khalid Sheikh", "Murtaza Ali", "Uzair Iqbal", "Irfan Ali", "Asim Sheikh",
    "Waqar Iqbal", "Yasir Raza", "Kashif Ahmed", "Salman Iqbal", "Sohail Ali",
    "Nadeem Sheikh", "Jawad Ali", "Yasir Khan", "Usama Qureshi", "Azhar Sheikh",
    "Faisal Sheikh", "Noman Qureshi", "Shahid Ali", "Hassan Ali", "Naveed Sheikh",
    "Farooq Raza", "Munir Iqbal", "Tariq Qureshi", "Waseem Ali", "Sajid Sheikh",
    "Adil Ali", "Azhar Ali", "Tanveer Sheikh", "Rafay Qureshi", "Imran Raza",
    "Ashraf Qureshi", "Farhan Iqbal", "Arslan Raza", "Bilal Qureshi", "Shabbir Ali",
    "Irfan Qadir", "Jawad Sheikh", "Faraz Sheikh", "Rafay Ali", "Nasir Ali",
    "Sajid Iqbal", "Nisar Qureshi", "Usman Raza", "Shakil Sheikh", "Adeel Qureshi",
    "Kashif Raza", "Naseem Raza", "Shan Ali", "Tariq Sheikh", "Kamran Ali",
    "Munir Raza", "Kashif Ali", "Tariq Ali", "Farhan Raza", "Anwar Sheikh",
    "Adeel Ali", "Munir Ali", "Faisal Qadir", "Rafiq Ali", "Ashfaq Ali",
    "Naeem Raza", "Salman Qadir", "Arif Iqbal", "Irfan Sheikh", "Yasir Ali",
    "Tariq Ahmed", "Furqan Ali", "Jibran Ali", "Salman Ahmed", "Ashraf Ali",
    "Asad Ali", "Yasir Sheikh", "Naseem Ali", "Sohail Ahmed", "Rizwan Ahmed",
    "Kamran Iqbal", "Tariq Khan", "Shahid Khan", "Sohail Raza", "Furqan Sheikh",
    "Rizwan Khan", "Junaid Sheikh", "Noman Ali", "Yasir Ahmed", "Mubashir Raza",
    "Imran Ali", "Irfan Hussain", "Shabbir Ahmed", "Ashfaq Qureshi", "Sami Ali",
    "Rafay Ahmed", "Tanveer Ali", "Kashif Iqbal", "Jawad Ahmed", "Farhan Ali",
    "Fayaz Ahmed", "Shan Sheikh", "Adeel Sheikh", "Fahad Ali", "Usman Qadir",
    "Wajid Ahmed", "Irfan Ahmed", "Saeed Ali", "Kamran Raza", "Shahid Raza",
    "Noman Sheikh", "Fayaz Ali", "Sohail Hussain", "Nasir Sheikh", "Mansoor Raza", "Ahmed", "Hassan", "Usman", "Fahad", "Bilal", "Ayesha", "Fatima", "Sana", "Zainab", "Hira", "Farhan",
    "Arslan", "Asma", "Imran", "Saad", "Hammad", "Amina", "Sara", "Yasir", "Irfan", "Rehan", "Fiza", "Nida", "Faisal",
    "Saima", "Aisha", "Waqas", "Omar", "Nabeel", "Samreen", "Zara", "Sadia", "Rabia", "Amna", "Mahnoor", "Zubair", "Tariq",
    "Waqar", "Danish", "Imtiaz", "Iqra", "Sumaira", "Rizwan", "Junaid", "Shazia", "Qasim", "Sobia", "Noman", "Hina", "Shahid",
    "Alisha", "Umar", "Yasmin",   "Ahmad Khan", "Bilal Ahmad", "Hamza Sheikh", "Usman Tariq", "Ali Raza",
    "Hassan Nawaz", "Salman Zafar", "Kashif Saeed", "Arslan Malik", "Shahid Qureshi",
    "Muhammad Asif", "Irfan Ahmed", "Farhan Ali", "Nazia", "Khalid", "Bushra", "Talha", "Adeel", "Esha", "Sohaib", "Rida", "Salman", "Aqsa",
    "Huma", "Aliya", "Hamza", "Hareem", "Khadija", "Faizan", "Hamid", "Sehrish", "Zohaib", "Emaan", "Aiman", "Neha", "Tanveer",
    "Umair", "Rameen", "Aqib", "Areeba", "Tayyaba", "Nadia", "Zahid", "Shoaib", "Mehak", "Soha", "Rameez", "Hafsa", "Bisma",
    "Zoya", "Taimoor", "Hadi", "Rabail", "Fariha","Shehryar", "Hifza", "Wajahat", "Hareer", "Raheel", "Sami", "Tahir",
    "Sanaullah", "Mehek", "Rafay", "Hibba", "Hamna","Uzair", "Atif", "Gulshan", "Mubeen", "Babar", "Laiba", "Yusra",
    "Zaid",  "Saif Ali", "Anees Ahmed", "Khalid Raza", "Salim Raza", "Asif Sheikh",
    "Anwar Raza", "Sami Qureshi", "Javed Ali", "Naeem Iqbal", "Shahid Ahmed",
    "Waseem Ahmed", "Salman Sheikh", "Yasir Qureshi", "Jawad Raza", "Kashif Hussain",
    "Irfan Qadir", "Farhan Qureshi", "Munir Ahmed", "Usama Ali", "Kamran Khan",
    "Tariq Hussain", "Shakil Ahmed", "Adnan Qureshi", "Zeeshan Ahmed", "Salim Ali",
    "Jibran Qureshi", "Sami Raza", "Arslan Qadir", "Shahid Iqbal", "Aqeel Ahmed",
    "Nabeel Ali", "Adeel Raza", "Noman Qadir", "Tariq Ahmed", "Munir Iqbal",
    "Azhar Qadir", "Usama Qadir", "Asim Ali", "Junaid Ahmed", "Kashif Sheikh",
    "Sami Iqbal", "Faisal Raza", "Arif Ahmed", "Rizwan Qadir", "Murtaza Qureshi",
    "Irfan Raza", "Kashif Ahmed", "Tariq Sheikh", "Wajid Raza", "Adeel Qadir",
    "Shabbir Qureshi", "Jawad Iqbal", "Nasir Ahmed", "Zeeshan Qureshi", "Tanveer Qadir",
    "Fayaz Iqbal", "Mansoor Ali", "Noman Raza", "Imran Ahmed", "Munir Qadir",
    "Ashfaq Raza", "Irfan Sheikh", "Rafay Sheikh", "Ashraf Ahmed", "Faisal Ahmed",
    "Usama Sheikh", "Khalid Qureshi", "Tariq Qadir", "Sohail Iqbal", "Anwar Ahmed",
    "Munir Raza", "Yasir Sheikh", "Adil Ahmed", "Kashif Qadir", "Nasir Qureshi","Shan Qureshi", "Farhan Ahmed", "Shakil Qureshi", "Irfan Iqbal", "Jawad Qadir",
    "Rafay Raza", "Furqan Qadir", "Junaid Raza", "Sohail Sheikh", "Aqeel Raza",
    "Faraz Ahmed", "Tariq Raza", "Adnan Ali", "Kamran Qureshi", "Arslan Raza",
    "Munir Sheikh", "Adil Qadir", "Shabbir Raza", "Rafay Ahmed", "Adeel Ahmed",
    "Usama Ahmed", "Noman Ahmed", "Yasir Raza", "Shahid Qadir", "Ashfaq Ahmed",
    "Jibran Ahmed", "Nasir Raza", "Kashif Raza", "Jawad Ahmed", "Kamran Ahmed",
    "Rizwan Raza", "Adil Ali", "Tariq Raza", "Irfan Qureshi", "Sami Ahmed",
    "Farhan Sheikh", "Sohail Ahmed", "Tanveer Ahmed", "Fayaz Ahmed", "Naeem Qureshi",
    "Jibran Raza", "Irfan Ali", "Noman Qureshi", "Ashfaq Qureshi", "Shan Ahmed",
    "Usama Raza", "Munir Qureshi", "Adnan Ahmed", "Kashif Qureshi", "Jawad Ali",
    "Furqan Ahmed", "Arslan Ahmed", "Junaid Qadir", "Rafay Qadir", "Adil Raza",
    "Adeel Ali", "Sami Qadir", "Ashraf Raza", "Tanveer Raza", "Usama Ali",
    "Shabbir Ahmed", "Nasir Ali", "Kashif Ali", "Jawad Qureshi", "Kamran Raza",
    "Rizwan Ahmed", "Aqeel Qureshi", "Farhan Ali", "Sohail Raza", "Irfan Raza","Tariq Ali", "Faisal Qureshi", "Rafay Qureshi", "Adil Qureshi", "Khalid Sheikh",
    "Faraz Raza", "Sami Sheikh", "Jibran Qadir", "Munir Ali", "Yasir Ahmed","Usama Qureshi", "Ashfaq Ali", "Naeem Ahmed", "Tanveer Qureshi", "Jawad Sheikh",
    "Furqan Raza", "Jibran Ali", "Ashraf Ali", "Rizwan Sheikh", "Farhan Qadir","Adnan Qadir", "Noman Ali", "Kashif Qadir", "Shabbir Ali", "Kamran Ali",
    "Irfan Ahmed", "Tariq Qureshi", "Sohail Qureshi", "Yasir Qadir", "Sami Ali","Adeel Qureshi", "Faisal Ali", "Jawad Iqbal", "Arslan Qureshi", "Shakil Ali",
    "Furqan Qureshi", "Kashif Iqbal", "Tanveer Ali", "Naeem Ali", "Farhan Raza","Irfan Qadir", "Munir Ahmed", "Adnan Sheikh", "Kamran Qadir", "Rizwan Ali",
    "Sohail Ali", "Ashfaq Sheikh", "Usama Iqbal", "Khalid Ali", "Faraz Qadir",
    "Adil Ahmed", "Rafay Ali", "Faisal Raza", "Jawad Raza", "Tanveer Sheikh","Sami Ahmed", "Kashif Ali", "Munir Qadir", "Yasir Ali", "Jibran Sheikh","Naeem Qadir", "Rafay Raza", "Sohail Raza", "Furqan Ali", "Farhan Ahmed","Shakil Sheikh", "Rizwan Raza", "Ashraf Qadir", "Adeel Raza", "Tanveer Ahmed",
    "Noman Qadir", "Kashif Raza", "Kamran Qureshi", "Munir Qureshi", "Yasir Qureshi","Rafay Ahmed", "Furqan Sheikh", "Ashfaq Ahmed", "Adnan Raza", "Jibran Ahmed",
    "Noman Sheikh", "Tanveer Qadir", "Adil Sheikh", "Kashif Qureshi", "Munir Raza",
    "Shabbir Sheikh", "Farhan Sheikh", "Jawad Qadir", "Aqeel Ahmed", "Yasir Raza",
    "Naeem Ahmed", "Faisal Qadir", "Sami Sheikh", "Ashfaq Raza", "Sohail Qadir",
    "Rafay Qadir", "Kamran Sheikh", "Munir Sheikh", "Irfan Sheikh", "Kashif Qadir",
    "Adil Qureshi", "Junaid Ahmed", "Tanveer Ali", "Furqan Qadir", "Rizwan Ahmed",
    "Adeel Sheikh", "Farhan Qureshi", "Shan Qadir", "Ashraf Sheikh", "Irfan Qureshi",
    "Khalid Qadir", "Adnan Qureshi", "Jibran Raza", "Yasir Ahmed", "Munir Ali",
    "Noman Ahmed", "Aqeel Qadir", "Faraz Ahmed", "Sami Qureshi", "Tanveer Raza",
    "Shakil Qadir", "Farhan Raza", "Kashif Ahmed", "Jawad Ali", "Furqan Ahmed",
    "Rafay Sheikh", "Naeem Qureshi", "Adnan Ali", "Ashraf Raza", "Irfan Ahmed",
    "Jawad Qureshi", "Sohail Qureshi", "Tanveer Qureshi", "Rafay Ali", "Jibran Sheikh",
    "Adil Ahmed", "Kashif Raza", "Munir Qadir", "Sami Raza", "Ashfaq Sheikh","Lamiah","Muntaha",
    "Yasir Raza", "Furqan Ali", "Farhan Ali", "Kamran Qadir", "Adeel Ali","Shaheen","Ali Wajdan",
    "Kashif Qadir", "Tanveer Qadir", "Jibran Ahmed", "Rafay Raza", "Munir Ahmed","Virat Kohli",
    "Adnan Sheikh", "Arjun Patel", "Ravi Sharma", "Anil Kapoor", "Rohan Singh", "Suresh Reddy", "Pooja Joshi", "Vikas Gupta",
    "Neha Jain", "Deepak Chawla","David Jones", "Sarah Miller", "James Davis", "Amanda Wilson", "Robert Moore", "Jennifer Taylor", "William Anderson", "Elizabeth Thomas", "Joseph Jackson", "Linda White", "Charles Harris", "Patricia Martin", "Thomas Thompson", "Barbara Garcia", "Christopher Martinez", "Susan Robinson", "Daniel Clark", "Margaret Rodriguez", "Matthew Lewis", "Karen Lee", "Anthony Walker", "Nancy Hall", "Mark Allen", "Betty Young", "Donald King", "Dorothy Wright", "Paul Scott", "Sandra Green", "Steven Adams", "Ashley Baker", "Andrew Gonzalez", "Kimberly Nelson", "Joshua Carter", "Deborah Mitchell", "Kevin Perez", "Laura Roberts", "Brian Turner", "Michelle Phillips", "George Campbell", "Stephanie Parker", "Edward Evans", "Rebecca Edwards", "Ronald Collins", "Sharon Stewart", "Timothy Sanchez", "Amy Morris", "Jason Rogers", "Anna Reed", "Jeffrey Cook", "Virginia Morgan", "Ryan Bell", "Kathleen Murphy", "Jacob Bailey", "Melissa Rivera", "Gary Cooper", "Diana Richardson", "Nicholas Cox", "Jane Howard",
    "Jonathan Ward", "Shirley Torres", "Larry Peterson", "Angela Gray", "Scott Ramirez", "Brenda James",  "Kiran Mehta", "Akash Malhotra", "Priya Rao", "Nitin Bhatia", "Sandeep Verma", "Swati Kaul",
    "Rajesh Iyer", "Anjali Khanna", "Mohit Soni", "Rekha Mishra", "Vikram Nair", "Shweta Desai", "Amit Sengupta", "Meera Bhatt",
    "Rakesh Kumar", "Lata Menon", "Amitabh Das", "Kavita Singh", "Sunil Dutta", "Nisha Aggarwal", "Harish Kaur", "Sanjay Pandey",
    "Arpita Chakraborty", "Rahul Tripathi", "Jyoti Srivastava", "Rajiv Sethi", "Alka Gupta", "Rohit Malhotra", "Ishita Chatterjee",
    "Naveen Bhandari", "Mona Joshi", "Gaurav Saxena", "Sheetal Rao", "Kamal Nayar", "Preeti Varma", "Amitabh Jain", "Seema Reddy",
    "Rajiv Kapoor", "Kajal Shah", "Vivek Nanda", "Suman Goel", "Tarun Bhatia", "Ruchi Nair", "Abhishek Bhatt", "Poonam Sen", "Girish Mehta",
    "Divya Reddy", "Yash Sharma", "Sneha Kapoor", "Siddharth Malhotra", "Nidhi Sinha", "Manoj Iyer", "Shruti Mehta", "Vineet Agarwal", "Vidya Rao",
    "Rajiv Reddy", "Simran Kaur", "Vishal Saxena", "Arpita Jain", "Rahul Sharma", "Ankita Gupta", "Sandeep Sen", "Kirti Singh", "Ashish Verma", "Meghna Mehta",
    "Puneet Sinha", "Nisha Reddy", "Rohit Kapoor", "Meera Malhotra", "Ajay Kumar", "Shilpa Rao", "Siddharth Reddy", "Anu Gupta", "Prakash Iyer", "Asha Singh", "Sanjay Mehta",
    "Sarika Desai", "Ravi Menon", "Shalini Gupta", "Kiran Sharma", "Ramesh Kapoor", "Isha Reddy", "Amit Khanna", "Nikita Malhotra", "Arjun Verma", "Rekha Rao",
    "Suresh Bhatia", "Nisha Mehta", "Vijay Reddy", "Pallavi Kapoor", "Anil Gupta", "Sangeeta Sharma", "Rajesh Malhotra", "Priya Sinha", "Vikas Reddy", "Preeti Kapoor", "Sunil Verma", "Sneha Bhatia", "Kishore Reddy", "Meera Kapoor", "Gaurav Mehta", "Divya Verma", "Naveen Kapoor", "Anita Sharma", "Rohit Verma", "Simran Sinha", "Siddharth Kapoor", "Nidhi Reddy", "Manoj Verma", "Shweta Malhotra", "Vineet Kapoor", "Vidya Bhatia", "Rajiv Mehta", "Arpita Sharma", "Rahul Kapoor", "Ankita Verma", "Sandeep Reddy", "Kirti Verma", "Ashish Malhotra", "Meghna Kapoor", "Puneet Verma", "Nisha Kapoor", "Rohit Sharma", "Meera Bhatia", "Ajay Verma", "Shilpa Kapoor", "Siddharth Verma", "Anu Reddy", "Prakash Malhotra", "Asha Kapoor", "Sanjay Verma", "Sarika Kapoor", "Ravi Sharma", "Shalini Verma", "Kiran Malhotra", "Ramesh Verma", "Isha Kapoor", "Amit Verma", "Nikita Kapoor", "Arjun Malhotra", "Rekha Verma", "Suresh Verma", "Nisha Verma", "Vijay Verma", "Pallavi Verma", "Anil Verma", "Sangeeta Verma", "Rajesh Verma", "Priya Verma", "Vikas Verma", "Preeti Verma", "Sunil Verma", "Sneha Verma", "Kishore Verma", "Meera Verma", "Gaurav Verma", "Divya Verma", "Naveen Verma", "Anita Verma""Jawad Raza", "Faisal Ahmed", "Shakil Ahmed", "Irfan Raza","Babar Azam",
    "Tanveer Ahmed", "Furqan Qureshi", "Sami Qadir", "Ashraf Ahmed", "Munir Raza","Qayuum",
    "Noman Qureshi", "Yasir Sheikh", "Rafay Qureshi", "Adil Qadir", "Farhan Sheikh","Haider","Shaheer","Ali Rehman",
    "Jawad Ahmed", "Kashif Sheikh", "Jibran Qadir", "Adeel Qureshi", "Tanveer Raza","Abdul Moiz","Manahil","Ahmad Arslan","Zohaib","Ahmad","Saad Virk","Ali Akbar",
    "Sohail Sheikh", "Kamran Ali", "Faraz Qureshi", "Ashfaq Qadir", "Adnan Ahmed", "Sahar", "Tayyab", "Hashir", "Shireen", "Muneeb",  "Anaya", "Yahya", "Kainat", "Haroon", "Uzma", "Faiza", "Shahzaib", "Aliyan"
]

# List of cities
cities = ["Lahore"]

# List of areas
areas = [
    "DHA", "Gulberg", "Model Town", "Johar Town", "Township", "Cantt", "Garden Town", "Iqbal Town", "Wapda Town",
    "Askari", "Shadman", "Faisal Town", "Shahdara", "Allama Iqbal Town", "Samanabad", "Liaqat Bagh", "Gulshan-e-Iqbal",
    "North Nazimabad", "Malir", "Clifton"
]

random.shuffle(areas)

# Generate random contact info (phone number)
def generate_contact_info():
    return "03" + ''.join(random.choices('0123456789', k=9))

# Generate random address
def generate_address():
    house_no = random.randint(1, 100)
    return f"House No. {house_no}, {random.choice(areas)}, {random.choice(cities)}"

# Get the current maximum customer_id
cursor.execute("SELECT ISNULL(MAX(customer_id), 0) FROM Customers")
start_customer_id = cursor.fetchone()[0] + 1

# Insert records
sql_insert = "{CALL InsertCustomer (?, ?, ?, ?)}"

for i, name in enumerate(names):
    cid = start_customer_id + i
    address = generate_address()
    contact = generate_contact_info()

    try:
        cursor.execute(sql_insert, cid, name, address, contact)
        print(f"✅ Inserted Customer {cid}: {name}")
    except Exception as e:
        print(f"❌ Failed to insert {name} - {e}")

conn.commit()
cursor.close()
conn.close()