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
        return jsonify({'status': 'Ok', 'user_id': _id}), 200
    return jsonify({'status': 'Bad credentials'}), 403

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
    if result is True:
        return jsonify({'status': 'Ok'}), 200
    else:
        return jsonify({'status': 'Bad request'}), 400

# @auth.route('/retire', methods=['POST'])
# def retire():
    