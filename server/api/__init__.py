from flask_cors import CORS
from flask import Flask
from api.auth.routes import auth
from api.company.routes import company
from api.sales.routes import sales
from api.clients.routes import clients

def create_app(config_file='settings.py'):
    ''' we add template from folder templates inside app directory '''
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    CORS(auth, origins=["*"])
    CORS(clients, origins=["*"])
    CORS(sales, origins=["*"])
    CORS(company, origins=["*"])
    app.register_blueprint(auth)
    app.register_blueprint(company)
    app.register_blueprint(sales)
    app.register_blueprint(clients)

    return app
