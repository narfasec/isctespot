import mariadb

connection = mariadb.connect(
	host="localhost",
	user="root",
	password="teste123",
	port=3306
)

cursor = connection.cursor()
try:

    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS iscte_spot;")
    print("Database 'iscte_spot' created or already exists.")

    # Switch to the newly created database
    cursor.execute("USE iscte_spot;")

    # SQL statements to create the tables
    create_tables_sql = """
    CREATE TABLE IF NOT EXISTS users (
        UserID INT(11) NOT NULL AUTO_INCREMENT,
        Username VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
        PasswordHash VARCHAR(255) NOT NULL COLLATE 'latin1_swedish_ci',
        Email VARCHAR(100) NOT NULL COLLATE 'latin1_swedish_ci',
        CreatedAt TIMESTAMP NULL DEFAULT current_timestamp(),
        LastLogin TIMESTAMP NULL DEFAULT NULL,
        CompanyID INT(11) NULL DEFAULT NULL,
        ResetPassword TINYINT(1) NULL DEFAULT '0',
        CommissionPercentage INT(11) NULL DEFAULT '5',
        LastLogout TIMESTAMP NULL DEFAULT NULL,
        isActive TINYINT(1) NULL DEFAULT '0',
        IsAdmin TINYINT(1) NULL DEFAULT '0',
        PRIMARY KEY (UserID) USING BTREE,
        UNIQUE INDEX Username (Username) USING BTREE,
        UNIQUE INDEX Email (Email) USING BTREE,
        INDEX CompanyID (CompanyID) USING BTREE
    )
    COLLATE='latin1_swedish_ci'
    ENGINE=InnoDB
    AUTO_INCREMENT=1;

    CREATE TABLE IF NOT EXISTS companies (
        CompanyID INT(11) NOT NULL AUTO_INCREMENT,
        AdminUserID INT(11) NOT NULL,
        NumberOfEmployees VARCHAR(10) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
        Revenue INT(11) NULL DEFAULT NULL,
        CreatedAt TIMESTAMP NULL DEFAULT current_timestamp(),
        CompanyName VARCHAR(255) NOT NULL COLLATE 'latin1_swedish_ci',
        PRIMARY KEY (CompanyID) USING BTREE,
        INDEX AdminUserID (AdminUserID) USING BTREE,
        CONSTRAINT companies_ibfk_1 FOREIGN KEY (AdminUserID) REFERENCES users (UserID) ON UPDATE RESTRICT ON DELETE RESTRICT
    )
    COLLATE='latin1_swedish_ci'
    ENGINE=InnoDB
    AUTO_INCREMENT=1;

    CREATE TABLE IF NOT EXISTS clients (
        ClientID INT(11) NOT NULL AUTO_INCREMENT,
        FirstName VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
        LastName VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
        Email VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
        PhoneNumber VARCHAR(15) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
        Address VARCHAR(255) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
        City VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
        Country VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
        CreatedAt TIMESTAMP NULL DEFAULT current_timestamp(),
        CompanyID INT(11) NULL DEFAULT NULL,
        PRIMARY KEY (ClientID) USING BTREE,
        UNIQUE INDEX Email (Email) USING BTREE
    )
    COLLATE='latin1_swedish_ci'
    ENGINE=InnoDB
    AUTO_INCREMENT=1;

    CREATE TABLE IF NOT EXISTS sales (
        SaleID INT(11) NOT NULL AUTO_INCREMENT,
        UserID INT(11) NULL,
        ClientID INT(11) NOT NULL,
        ProductName VARCHAR(100) NOT NULL COLLATE 'latin1_swedish_ci',
        Quantity INT(11) NOT NULL,
        Price DECIMAL(10,2) NOT NULL,
        SaleDate TIMESTAMP NULL DEFAULT current_timestamp(),
        PRIMARY KEY (SaleID) USING BTREE,
        INDEX UserID (UserID) USING BTREE,
        INDEX ClientID (ClientID) USING BTREE,
        CONSTRAINT sales_ibfk_1 FOREIGN KEY (UserID) REFERENCES users (UserID) ON UPDATE RESTRICT ON DELETE SET NULL,
        CONSTRAINT sales_ibfk_2 FOREIGN KEY (ClientID) REFERENCES clients (ClientID) ON UPDATE RESTRICT ON DELETE RESTRICT
    )
    COLLATE='latin1_swedish_ci'
    ENGINE=InnoDB
    AUTO_INCREMENT=1;
    
    CREATE TABLE IF NOT EXISTS Products (
		ProductID INT(11) NOT NULL AUTO_INCREMENT,
		CompanyID INT(11) NOT NULL,
		ProductName VARCHAR(255) NOT NULL COLLATE 'latin1_swedish_ci',
		CreatedAt TIMESTAMP NULL DEFAULT current_timestamp(),
		PRIMARY KEY (ProductID) USING BTREE,
		INDEX CompanyID (CompanyID) USING BTREE,
		CONSTRAINT products_ibfk_1 FOREIGN KEY (CompanyID) REFERENCES companies (CompanyID) ON UPDATE RESTRICT ON DELETE RESTRICT
	)
	COLLATE='latin1_swedish_ci'
	ENGINE=InnoDB
 	AUTO_INCREMENT=1;
 

    """

    # Executing the SQL statements
    for statement in create_tables_sql.split(';'):
        if statement.strip():
            cursor.execute(statement)

    connection.commit()
    print("Tables created successfully.")

except mariadb.Error as err:
    print(f"Error: {err}")
finally:
    if connection is not None:
        cursor.close()
        connection.close()
