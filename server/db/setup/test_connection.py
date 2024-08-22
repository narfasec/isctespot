import os
import mariadb
import time

db_config = {
    'host': 'mariadb',  # Use the service name 'mariadb'
    'user': 'root',
    'password': 'teste123',
}

max_retries = 5
retry_interval = 5  # seconds

# Establish the connection with retries
for attempt in range(max_retries):
    try:
        connection = mariadb.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = connection.cursor()

        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS iscte_spot;")
        print("Database 'iscte_spot' created or already exists.")
        
        # Use the database
        cursor.execute("USE iscte_spot;")

        # Your table creation code goes here
        break

    except mariadb.Error as err:
        print(f"Attempt {attempt + 1} failed: {err}")
        if attempt < max_retries - 1:
            print(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
        else:
            print("All attempts failed. Exiting.")
            raise
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")
