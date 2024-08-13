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
                    CREATE
                        'create_user_employee'      args: {username, email, company_id}
                        'create_user_admin'         args: {username, password, email}
                        'create_company'            args: {company_name, n_employees}
                    UPDATE
                        'update_user_password'      args: {user_id, new_password}
                    DELETE
                        'delete_users_by_comp_id'   args: {user_id, company_id}
                        'delete_user_by_id'         args:user_id
                        'delete_company_by_id'      args:company_id
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
                if isinstance(result, tuple):
                    return result[0]['UserID']
                else:
                    return result["UserID"]

            elif query == 'get_user_password':
                cursor.execute("SELECT PasswordHash FROM Users WHERE PasswordHash = ?", (args,))
                result = cursor.fetchone()
                if isinstance(result, tuple):
                    return result[0]['PasswordHash']
                else:
                    return result['PasswordHash']

            elif query == 'get_user_by_id':
                cursor.execute("SELECT * FROM Users WHERE UserID = ?", (args,))
                result = cursor.fetchone()

            elif query == 'create_user_employee':
                cursor.execute(
                    "INSERT INTO Users (Username, PasswordHash, Email, CompanyID, CommissionPercentage, CreatedAt) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                    (args['username'], 'T3MP-password-32',args['email'], args['comp_id'], 5)
                )
                connection.commit()
                result = cursor.lastrowid
                print(result)
                if isinstance(result, int):
                    return True
                else:
                    return False
                
            elif query == 'create_user_admin':
                cursor.execute(
                    "INSERT INTO Users (Username, PasswordHash, Email, CreatedAt) VALUES (?, ?, ?, CURRENT_TIMESTAMP);",
                    (args['username'], args['password'],args['email'])
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
            
            elif query == 'delete_users_by_comp_id':
                cursor.execute("DELETE FROM Users WHERE CompanyID = ?", (args,))
                connection.commit()
                result = cursor.rowcount
                if isinstance(result, tuple):
                    result = result[0]
                if cursor.rowcount > 0:
                    return True
                else:
                    return False
                
            elif query == 'delete_user_by_id':
                cursor.execute("DELETE FROM Users WHERE UserID = ?", (args,))
                connection.commit()
                result = cursor.rowcount
                if isinstance(result, tuple):
                    result = result[0]
                if cursor.rowcount > 0:
                    return True
                else:
                    return False

            elif query == 'delete_company_by_id':
                cursor.execute("DELETE FROM Companies WHERE CompanyID = ?", (args,))
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
