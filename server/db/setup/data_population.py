import mariadb
from fakes.fake_users import data as fake_users
from fakes.fake_companies import data as fake_companies
from fakes.fake_clients import data as fake_clients
from fakes.fake_products import data as fake_products
from fakes.fake_sales import data as fake_sales
import random

# Database connection
db = mariadb.connect(
    host="localhost",
    user="root",
    password="teste123",
    port=3306,
    database="iscte_spot"
)

cursor = db.cursor()

# Function to insert data into the 'users' table
def insert_users():
    fake_users_tuples = [
        (
            user["Username"],
            user["PasswordHash"],
            user["Email"],
            user["CreatedAt"],
            user["LastLogin"],
            user["CompanyID"],
            user["ResetPassword"],
            user["CommissionPercentage"],
            user["LastLogout"],
            user["isActive"],
            user["IsAdmin"]
        )
        for user in fake_users
    ]
    cursor.executemany("""
    INSERT INTO users (Username, PasswordHash, Email, CreatedAt, LastLogin, CompanyID, ResetPassword, CommissionPercentage, LastLogout, isActive, IsAdmin)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, fake_users_tuples)
    db.commit()

# Function to insert data into the 'companies' table
def insert_companies():
    fake_companies_tuples = [
        (
            company["CompanyID"],
            company["AdminUserID"],
            company["NumberOfEmployees"],
            company["Revenue"],
            company["CreatedAt"],
            company["CompanyName"]
        )
        for company in fake_companies
    ]
    cursor.executemany("""
    INSERT INTO companies (CompanyID, AdminUserID, NumberOfEmployees, Revenue, CreatedAt, CompanyName)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, fake_companies_tuples)
    db.commit()

# Function to insert data into the 'clients' table
def insert_clients():
    fake_clients_tuples = [
        (
            client["FirstName"],
            client["LastName"],
            client["Email"],
            client["PhoneNumber"],
            client["Address"],
            client["City"],
            client["Country"],
            client["CreatedAt"],
            client["CompanyID"]
        )
        for client in fake_clients
    ]
    cursor.executemany("""
    INSERT INTO clients (FirstName, LastName, Email, PhoneNumber, Address, City, Country, CreatedAt, CompanyID)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, fake_clients_tuples)
    db.commit()

# Function to insert data into the 'products' table
def insert_products():
    fake_products_tuples = [
        (
            product["ProductID"],
            product["CompanyID"],
            product["ProductName"],
            product["FactoryPrice"],
            product["SellingPrice"],
            product["CreatedAt"]
        )
        for product in fake_products
    ]
    cursor.executemany("""
    INSERT INTO products (ProductID, CompanyID, ProductName, FactoryPrice, SellingPrice, CreatedAt)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, fake_products_tuples)
    db.commit()

# Function to insert data into the 'sales' table
def insert_sales():
    fake_sales_tuples = [
        (
            sale["UserID"],
            sale["ClientID"],
            sale["ProductID"],
            sale['Quantity'],
            sale["SaleDate"]
        )
        for sale in fake_sales
    ]
    cursor.executemany("""
    INSERT INTO sales (UserID, ClientID, ProductID, Quantity, SaleDate)
    VALUES (%s, %s, %s, %s, %s)
    """, fake_sales_tuples)
    db.commit()

# Inserting data
insert_users()
insert_companies()
insert_products()
insert_clients()
insert_sales()
# Close connection
cursor.close()
db.close()

print("Data inserted successfully!")
