import mariadb

# Establish a connection to the MariaDB database
db = mariadb.connect(
    host="mariadb", # Altered
    user="root",
    password="teste123",
    database="iscte_spot"
)

cursor = db.cursor()

def drop_all_tables():
    # Query to get all table names
    tables = ['Sales', 'Clients', 'Products', 'Companies', 'SupportTickets', 'Users']
    # Drop each table
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
        print(f"Table {table} dropped.")

    db.commit()

# Run the drop tables function
drop_all_tables()

# Close the connection
cursor.close()
db.close()
