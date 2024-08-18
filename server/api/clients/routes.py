from flask import Flask, Blueprint, request, jsonify, current_app
from db.db_connector import DBConnector
import json

clients = Blueprint('clients', __name__)

@clients.route('/clients', methods=['GET', 'POST'])
def list_clients():
    ''' List clients function'''
    dbc = DBConnector()
    dict_data = request.get_json()
    comp_id = dbc.execute_query(query='get_compnay_id_by_user', args=dict_data['user_id'])
    results = dbc.execute_query(query='get_clients_list', args=comp_id)
    if isinstance(results, list):
        return jsonify({'status': 'Ok', 'clients': results}), 200
    return jsonify({'status': 'Bad credentials'}), 403

@clients.route('/clients/new', methods=['POST'])
def new_client():
    ''' Create a new client '''
    dbc = DBConnector()
    dict_data = request.get_json()
    result = dbc.execute_query('create_client', args={
        'comp_id': dict_data['comp_id'],
        'first_name': dict_data['first_name'],
        'last_name': dict_data['last_name'],
        'email': dict_data['email'],
        'phone_number': dict_data['phone_number'],
        'address': dict_data['address'],
        'city': dict_data['city'],
        'country': dict_data['country'],
    })
    if isinstance(result, int):
        return jsonify({'status': 'Ok', 'client_id':result}), 200
    else:
        return jsonify({'status': 'Bad reuest'}), 400

@clients.route('/clients/delete', methods=['POST'])
def delete_client():
    ''' Delete client '''
    dbc = DBConnector()
    dict_data = request.get_json()
    token = dict_data['token']
    if token != current_app.config["ADMIN_AUTH_TOKEN"]:
        return jsonify({'status': 'Unauthorised'}), 403
    result = dbc.execute_query(query='delete_client_by_id', args=dict_data['client_id'])
    if isinstance(result, int):
        return jsonify({'status': 'Ok', 'client_id':result}), 200
    else:
        return jsonify({'status': 'Bad reuest'}), 400
 