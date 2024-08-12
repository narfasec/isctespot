from flask import Flask, Blueprint, request, jsonify
from db.db_connector import DBConnector
import json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    ''' Login function'''
    dbc = DBConnector()
    dict_data = request.get_json()
    print(dict_data)
    username = dict_data['username']
    password = dict_data['password']
    print(username)
    print(password)
    _id = dbc.execute_query(query='get_user_by_name', args=username)
    if not isinstance(_id, int):
         return jsonify({'status': 'Bad request'}), 400
    _password = dbc.execute_query(query='get_user_password', args=password)
    if password == _password:
        return jsonify({'status': 'Ok', 'user_id': _id}), 200
    return jsonify({'status': 'Bad credentials'}), 403
    
# @auth.route('/signup')
# def signup():
#     ''' Signup function '''