import mariadb
from faker import Faker
import random

# Database connection
db = mariadb.connect(
    host="mariadb",
    user="root",
    password="teste123",
    database="iscte_spot"
)

cursor = db.cursor()

fake = Faker()

# Function to insert data into the 'users' table
def insert_users(num_users=20):
    users = []
    for _ in range(num_users):
        username = fake.user_name()
        password_hash = fake.password()
        email = fake.email()
        created_at = fake.date_time_this_year()
        last_login = fake.date_time_this_year() if random.random() > 0.5 else None
        company_id = random.randint(1, 5) if random.random() > 0.5 else None
        reset_password = random.choice([0, 1])
        commission_percentage = random.randint(5, 20)
        last_logout = fake.date_time_this_year() if last_login else None
        is_active = random.choice([0, 1])
        is_admin = random.choice([0, 1])
        users.append((username, password_hash, email, created_at, last_login, company_id, reset_password, commission_percentage, last_logout, is_active, is_admin))

    cursor.executemany("""
    INSERT INTO users (Username, PasswordHash, Email, CreatedAt, LastLogin, CompanyID, ResetPassword, CommissionPercentage, LastLogout, isActive, IsAdmin)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, users)
    db.commit()

# Function to insert data into the 'companies' table
def insert_companies(num_companies=5):
    companies = []
    for i in range(1, num_companies + 1):
        admin_user_id = i  # Assigning admin user ID as first 5 users
        num_employees = str(random.randint(5, 100))
        revenue = random.randint(10000, 1000000)
        created_at = fake.date_time_this_year()
        company_name = fake.company()
        companies.append((admin_user_id, num_employees, revenue, created_at, company_name))

    cursor.executemany("""
    INSERT INTO companies (AdminUserID, NumberOfEmployees, Revenue, CreatedAt, CompanyName)
    VALUES (%s, %s, %s, %s, %s)
    """, companies)
    db.commit()

# Function to insert data into the 'clients' table
def insert_clients(num_clients=50):
    clients = []
    for _ in range(num_clients):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = fake.phone_number()
        address = fake.address()
        city = fake.city()
        country = fake.country()
        created_at = fake.date_time_this_year()
        company_id = random.randint(1, 5) if random.random() > 0.5 else None
        clients.append((first_name, last_name, email, phone_number, address, city, country, created_at, company_id))

    cursor.executemany("""
    INSERT INTO clients (FirstName, LastName, Email, PhoneNumber, Address, City, Country, CreatedAt, CompanyID)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, clients)
    db.commit()

# Function to insert data into the 'sales' table
def insert_sales(num_sales=500):
    sales = []
    for _ in range(num_sales):
        user_id = random.randint(1, 20)
        client_id = random.randint(1, 50)
        product_name = fake.word()
        quantity = random.randint(1, 10)
        price = round(random.uniform(10, 1000), 2)
        sale_date = fake.date_time_this_year()
        sales.append((user_id, client_id, product_name, quantity, price, sale_date))

    cursor.executemany("""
    INSERT INTO sales (UserID, ClientID, ProductName, Quantity, Price, SaleDate)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, sales)
    db.commit()

# Inserting data
insert_users(20)
insert_companies(5)
insert_clients(50)
insert_sales(500)

# Close connection
cursor.close()
db.close()

print("Data inserted successfully!")
