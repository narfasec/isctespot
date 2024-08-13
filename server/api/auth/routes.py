from flask import Flask, Blueprint, request, jsonify, current_app
from db.db_connector import DBConnector
import json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    ''' Login function'''
    dbc = DBConnector()
    dict_data = request.get_json()
    username = dict_data['username']
    password = dict_data['password']
    _id = dbc.execute_query(query='get_user_by_name', args=username)
    if not isinstance(_id, int):
        return jsonify({'status': 'Bad request'}), 400
    _password = dbc.execute_query(query='get_user_password', args=password)
    if password == _password:
        result = dbc.execute_query(query='update_user_activity', args={
            'user_id': _id,
            'active': True
        })
        return jsonify({'status': 'Ok', 'user_id': _id}), 200
    return jsonify({'status': 'Bad credentials'}), 403

@auth.route('/logout', methods=['POST'])
def logout():
    ''' Logout function'''
    dbc = DBConnector()
    dict_data = request.get_json()
    _id = dbc.execute_query(query='update_user_activity', args={
        'user_id': dict_data['user_id'],
        'active': False
    })
    if not isinstance(_id, int):
        return jsonify({'status': 'Bad request'}), 400
    else:
        return jsonify({'status': 'Ok'}), 200

@auth.route('/user/reset-password', methods=['POST'])
def reset_password():
    ''' Reset password function '''
    dbc = DBConnector()
    dict_data = request.get_json()
    user_id = dict_data['user_id']
    new_password = dict_data['new_password']
    token = dict_data['token']
    
    if token != current_app.config["AUTH_TOKEN"] and token != current_app.config["ADMIN_AUTH_TOKEN"]:
        return jsonify({'status': 'Unauthorised'}), 403
    
    result = dbc.execute_query(query='update_user_password', args={
        "user_id": user_id,
        "new_password": new_password
    })
    if result is True:
        return jsonify({'status': 'Ok'}), 200
    else:
        return jsonify({'status': 'Bad request'}), 400

@auth.route('/signup', methods=['POST'])
def signup():
    ''' Signup function, create new user and company'''
    dbc = DBConnector()
    dict_data = request.get_json()
    user_id = 0
    result = dbc.execute_query('create_user_admin', args={
        "username": dict_data['username'],
        "password": dict_data['password'],
        "email": dict_data['email'],
        "comp_name": dict_data['comp_name'],
        "num_employees": dict_data['num_employees']        
    })
    if isinstance(result,int):
        user_id = result
    else:
        return jsonify({'status': 'Bad request'}), 400

    result = dbc.execute_query('create_company', args={
        "user_id": user_id,
        "comp_name": dict_data['comp_name'],
        "num_employees": dict_data['num_employees']
    })
    if isinstance(result,int):
        return jsonify({'status': 'Ok', 'comp_id': result, 'user_id': user_id}), 200
    else:
        return jsonify({'status': 'Bad request'}), 400

@auth.route('/new-employee', methods=['POST'])
def new_employee():
    ''' Create new employee function '''
    dbc = DBConnector()
    dict_data = request.get_json()
    if dict_data['token'] != current_app.config['ADMIN_AUTH_TOKEN']:
        return jsonify({'status': 'Unauthorized'}), 403
    result = dbc.execute_query('create_user_employee', args={
        'username': dict_data['username'],
        'email': dict_data['email'],
        'comp_id': dict_data['comp_id']
    })
    if isinstance(result, int):
        return jsonify({'status': 'Ok', 'employee_id': result})
    else:
        return jsonify({'status': 'Bad requests'})

@auth.route('/retire', methods=['POST'])
def retire():
    ''' Retire function, delete company and all employees '''
    dbc = DBConnector()
    dict_data = request.get_json()
    if dict_data['token'] != current_app.config['ADMIN_AUTH_TOKEN']:
        return jsonify({'status': 'Unauthorized'}), 403
    result = dbc.execute_query(query='delete_users_by_comp_id', args=dict_data['comp_id'])
    if result is False:
        return jsonify({'status': 'Bad request'}), 400
    result = dbc.execute_query('delete_company_by_id', dict_data['comp_id'])
    if result is not True:
        return jsonify({'status': "Bad request"}), 400
    result = dbc.execute_query('delete_user_by_id', dict_data['user_id'])
    if result is not True:
        return jsonify({'status': "Bad request"}), 400
    if result is True:
        return jsonify({'status': 'Ok'}), 200
    else:
        return jsonify({'status': 'Bad request'}), 400

@auth.route('/delete-employee', methods=['POST'])
def delete_employee():
    ''' Delete employee function '''
    dbc = DBConnector()
    dict_data = request.get_json()
    if dict_data['token'] != current_app.config['ADMIN_AUTH_TOKEN']:
        return jsonify({'status': 'Unauthorized'}), 403
    result = dbc.execute_query('delete_user_by_id', dict_data['employee_id'])
    if result is True:
        return jsonify({'status': 'Ok'}), 200
    else:
        return jsonify({'status': "Bad request"}), 400
