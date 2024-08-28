import mariadb
import sys
class DBConnector:

    def __init__(self ):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'teste123'
        self.database = 'iscte_spot'
        self.port = 3306

    def connect(self):
        print("Trying connection to DB")
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
                Auth:
                    READ
                        'get_user_by_name'          args:username       |       return: user id if exits if not, return false
                        'get_user_password'         args:password       |       return: password id if exits if not, return false
                        'get_user_by_id'            args:user_id        |       return: all parameters
                        'get_user_sales             args:user_id        |       return: list of sales by the user
                        'get_clients_list'          args:company_id     |       return: list of clients
                        'get_employees_list'        args:company_id     |       return: list of employees
                        'get_user_admin'            args:user_id        |       return: is_admin value (True or False)
                        'get_user_comp_id'          args:user_id        |       return: comp_id
                    CREATE
                        'create_user_employee'      args: {username, email, company_id}
                        'create_user_admin'         args: {username, password, email}
                        'create_company'            args: {company_name, n_employees}
                        'create_client'             args: {first_name, last_name, email, phone_number, address, city, country, company_id}
                        'create_sale'               args: {client_id, user_id, product, price, quantity}
                    UPDATE
                        'update_user_password'      args: {user_id, new_password}
                        'update_user_comp_id'       args: {user_id, comp_id}
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
                cursor.execute(f"SELECT UserID FROM Users WHERE Username = {args}")
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
                cursor.execute(f"SELECT PasswordHash FROM Users WHERE PasswordHash = {args}")
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
                    SELECT Sales.SaleID, Sales.UserID, Sales.ClientID, Sales.ProductName, Sales.Quantity, Sales.Price, Sales.SaleDate
                    FROM Sales
                    JOIN Clients ON Sales.ClientID = Clients.ClientID
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
                    SELECT * FROM Sales WHERE UserID = {args};
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

            elif query == 'create_user_employee':
                
                cursor.execute(
                    f"""
                    INSERT INTO Users (Username, PasswordHash, Email, CompanyID, CommissionPercentage, CreatedAt)
                    VALUES ({args['username']}, 'T3MP-password-32', {args['email']}, {args['comp_id']}, 5, CURRENT_TIMESTAMP)
                    """
                )
                connection.commit()
                result = cursor.lastrowid
                if isinstance(result, tuple):
                    return result[0]
                else:
                    return result

            elif query == 'create_user_admin':
                cursor.execute(
                    f"""INSERT INTO Users (Username, PasswordHash, Email, IsAdmin, CreatedAt) 
                    VALUES ({args['username']}, {args['password']}, {args['email']}, {args['is_admin']}, CURRENT_TIMESTAMP);
                    """
                )
                connection.commit()
                result = cursor.lastrowid
                if isinstance(result, tuple):
                    return result[0]
                else:
                    return result

            elif query == 'create_company':
                cursor.execute(
                    f"""
                    INSERT INTO Companies (CompanyName, NumberOfEmployees, AdminUserID, Revenue)
                    VALUES ({args['comp_name']}, {args['num_employees']}, {args['user_id']}, 0)
                    """
                )
                connection.commit()
                result = cursor.lastrowid
                if isinstance(result, tuple):
                    return result[0]
                else:
                    return result

            elif query == 'create_client':
                cursor.execute(
                    f"""
                    INSERT INTO Clients (FirstName, LastName, Email, PhoneNumber, Address, City, Country, CompanyID, CreatedAt)
                    VALUES ({args['first_name']}, {args['last_name']}, {args['email']}, {args['phone_number']}, {args['address']}, {args['city']}, {args['country']}, {args['comp_id']}, CURRENT_TIMESTAMP)
                    """
                )
                connection.commit()
                result = cursor.lastrowid
                if isinstance(result, tuple):
                    return result[0]
                else:
                    return result
            
            elif query == 'create_sale':
                cursor.execute(
                    f"""
                    INSERT INTO Sales (UserID, ClientID, ProductName, Quantity, Price, SaleDate)
                    VALUES ({args['user_id']}, {args['client_id']}, {args['product']}, {args['quantity']}, {args['price']}, CURRENT_TIMESTAMP)
                    """
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
                    f"""
                    UPDATE Users SET PasswordHash = {args["new_password"]} WHERE UserID = {args["user_id"]};
                    """
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
                    f"""
                    UPDATE Users SET CompanyID = {args["comp_id"]} WHERE UserID = {args["user_id"]}
                    """
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

            elif query == 'delete_users_by_comp_id':
                cursor.execute(f"DELETE FROM Users WHERE CompanyID = {args}")
                connection.commit()
                result = cursor.rowcount
                return True

            elif query == 'delete_user_by_id':
                cursor.execute(f"DELETE FROM Users WHERE UserID = {args}")
                connection.commit()
                result = cursor.rowcount
                print(result)
                if isinstance(result, tuple):
                    result = result[0]
                if cursor.rowcount > 0:
                    return True
                else:
                    return False

            elif query == 'delete_company_by_id':
                cursor.execute(f"DELETE FROM Companies WHERE CompanyID = {args}")
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
