import requests
import json
import sys

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
login_payload = {'username': 'testuser', 'password': 'testpassword'}
login_response = requests.post(login_url, json=login_payload)
login_data = login_response.json()
user_id = 0
if login_data['status'] == 'Ok':
    test_output_status('pass', 'Login successful')
    user_id = login_data['user_id']
else:
    test_output_status('fail', 'Failed to Login user')

# User resets password
test_output_status('info', 'Testing User resting password')
reset_password_url = f'{base_url}/user/reset-password'
reset_password_payload = {
    'user_id': user_id,
    'current_password': 'testpassword',
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
user_id = 0
if reset_password_data['status'] == 'Ok':
    test_output_status('pass', 'Reset for backward compatibile')
else:
    test_output_status('fail', 'Failed to reset password')

# Signup
test_output_status('info', 'Testing Signup')
signup_url = f'{base_url}/signup'
signup_payload = {
    'username': 'test-admin',
    'password': 'testpassword',
    'email': 'testadmin@email.com',
    'comp_name': 'Company Test',
    'num_employees': '1-10',
}
signup_response = requests.post(signup_url, json=signup_payload)
signup_data = signup_response.json()
comp_id = 0
if signup_data['status'] == 'Ok':
    comp_id = signup_data['comp_id']
    user_id = signup_data['user_id']
    test_output_status('pass', 'Signup  success')
else:
    test_output_status('fail', 'Signup failed')

# Admin adds new users
test_output_status('info', 'Employee creation')
new_employee_url = f'{base_url}/new-employee'
new_employee_payload = {
    'username': 'employeetest',
    'email': 'employeetest@email.com',
    'comp_id': comp_id,
    'token': ADMIN_AUTH_TOKEN,
}
new_employee_response = requests.post(new_employee_url, json=new_employee_payload)
new_employee_data = new_employee_response.json()
if new_employee_data['status'] == 'Ok':
    test_output_status('pass', 'Employee creation success')
else:
    test_output_status('fail', 'Employee creation failed')

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