from flask import Flask, Blueprint, request, jsonify, current_app
from db.db_connector import DBConnector
from services.process_sales import ProcessSales
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
    ps = ProcessSales(results, dict_data['user_id'])
    ps.get_3_most_recent_sales()
    revenue = ps.revenue
    if isinstance(results, list):
        return jsonify({'status': 'Ok', 'sales': results, 'last_3_sales': ps.last_3_sales, 'revenue': revenue}), 200
    return jsonify({'status': 'Bad request'}), 400

@sales.route('/sales/new', methods=['POST'])
def add_new_sale():
    ''' Add new sale function '''
    dbc = DBConnector()
    dict_data = request.get_json()
    if dict_data['token'] != current_app.config['ADMIN_AUTH_TOKEN'] and dict_data['token'] != current_app.config['AUTH_TOKEN']:
        return jsonify({'status': 'Unauthorised'}), 403
    result = dbc.execute_query(query='create_sale', args={
        'client_id': dict_data['client_id'],
        'user_id': dict_data['user_id'],
        'product_id': dict_data['product_id'],
        'quantity': dict_data['quantity']
    })
    if isinstance(result, int):
        return jsonify({'status': 'Ok', 'sale_id': result}), 200
    return jsonify({'status': 'Bad request'}), 400
