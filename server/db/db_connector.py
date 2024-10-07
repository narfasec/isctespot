import mariadb
class DBConnector:

    def __init__(self):
        self.host = 'mariadb'
        self.user = 'root'
        self.password = 'teste123'
        self.database = 'iscte_spot'
        self.port = 3306

    def connect(self):
        ''' Connect to database mariadb'''
        try:
            connection = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            return connection
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            return None

    def execute_query(self, query, args=None):
        ''' Execute queries by query name
            query:
                READ
                    'get_user_by_name'          args:username       |       return: user id if exits if not, return false
                    'get_user_password'         args:user_id        |       return: password id if exits if not, return false
                    'get_user_by_id'            args:user_id        |       return: all parameters
                    'get_user_sales'            args:user_id        |       return: list of sales by the user
                    'get_clients_list'          args:company_id     |       return: list of clients
                    'get_employees_list'        args:company_id     |       return: list of employees
                    'get_user_admin'            args:user_id        |       return: is_admin value (True or False)
                    'get_user_comp_id'          args:user_id        |       return: comp_id
                    'get_products_list'         args:comp_id        |       return: list of products
                    'get_company_revenue'       args:comp_id        |       return: revenue
                    'get_last_3_sales'          args:user_id        |       return: list of last_3_sales
                    'get_sales_month_comp_id'   args:month,comp_id  |       return: list of sales of selected month
                    'get_costs_sales_month'     args:month,comp_id  |       return: production costs and sales revenue for given month
                CREATE
                    'create_user_employee'      args: {username, email, company_id}
                    'create_user_admin'         args: {username, password, email}
                    'create_company'            args: {company_name, n_employees}
                    'create_client'             args: {first_name, last_name, email, phone_number, address, city, country, company_id}
                    'create_sale'               args: {client_id, user_id, product, price, quantity}
                UPDATE
                    'update_user_password'      args: {user_id, new_password}
                    'update_user_comp_id'       args: {user_id, comp_id}
                    'update_products_by_comp_id args: {file, comp_id}
                    'update_company_revenue'    args: comp_id
                DELETE
                    'delete_users_by_comp_id'   args: {user_id, company_id}
                    'delete_user_by_id'         args: user_id
                    'delete_company_by_id'      args: company_id
                    'delete_client_by_id'       args: client_id
        '''
        print(f'DB query selceted: {query}, args: {args}')
        connection = self.connect()
        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)
        result = None
        try:
            if query == 'get_user_by_name':
                cursor.execute("SELECT UserID FROM Users WHERE Username = ?", (args,))
                result = cursor.fetchone()
                try:
                    if isinstance(result, tuple):
                        result = result[0]['UserID']
                        if result == 1:
                            return True
                    else:
                        result = result["UserID"]
                        if result == 0:
                            return False
                except TypeError:
                    return 'TypeError'

            elif query == 'get_user_password':
                cursor.execute("SELECT PasswordHash FROM Users WHERE UserID = ?", (args,))
                result = cursor.fetchone()
                try:
                    if isinstance(result, tuple):
                        return result[0]['PasswordHash']
                    else:
                        return result['PasswordHash']
                except TypeError:
                    return False

            elif query == 'get_user_by_id':
                cursor.execute(f"SELECT * FROM Users WHERE UserID = {args}")
                result = cursor.fetchone()

            elif query == 'get_clients_list':
                cursor.execute(
                    f"""
                    SELECT ClientID, FirstName, LastName, Email, PhoneNumber, Address, City, Country
                    FROM Clients
                    WHERE CompanyID = {args}
                    """)
                result = cursor.fetchall()
                if isinstance(result, list):
                    return result
                else:
                    return False

            elif query == 'get_employees_list':
                cursor.execute(f"SELECT UserID, Username, Email, CommissionPercentage, isActive FROM Users WHERE CompanyID = {args}")
                result = cursor.fetchall()
                if isinstance(result, list):
                    return result
                else:
                    return False

            elif query == 'get_compnay_id_by_user':
                cursor.execute(f'SELECT CompanyID FROM Users WHERE UserID = {args}')
                result = cursor.fetchone()
                print(result)
                if isinstance(result, tuple):
                    return result[0]['CompanyID']
                else:
                    return result["CompanyID"]

            elif query == 'get_company_sales':
                cursor.execute(
                    f"""
                    SELECT Sales.SaleID, Products.ProductName, Users.Username, Clients.FirstName, Clients.FirstName, Products.SellingPrice, Sales.Quantity, Sales.SaleDate
                    FROM Sales
                    JOIN Clients ON Sales.ClientID = Clients.ClientID
                    JOIN Users ON Sales.UserID = Users.UserID
                    JOIN Products ON Sales.ProductID = Products.ProductID
                    WHERE Clients.CompanyID = {args};
                    """
                )
                result = cursor.fetchall()
                if isinstance(result, list):
                    return result
                else:
                    return False

            elif query == 'get_user_sales':
                cursor.execute(
                    f"""
                    SELECT 
                        S.SaleID,
                        U.UserName,    
                        C.FirstName,   
                        P.ProductName,
                        P.SellingPrice,
                        S.Quantity,
                        S.SaleDate
                    FROM 
                        Sales S
                    JOIN 
                        Users U ON S.UserID = U.UserID       -- Join the Users table to get UserName
                    JOIN 
                        Clients C ON S.ClientID = C.ClientID -- Join the Clients table to get ClientName
                    JOIN 
                        Products P ON S.ProductID = P.ProductID -- Join the Products table to get ProductName
                    WHERE 
                        S.UserID = {args};
                    """
                )
                result = cursor.fetchall()
                print(result)
                if isinstance(result, list):
                    return result
                else:
                    return False

            elif query == 'get_user_admin':
                cursor.execute(
                    f"""
                    SELECT IsAdmin FROM Users WHERE UserID = {args};
                    """
                )
                result = cursor.fetchone()
                print(result)
                if isinstance(result, tuple):
                    return result[0]['IsAdmin']
                else:
                    return result['IsAdmin']

            elif query == 'get_user_comp_id':
                cursor.execute(
                    f"""
                    SELECT CompanyID FROM Users WHERE UserID = {args};
                    """
                )
                result = cursor.fetchone()
                print(result)
                if isinstance(result, tuple):
                    return result[0]['CompanyID']
                else:
                    return result['CompanyID']

            elif query == 'get_products_list':
                cursor.execute(f"SELECT ProductID, ProductName, SellingPrice FROM Products WHERE CompanyID = {args}")
                result = cursor.fetchall()
                if isinstance(result, list):
                    return result
                else:
                    return False

            elif query == 'get_company_revenue':
                cursor.execute(f"SELECT Revenue FROM Companies WHERE CompanyID = {args}")
                result = cursor.fetchone()
                if isinstance(result, tuple):
                    return result[0]
                return result['Revenue']
            
            elif query == 'get_employees_return':
                cursor.execute(
                    f"""
                            SELECT 
                                u.UserID,
                                u.Username,
                                u.CommissionPercentage,
                                COUNT(s.SaleID) AS total_sales,
                                SUM(s.Quantity * p.SellingPrice) AS total_sales_amount,
                                (SUM(s.Quantity * p.SellingPrice) * (u.CommissionPercentage / 100)) AS total_commission
                            FROM Users u
                            LEFT JOIN Sales s ON u.UserID = s.UserID
                            LEFT JOIN Products p ON s.ProductID = p.ProductID
                            WHERE u.CompanyID = {args['comp_id']} 
                            AND p.CompanyID = u.CompanyID
                            AND MONTH(s.SaleDate) = {args['month']}
                            AND YEAR(s.SaleDate) = 2024
                            GROUP BY u.UserID, u.CommissionPercentage
                    """
                )
                result = cursor.fetchall()
                # Format the result into a list of dictionaries
                employee_sales_data = []
                print(f'Result: {result}')
                for row in result:
                    employee_sales_data.append({
                        "UserID": row['UserID'],
                        "Username": row['Username'],
                        "CommissionPercentage": row['CommissionPercentage'],
                        "TotalSales": row['total_sales'],
                        "TotalSalesAmount": row['total_sales_amount'],
                        "TotalCommission": row['total_commission']
                    })

                return employee_sales_data
            
            elif query == 'get_last_3_sales':
                cursor.execute(
                    f"""
                    SELECT 
                        S.SaleID,
                        U.UserName,    
                        C.FirstName,   
                        P.ProductName,
                        P.SellingPrice,
                        S.Quantity,
                        S.SaleDate
                    FROM 
                        Sales S
                     JOIN
                        Users U ON S.UserID = U.UserID       -- Join the Users table to get UserName
                    JOIN 
                        Clients C ON S.ClientID = C.ClientID -- Join the Clients table to get ClientName
                    JOIN 
                        Products P ON S.ProductID = P.ProductID -- Join the Products table to get ProductName
                    WHERE 
                        S.UserID = {args}
                  	ORDER BY
                        S.SaleDate DESC
                   LIMIT 3;
                    """
                )
                result = cursor.fetchall()
                print(result)
                if isinstance(result, list):
                    return result
                else:
                    return False
            
            elif query == 'get_sales_month_comp_id':
                cursor.execute(
                    """
                    SELECT 
                        Sales.SaleID,
                        Sales.UserID,
                        Sales.ClientID,
                        Sales.ProductID,
                        Sales.Quantity,
                        Sales.SaleDate
                    FROM 
                        Sales
                    JOIN 
                        Users ON Sales.UserID = Users.UserID
                    WHERE 
                        Users.CompanyID = ?
                        AND MONTH(Sales.SaleDate) = ?
                        AND YEAR(Sales.SaleDate) = 2024;
                    """,
                    (args['comp_id'], args['month'])
                )
                result = cursor.fetchall()
                if isinstance(result, list):
                    return result
                else:
                    return False

            elif query == 'get_costs_sales_month':
                cursor.execute(
                    f"""
                    SELECT 
                        SUM(Products.SellingPrice * Sales.Quantity) AS TotalSellingPrice,
                        SUM(Products.FactoryPrice * Sales.Quantity) AS TotalFactoryPrice
                    FROM 
                        Sales
                    JOIN 
                        Products ON Sales.ProductID = Products.ProductID
                    WHERE 
                        Products.CompanyID = {args['comp_id']}
                        AND MONTH(Sales.SaleDate) = {args['month']}
                        AND YEAR(Sales.SaleDate) = 2024;
                    """
                )
                result = cursor.fetchone()
                print(result)
                try:
                    if isinstance(result, tuple):
                        return result[0]
                    else:
                        return result
                except TypeError:
                    return False
            elif query == 'create_user_employee':
                cursor.execute(
                    "INSERT INTO Users (Username, PasswordHash, Email, CompanyID, CommissionPercentage, CreatedAt) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                    (args['username'], 'T3MP-password-32',args['email'], args['comp_id'], 5)
                )
                connection.commit()
                result = cursor.lastrowid
                if isinstance(result, tuple):
                    return result[0]
                else:
                    return result

            elif query == 'create_user_admin':
                cursor.execute(
                    "INSERT INTO Users (Username, PasswordHash, Email, IsAdmin, CreatedAt) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP);",
                    (args['username'], args['password'],args['email'], args['is_admin'])
                )
                connection.commit()
                result = cursor.lastrowid
                if isinstance(result, tuple):
                    return result[0]
                else:
                    return result

            elif query == 'create_company':
                cursor.execute(
                    "INSERT INTO Companies (CompanyName, NumberOfEmployees, AdminUserID, Revenue) VALUES (?, ?, ?, ?)",
                    (args['comp_name'], args['num_employees'], args['user_id'], 0)
                )
                connection.commit()
                result = cursor.lastrowid
                if isinstance(result, tuple):
                    return result[0]
                else:
                    return result

            elif query == 'create_client':
                cursor.execute(
                    "INSERT INTO Clients (FirstName, LastName, Email, PhoneNumber, Address, City, Country, CompanyID, CreatedAt) VALUES (?, ?, ?, ?, ?, ? ,?, ?, CURRENT_TIMESTAMP)",
                    (args['first_name'], args['last_name'], args['email'], args['phone_number'], args['address'], args['city'], args['country'], args['comp_id'])
                )
                connection.commit()
                result = cursor.lastrowid
                if isinstance(result, tuple):
                    return result[0]
                else:
                    return result
            
            elif query == 'create_sale':
                cursor.execute(
                    "INSERT INTO Sales (UserID, ClientID, ProductID, Quantity, SaleDate) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                    (args['user_id'], args['client_id'], args['product_id'], args['quantity'])
                )
                connection.commit()
                result = cursor.lastrowid
                print(result)
                if isinstance(result, tuple):
                    return result[0]
                else:
                    return result

            elif query == 'update_user_password':
                cursor.execute(
                    "UPDATE Users SET PasswordHash = ? WHERE UserID = ?;",
                    (args["new_password"], args["user_id"])
                )
                connection.commit()
                result = cursor.rowcount
                if isinstance(result, tuple):
                    result = result[0]
                if cursor.rowcount > 0:
                    return True
                else:
                    return False

            elif query == 'update_user_comp_id':
                cursor.execute(
                    "UPDATE Users SET CompanyID = ? WHERE UserID = ?;",
                    (args["comp_id"], args["user_id"])
                )
                connection.commit()
                result = cursor.rowcount
                if isinstance(result, tuple):
                    result = result[0]
                if cursor.rowcount > 0:
                    return True
                else:
                    return False

            elif query == 'update_user_activity':
                if args['active']:
                    cursor.execute(f"UPDATE Users SET LastLogin = CURRENT_TIMESTAMP, isActive = True WHERE UserID = {args['user_id']}")
                else:
                    cursor.execute(f"UPDATE Users SET LastLogout = CURRENT_TIMESTAMP, isActive = False WHERE UserID = {args['user_id']}")
                connection.commit()
                result = cursor.rowcount
                if isinstance(result, tuple):
                    result = result[0]
                return result

            elif query == 'update_products_by_comp_id':
                cursor.execute(
                    f"""
                    DELETE FROM Products WHERE CompanyID = {args['comp_id']}
                    """
                )

                insert_query = """
                    INSERT INTO Products (ProductID, CompanyID, ProductName, FactoryPrice, SellingPrice, CreatedAt)
                    VALUES (?, ?, ?, ?, ?, ?)
                """

                for index, row in args['file'].iterrows():
                    cursor.execute(insert_query, (row['ProductID'], args['comp_id'], row['ProductName'],row['FactoryPrice'], row['SellingPrice'],  row['CreatedAt']))
                
                connection.commit()
                return True

            elif query == 'update_company_revenue':

                cursor.execute(
                    f"""
                    SELECT SUM(s.Quantity * p.SellingPrice) AS total_sales
                    FROM Sales s
                    JOIN Products p ON s.ProductID = p.ProductID
                    JOIN Users u ON s.UserID = u.UserID
                    WHERE u.CompanyID = {args};
                    """
                )
                result = cursor.fetchone()
                if isinstance(result, dict):
                    result = result['total_sales']

                cursor.execute(
                    f"""
                    UPDATE Companies
                    SET Revenue = {result}
                    WHERE CompanyID = {args}
                    """
                )
                connection.commit()
                affected_rows = cursor.rowcount
                return affected_rows > 0

            elif query == 'delete_sales_by_comp_id':
                cursor.execute(
                    f"""
                    DELETE FROM sales
                    WHERE UserID IN (
                        SELECT UserID
                        FROM users
                        WHERE CompanyID = {args}
                    );

                    """)
                connection.commit()
                result = cursor.rowcount
                return True

            elif query == 'update_seller_commission':
                value = args['new_commission']
                user_id = args['seller_id']
                cursor.execute(
                    f"""
                    UPDATE Users
                    SET CommissionPercentage = {value}
                    WHERE UserID = {user_id};
                    """
                )
                connection.commit()
                result = cursor.rowcount
                print(result)
                if isinstance(result, tuple):
                    result = result[0]
                return result

            elif query == 'delete_sales_by_comp_id':
                cursor.execute(
                    f"""
                    DELETE FROM sales
                    WHERE UserID IN (
                        SELECT UserID
                        FROM users
                        WHERE CompanyID = {args}
                    );

                    """)
                connection.commit()
                result = cursor.rowcount
                print('Deleting Sales')
                print(result)
                return True
            elif query == 'delete_products_by_comp_id':
                cursor.execute(f"DELETE FROM Products WHERE CompanyID = {args}")
                connection.commit()
                result = cursor.rowcount
                return True
            
            elif query == 'delete_users_by_comp_id':
                cursor.execute(f"DELETE FROM Users WHERE CompanyID = {args}")
                connection.commit()
                result = cursor.rowcount
                return True

            elif query == 'delete_user_by_id':
                cursor.execute("DELETE FROM Users WHERE UserID = ?", (args,))
                connection.commit()
                result = cursor.rowcount
                print(result)
                if result > 0:
                    return True
                else:
                    return False

            elif query == 'delete_company_by_id':
                cursor.execute(f"DELETE FROM Companies WHERE CompanyID = ?", (args,))
                connection.commit()
                result = cursor.rowcount
                if isinstance(result, tuple):
                    result = result[0]
                if cursor.rowcount > 0:
                    return True
                else:
                    return False

            elif query == 'delete_client_by_id':
                cursor.execute(f"DELETE FROM Clients WHERE ClientID = {args}")
                connection.commit()
                result = cursor.rowcount
                if isinstance(result, tuple):
                    result = result[0]
                if cursor.rowcount > 0:
                    return True
                else:
                    return False

        except mariadb.Error as e:
            print(f"Error: {e}")
            result = None
        finally:
            cursor.close()
            connection.close()
        return result
