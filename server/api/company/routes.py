import os
from flask import Flask, Blueprint, request, jsonify, current_app, abort, send_file
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
    pcf = ProcessCashFlow(dict_data['comp_id'], 'PT', month=7) ### in this case we don't cate about the month, let's give one value just to simplify
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

@company.route('/invoice', methods=['GET', 'POST'])
def invoice():
    ''' List products for given company '''
    filename = request.args.get('filename')
    # Construct the full file path
    _dir = os.path.join(os.path.dirname(__file__), 'invoices')
    file_path = os.path.join(_dir, filename)

    # Check if the file exists
    if os.path.exists(file_path):
        try:
            # Send the file to the client with the proper mimetype
            return send_file(file_path, as_attachment=True)
        except Exception as e:
            return str(e), 500
    else:
        # If the file doesn't exist, return a 404 error
        abort(404, description="File not found")

@company.route('/seller/update-commission', methods=['GET', 'POST'])
def update_commission():
    ''' Update seller commission '''
    dict_data = request.get_json()
    token = dict_data['token']
    print(dict_data)
    seller_id = dict_data['seller_id']
    new_commission = dict_data['new_commission']
    print(token + '======' + current_app.config['ADMIN_AUTH_TOKEN'])
    if token != current_app.config['ADMIN_AUTH_TOKEN']:
        return jsonify({'status': 'Unauthorized'}), 403
    dbc = DBConnector()
    dbc.execute_query(query='update_seller_commission', args={'seller_id': seller_id, 'new_commission':new_commission})
    return jsonify({'status': 'Ok','message': 'File successfully uploaded'}), 200

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
    
    #### To Simplify, we will only use 3 fixed months of sales ####
    pcf7 = ProcessCashFlow(country_code=dict_data['country_code'], company_id=dict_data['comp_id'], month=7)
    pcf8 = ProcessCashFlow(country_code=dict_data['country_code'], company_id=dict_data['comp_id'], month=8)
    pcf9 = ProcessCashFlow(country_code=dict_data['country_code'], company_id=dict_data['comp_id'], month=9)
    #########################################################
    
    return jsonify(
        {
        'profit': pcf7.profit + pcf8.profit + pcf9.profit,
        'status': 'Ok',
        'July':
            {
                'revenue': pcf7.month_revenue,
                'prod_costs': pcf7.month_prod_costs,
                'profit': pcf7.profit,
                'employees': pcf7.employees,
                'vat': pcf7.vat,
                'vat_value': pcf7.vat_value,
                'totalEmployeesPayment': pcf7.total_payment
            },
        'August':
            {
                'revenue': pcf8.revenue,
                'prod_costs': pcf8.month_prod_costs,
                'profit': pcf8.profit,
                'employees': pcf8.employees,
                'vat': pcf8.vat,
                'vat_value': pcf8.vat_value,
                'totalEmployeesPayment': pcf8.total_payment
            },
        'September':
            {
                'revenue': pcf9.revenue,
                'prod_costs': pcf9.month_prod_costs,
                'profit': pcf9.profit,
                'employees': pcf9.employees,
                'vat': pcf9.vat,
                'vat_value': pcf9.vat_value,
                'totalEmployeesPayment': pcf9.total_payment
            }
        }
            
    ), 200
