from flask import Flask, Blueprint, request, jsonify, current_app
from db.db_connector import DBConnector
import json

sales = Blueprint('sales', __name__)

@sales.route('/user/overview', methods=['GET', 'POST'])
def list_user_sales():
    ''' List user sales function'''
    dbc = DBConnector()
    dict_data = request.get_json()
    if dict_data['token'] != current_app.config['ADMIN_AUTH_TOKEN'] and dict_data['token'] != current_app.config['AUTH_TOKEN']:
        return jsonify({'status': 'Unauthorised'}), 403
    results = dbc.execute_query(query='get_user_sales', args=dict_data['user_id'])
    if isinstance(results, list):
        return jsonify({'status': 'Ok', 'sales': results}), 200
    return jsonify({'status': 'Bad request'}), 400
