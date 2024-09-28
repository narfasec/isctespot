from flask import Flask, Blueprint, request, jsonify, current_app
from db.db_connector import DBConnector
from services.process_file import ProcessFile
from services.process_cash_flow import ProcessCashFlow
from services.process_sales     import ProcessSales

company = Blueprint('company', __name__)

@company.route('/analytics', methods=['GET', 'POST'])
def list_clients():
    ''' List Sales function'''
    dbc = DBConnector()
    dict_data = request.get_json()
    if dict_data['token'] != current_app.config['ADMIN_AUTH_TOKEN']:
        return jsonify({'status': 'Unauthorised'}), 403
    results = dbc.execute_query(query='get_company_sales', args=dict_data['comp_id'])
    print(results)
    pcf = ProcessCashFlow(dict_data['comp_id'], 'PT')
    revenue = pcf.revenue
    ps = ProcessSales(results, dict_data['user_id'])
    ps.get_3_most_recent_sales()
    if isinstance(results, list):
        return jsonify({'status': 'Ok', 'last_3_sales': ps.last_3_sales, 'revenue': revenue, 'sales': results}), 200
    return jsonify({'status': 'Bad request'}), 403

@company.route('/employees', methods=['GET', 'POST'])
def list_employees():
    ''' List employees function'''
    dbc = DBConnector()
    dict_data = request.get_json()
    if dict_data['token'] != current_app.config['ADMIN_AUTH_TOKEN']:
        return jsonify({'status': 'Unauthorised'}), 403
    results = dbc.execute_query(query='get_employees_list', args=dict_data['comp_id'])
    if isinstance(results, list):
        return jsonify({'status': 'Ok', 'employees': results}), 200
    return jsonify({'status': 'Bad request'}), 403

@company.route('/products', methods=['GET', 'POST'])
def list_products():
    ''' List products for given company '''
    dbc = DBConnector()
    dict_data = request.get_json()
    if dict_data['token'] != current_app.config['ADMIN_AUTH_TOKEN'] and dict_data['token'] != current_app.config['AUTH_TOKEN']:
        return jsonify({'status': 'Unauthorised'}), 403
    results = dbc.execute_query(query='get_products_list', args=dict_data['comp_id'])
    if isinstance(results, list):
        return jsonify({'status': 'Ok', 'products': results}), 200
    return jsonify({'status': 'Bad request'}), 403
    
@company.route('/update_products', methods=['POST'])
def upload_excel():
    ''' Update company products from csv or xlsx '''
    token = request.form.get('token')
    comp_id = request.form.get('comp_id')
    if token != current_app.config['ADMIN_AUTH_TOKEN']:
        return jsonify({'status': 'Unauthorized'}), 403
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    pf = ProcessFile(file, comp_id)
    if not pf.is_updated:
        return jsonify({'error': 'File processing failed'}), 400

    return jsonify({'status': 'Ok','message': 'File successfully uploaded'}), 200

@company.route('/cash-flow', methods=['POST'])
def cash_flow():
    ''' Calculate compnay's cash flow '''
    dict_data = request.get_json()
    if dict_data['token'] != current_app.config['ADMIN_AUTH_TOKEN']:
        return jsonify({'status': 'Unauthorised'}), 403
    pcf = ProcessCashFlow(country_code=dict_data['country_code'], company_id=dict_data['comp_id'])
    return jsonify(
        {
            'status': 'Ok',
            'revenue': pcf.revenue,
            'profit': pcf.profit,
            'employees': pcf.employees,
            'vat': pcf.vat,
            'vat_value': pcf.vat_value,
            'totalEmployeesPayment': pcf.total_payment
        }
    ), 200
