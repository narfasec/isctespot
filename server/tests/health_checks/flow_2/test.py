import requests
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

# Admin logs-in
test_output_status('info', 'Testing User authentication')
login_url = f'{base_url}/login'
login_payload = {'username': 'jdoe', 'password': 'teste123'}
login_response = requests.post(login_url, json=login_payload)
login_data = login_response.json()
user_id = 0
if login_data['status'] == 'Ok':
    test_output_status('pass', 'Login successful')
    user_id = login_data['user_id']
else:
    test_output_status('fail', 'Failed to Login user')

# Admin lists products
list_products_url = f'{base_url}/products'
list_products_payload = {
    'comp_id': 1,
    'token': ADMIN_AUTH_TOKEN
}
list_products_response = requests.post(login_url, json=login_payload)
list_products_data = list_products_response.json()
if list_products_data['status'] == 'Ok':
    test_output_status('pass', 'Products list success')
else:
    test_output_status('fail', 'Products list failed')

# Admin updates products with file
update_products_url = f'{base_url}/update_products'
update_products_payload = {
    'comp_id': 1,
    'token': ADMIN_AUTH_TOKEN
}
file_path = 'sample_products.csv'

# Open the file in binary mode
with open(file_path, 'rb') as file:
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

# Admin logs-out
