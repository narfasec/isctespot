import requests
import sys
import os

base_url = 'http://127.0.0.1:5000'

AUTH_TOKEN = 'W4N7CQ'
ADMIN_AUTH_TOKEN = 'Z8V9LD'

def test_output_status(status, text):
    if status == 'pass':
        print(f'\033[92m[PASS]\033[0m {text}')
    elif status == 'info':
        print(f'\033[96m[INFO]\033[0m {text}')
    else:
        print(f'\033[91m[FAIL]\033[0m {text}')
        sys.exit(1)

# User login
test_output_status('info', 'Testing User authentication')
login_url = f'{base_url}/login'
login_payload = {'username': 'jdoe', 'password': 'password123'}
login_response = requests.post(login_url, json=login_payload)
login_data = login_response.json()
user_id = 0
if login_data['status'] == 'Ok':
    test_output_status('pass', 'Login successful')
    user_id = login_data['user_id']
else:
    test_output_status('fail', 'Failed to Login user')

# User resets password
reset_password_url = f'{base_url}/user/reset-password'
reset_password_payload = {
    'user_id': user_id,
    'current_password': 'password123',
    'new_password': '1234',
    'token': AUTH_TOKEN
}

reset_password_response = requests.post(reset_password_url, json=reset_password_payload)
reset_password_data = reset_password_response.json()
if reset_password_data['status'] == 'Ok':
    test_output_status('pass', 'User reseted password')
else:
    test_output_status('fail', 'Failed to reset password')
reset_password_payload["new_password"] = reset_password_payload["current_password"]
reset_password_payload["current_password"] = '1234'
reset_password_response = requests.post(reset_password_url, json=reset_password_payload)
reset_password_data = reset_password_response.json()
if reset_password_data['status'] == 'Ok':
    test_output_status('pass', 'Reset for backward compatibile')
else:
    test_output_status('fail', 'Failed to reset password')

# List Clients
test_output_status('info', 'Testing list clients')
list_clients_url = f'{base_url}/clients'
list_clients_payload = {
    'user_id': user_id,
}
list_clients_response = requests.get(list_clients_url, json=list_clients_payload)
list_clients_data = list_clients_response.json()
if list_clients_data['status'] == 'Ok':
    test_output_status('pass', 'List clients  success')
else:
    test_output_status('fail', 'List clients failed')

# User logs out
logout_url = f'{base_url}/logout'
logout_payload = {'user_id': user_id}
logout_response = requests.post(logout_url, json=logout_payload)
logout_data = logout_response.json()
if logout_data['status'] == 'Ok':
    test_output_status('pass', 'Logout successful')
else:
    test_output_status('fail', 'Failed to logout user')

# Signup
test_output_status('info', 'Testing Signup')
signup_url = f'{base_url}/signup'
signup_payload = {
    'username': 'test-admin',
    'password': 'testpassword',
    'email': 'testadmin@email.com',
    'comp_name': 'Company Test',
    'num_employees': 2,
}
signup_response = requests.post(signup_url, json=signup_payload)
signup_data = signup_response.json()
comp_id = 0
user_id = 0
if signup_data['status'] == 'Ok':
    comp_id = signup_data['comp_id']
    user_id = signup_data['user_id']
    test_output_status('pass', 'Signup  success')
else:
    test_output_status('fail', 'Signup failed')

# Admin list all employees
test_output_status('info', 'Testing list employees')
list_employees_url = f'{base_url}/employees'
list_employees_payload = {
    'user_id': user_id,
    'token': ADMIN_AUTH_TOKEN,
    'comp_id': comp_id
}

list_employees_response = requests.get(list_employees_url, json=list_employees_payload)
list_employees_data = list_employees_response.json()
if list_employees_data['status'] == 'Ok':
    test_output_status('pass', 'List employees  success')
else:
    test_output_status('fail', 'List employees failed')

# Admin adds new users
test_output_status('info', 'Employee creation')
new_employee_url = f'{base_url}/employee/new'
new_employee_payload = {
    'username': 'employeetest',
    'email': 'employeetest@email.com',
    'comp_id': comp_id,
    'token': ADMIN_AUTH_TOKEN,
}
new_employee_response = requests.post(new_employee_url, json=new_employee_payload)
new_employee_data = new_employee_response.json()
employee_id = 0
if new_employee_data['status'] == 'Ok':
    employee_id = new_employee_data['employee_id']
    test_output_status('pass', 'Employee creation success')
else:
    test_output_status('fail', 'Employee creation failed')

# Admin updates products with file
update_products_url = f'{base_url}/update_products'
update_products_payload = {
    'comp_id': comp_id,
    'token': ADMIN_AUTH_TOKEN
}
file_path = 'flow_2/sample_products.csv'
base_dir = os.path.dirname(os.path.abspath(__file__))

# Join it with the relative path
absolute_path = os.path.join(base_dir, file_path)
# Open the file in binary mode
with open(absolute_path, 'rb') as file:
    # Send the POST request with the file
    update_products_response = requests.post(
        update_products_url,
        data=update_products_payload,
        files={'file': file}
    )
update_products_data = update_products_response.json()
if update_products_data['status'] == 'Ok':
    test_output_status('pass', 'Products update success')
else:
    test_output_status('fail', 'Products update failed')

# Employee Create new client
test_output_status('info', 'Testing new client')
new_client_url = f'{base_url}/clients/new'
new_client_payload = {
    'user_id': user_id,
    'comp_id': comp_id,
    'first_name': 'Roger',
    'last_name': 'Schmidt',
    'email': 'roger.schmidt@benfica.pt',
    'phone_number': '+351963023202',
    'address': 'Top top level street',
    'city': 'Lisbon',
    'country': 'Germany',
    'token': AUTH_TOKEN
}
new_client_response = requests.post(new_client_url, json=new_client_payload)
new_client_data = new_client_response.json()
if new_client_data['status'] == 'Ok':
    client_id = new_client_data['client_id']
    test_output_status('pass', 'New client  success')
else:
    test_output_status('fail', 'New client failed')

# Employee User creates new sale
test_output_status('info', 'Testing Sale creation')
new_sale_url = f'{base_url}/sales/new'
new_sale_payload = {
    'user_id': employee_id,
    'client_id': client_id,
    'product_id': 90,
    'token': AUTH_TOKEN,
    'quantity': 2,
}

new_sale_response = requests.post(new_sale_url, json=new_sale_payload)
new_sale_data = new_sale_response.json()
sale_id = 0
if new_sale_data['status'] == 'Ok':
    sale_id = new_sale_data['sale_id']
    test_output_status('pass', 'Sale creation success')
else:
    test_output_status('fail', 'Sale creation failed')

# Delete employee
test_output_status('info', 'Testing employee deletion')
delete_employee_url = f'{base_url}/employee/delete'
delete_employee_payload = {
    'user_id': user_id,
    'employee_id': employee_id,
    'token': ADMIN_AUTH_TOKEN,
}
delete_employee_response = requests.post(delete_employee_url, json=delete_employee_payload)
delete_employee_data = delete_employee_response.json()
if delete_employee_data['status'] == 'Ok':
    test_output_status('pass', 'Delete employee  success')
else:
    test_output_status('fail', 'Delete employee failed')


# Delete client
test_output_status('info', 'Testing delete client')
delete_client_url = f'{base_url}/clients/delete'
delete_client_payload = {
    'user_id': user_id,
    'token': ADMIN_AUTH_TOKEN,
    'client_id': client_id
}
delete_client_response = requests.post(delete_client_url, json=delete_client_payload)
delete_client_data = delete_client_response.json()
if delete_client_data['status'] == 'Ok':
    client_id = delete_client_data['client_id']
    test_output_status('pass', 'Delete client  success')
else:
    test_output_status('fail', 'Delete client failed')

# Retire
test_output_status('info', 'Testing retire')
retire_url = f'{base_url}/retire'
retire_payload = {
    'user_id': user_id,
    'comp_id': comp_id,
    'token': ADMIN_AUTH_TOKEN,
}
retire_response = requests.post(retire_url, json=retire_payload)
retire_data = retire_response.json()
if retire_data['status'] == 'Ok':
    test_output_status('pass', 'Retire  success')
else:
    test_output_status('fail', 'Retire failed')
    
# Admin overview
test_output_status('info', 'Testing analytics')
analytics_url = f'{base_url}/analytics'
analytics_payload = {
    'user_id': 1,
    'token': ADMIN_AUTH_TOKEN,
    'comp_id': 1
}
analytics_response = requests.get(analytics_url, json=analytics_payload)
analytics_data = analytics_response.json()
if analytics_data['status'] == 'Ok':
    sales = analytics_data['sales']
    test_output_status('pass', 'Company analytics success')
else:
    test_output_status('fail', 'Company analytics failed')

# Admin calculates cashflow
cash_flow_url = f'{base_url}/cash-flow'
cash_flow_payload = {
    'comp_id': 1,
    'country_code': 'PT',
    'token': ADMIN_AUTH_TOKEN
}

cash_flow_response = requests.post(cash_flow_url, json=cash_flow_payload)
cash_flow_data = cash_flow_response.json()
if cash_flow_data['status'] == 'Ok':
    test_output_status('pass', 'Cash flow calculated')
else:
    test_output_status('fail', 'Cash flow failed')

# User overview
test_output_status('info', 'Testing user overview')
user_overview_url = f'{base_url}/user/overview'
user_overview_payload = {
    'user_id': 3,
    'token': AUTH_TOKEN,
}
user_overview_response = requests.get(user_overview_url, json=user_overview_payload)
user_overview_data = user_overview_response.json()
if user_overview_data['status'] == 'Ok':
    sales = user_overview_data['sales']
    test_output_status('pass', 'User overview success')
else:
    test_output_status('fail', 'User overview failed')
