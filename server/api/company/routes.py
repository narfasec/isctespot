from flask import Flask, Blueprint, request, jsonify, current_app
from db.db_connector import DBConnector
import json

company = Blueprint('company', __name__)

@company.route('/analytics', methods=['GET', 'POST'])
def list_clients():
    ''' List clients function'''
    dbc = DBConnector()
    dict_data = request.get_json()
    if dict_data['token'] != current_app.config['ADMIN_AUTH_TOKEN']:
        return jsonify({'status': 'Unauthorised'}), 403
    results = dbc.execute_query(query='get_company_sales', args=dict_data['company_id'])
    print(results)
    if isinstance(results, list):
        return jsonify({'status': 'Ok', 'sales': results}), 200
    return jsonify({'status': 'Bad request'}), 403
