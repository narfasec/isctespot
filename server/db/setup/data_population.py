import mariadb
from fakes.fake_users import data as fake_users
from fakes.fake_companies import data as fake_companies
from fakes.fake_clients import data as fake_clients
from fakes.fake_products import data as fake_products
from fakes.fake_sales import data as fake_sales
import random

# Database connection
db = mariadb.connect(
    host="mariadb",
    user="root",
    password="teste123",
    database="iscte_spot"
)

cursor = db.cursor()

# Function to insert data into the 'users' table
def insert_users():
    cursor.executemany("""
    INSERT INTO users (Username, PasswordHash, Email, CreatedAt, LastLogin, CompanyID, ResetPassword, CommissionPercentage, LastLogout, isActive, IsAdmin)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, fake_users)
    db.commit()

# Function to insert data into the 'companies' table
def insert_companies():
    cursor.executemany("""
    INSERT INTO companies (AdminUserID, NumberOfEmployees, Revenue, CreatedAt, CompanyName)
    VALUES (%s, %s, %s, %s, %s)
    """, fake_companies)
    db.commit()

# Function to insert data into the 'clients' table
def insert_clients():
    cursor.executemany("""
    INSERT INTO clients (FirstName, LastName, Email, PhoneNumber, Address, City, Country, CreatedAt, CompanyID)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, fake_clients)
    db.commit()

# Function to insert data into the 'products' table
def insert_products():
    cursor.executemany("""
    INSERT INTO sales (UserID, ClientID, ProductName, Quantity, Price, SaleDate)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, fake_sales)
    db.commit()
# Function to insert data into the 'sales' table
def insert_sales():
    cursor.executemany("""
    INSERT INTO sales (UserID, ClientID, ProductName, Quantity, Price, SaleDate)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, fake_sales)
    db.commit()

# Inserting data
insert_users()
insert_companies()
insert_clients()
insert_sales()
insert_products()
# Close connection
cursor.close()
db.close()

print("Data inserted successfully!")
