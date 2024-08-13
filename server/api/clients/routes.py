from flask import Flask, Blueprint, request, jsonify, current_app
from db.db_connector import DBConnector
import json

clients = Blueprint('clients', __name__)

@clients.route('/clients', methods=['GET'])
def list_clients():
    ''' List clients function'''
    dbc = DBConnector()
    dict_data = request.get_json()
    comp_id = dbc.execute_query(query='get_compnay_id_by_user', args=dict_data['user_id'])
    results = dbc.execute_query(query='get_clients_list', args=comp_id)
    if isinstance(results, list):
        return jsonify({'status': 'Ok', 'clients': results}), 200
    return jsonify({'status': 'Bad credentials'}), 403
