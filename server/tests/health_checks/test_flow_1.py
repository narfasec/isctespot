import requests
import json
import sys

base_url = 'http://127.0.0.1:5000'

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
login_payload = {"username": "testuser", "password": "testpassword"}
login_response = requests.post(login_url, json=login_payload)
login_data = login_response.json()
if login_data['status'] == 'Ok':
    test_output_status('pass', 'Login successful')
else:
    test_output_status('fail', 'Failed to Login user')
