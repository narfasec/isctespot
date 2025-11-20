import mariadb

connection = mariadb.connect(
    host="mariadb", #Altered
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
    CREATE TABLE IF NOT EXISTS Users (
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
        IsAgent TINYINT(1) NULL DEFAULT '0',
        PRIMARY KEY (UserID) USING BTREE,
        UNIQUE INDEX Username (Username) USING BTREE,
        UNIQUE INDEX Email (Email) USING BTREE,
        INDEX CompanyID (CompanyID) USING BTREE
    )
    COLLATE='latin1_swedish_ci'
    ENGINE=InnoDB
    AUTO_INCREMENT=1;

    CREATE TABLE IF NOT EXISTS Companies (
        CompanyID INT(11) NOT NULL AUTO_INCREMENT,
        AdminUserID INT(11) NOT NULL,
        NumberOfEmployees INT(11) NULL DEFAULT NULL,
        Revenue INT(11) NULL DEFAULT NULL,
        CreatedAt TIMESTAMP NULL DEFAULT current_timestamp(),
        CompanyName VARCHAR(255) NOT NULL COLLATE 'latin1_swedish_ci',
        PRIMARY KEY (CompanyID) USING BTREE,
        INDEX AdminUserID (AdminUserID) USING BTREE,
        CONSTRAINT companies_ibfk_1 FOREIGN KEY (AdminUserID) REFERENCES Users (UserID) ON UPDATE RESTRICT ON DELETE RESTRICT
    )
    COLLATE='latin1_swedish_ci'
    ENGINE=InnoDB
    AUTO_INCREMENT=1;

    CREATE TABLE IF NOT EXISTS Clients (
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

    CREATE TABLE IF NOT EXISTS Products (
        ProductID INT(11) NOT NULL AUTO_INCREMENT,
        CompanyID INT(11) NOT NULL,
        ProductName VARCHAR(255) NOT NULL COLLATE 'latin1_swedish_ci',
        Category VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',  -- New field for product category
        FactoryPrice DECIMAL(10,2) NOT NULL,
        SellingPrice DECIMAL(10,2) NOT NULL,
        CreatedAt TIMESTAMP NULL DEFAULT current_timestamp(),
        PRIMARY KEY (ProductID) USING BTREE,
        INDEX CompanyID (CompanyID) USING BTREE,
        CONSTRAINT products_ibfk_1 FOREIGN KEY (CompanyID) REFERENCES Companies (CompanyID) ON UPDATE RESTRICT ON DELETE RESTRICT
    )
    COLLATE='latin1_swedish_ci'
    ENGINE=InnoDB
    AUTO_INCREMENT=1;
    
    CREATE TABLE IF NOT EXISTS Sales (
        SaleID INT(11) NOT NULL AUTO_INCREMENT,
        UserID INT(11) NULL,
        ClientID INT(11) NULL,
        ProductID INT(11) NULL,
        Quantity INT(11) NOT NULL,
        SaleDate TIMESTAMP NULL DEFAULT current_timestamp(),
        PRIMARY KEY (SaleID) USING BTREE,
        INDEX UserID (UserID) USING BTREE,
        INDEX ClientID (ClientID) USING BTREE,
        INDEX ProductID (ProductID) USING BTREE,
        CONSTRAINT sales_ibfk_1 FOREIGN KEY (UserID) REFERENCES Users (UserID) ON UPDATE RESTRICT ON DELETE SET NULL,
        CONSTRAINT sales_ibfk_2 FOREIGN KEY (ClientID) REFERENCES Clients (ClientID) ON UPDATE RESTRICT ON DELETE SET NULL,
        CONSTRAINT sales_ibfk_3 FOREIGN KEY (ProductID) REFERENCES Products (ProductID) ON UPDATE RESTRICT ON DELETE SET NULL
    )
    COLLATE='latin1_swedish_ci'
    ENGINE=InnoDB
    AUTO_INCREMENT=1;
    
    CREATE TABLE IF NOT EXISTS SupportTickets (
        TicketID INT(11) NOT NULL AUTO_INCREMENT,
        UserID INT(11) NULL,  -- Allow NULLs for ON DELETE SET NULL
        Status VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
        Category VARCHAR(100) NOT NULL COLLATE 'latin1_swedish_ci',
        Description LONGTEXT NOT NULL COLLATE 'latin1_swedish_ci',
        Messages JSON NULL,
        CreatedAt TIMESTAMP NULL DEFAULT current_timestamp(),
        UpdatedAt TIMESTAMP NULL DEFAULT NULL ON UPDATE current_timestamp(),
        PRIMARY KEY (TicketID) USING BTREE,
        INDEX UserID (UserID) USING BTREE,
        CONSTRAINT supporttickets_ibfk_1 
            FOREIGN KEY (UserID) 
            REFERENCES Users (UserID) 
            ON UPDATE RESTRICT 
            ON DELETE SET NULL
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
