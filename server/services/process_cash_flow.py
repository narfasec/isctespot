import subprocess
import pandas as pd
import os
from db.db_connector import DBConnector

class ProcessCashFlow:
    ''' Calss to process company cashflow '''

    def __init__(self, company_id: int, country_code: str, month: int):
        self.company_id: int = company_id
        self.country_code: str = country_code
        self.month: int = month
        self.month_revenue:float = 0.0
        self.month_prod_costs: float = 0.0
        self.revenue: float = 0
        self.vat: int = 0
        self.vat_value = 0
        self.invoice: float = 0
        self.employees: list = []
        self.profit: float = 0.0
        self.total_payment: float = 0.0
        self.prod_cost: float = 0.0

        self.start()

    def start(self) -> str:
        ''' start processing teams cashflow '''
        self.update_company_revenue()
        self.get_company_revenue()
        self.get_monthly_costs_and_revenue()
        self.get_sales_and_commission_by_employee()
        self.get_VAT()
        self.calculate()

    def update_company_revenue(self):
        ''' update company revenue'''
        dbc = DBConnector()
        results = dbc.execute_query(query='update_company_revenue', args=self.company_id)
        if results is True:
            print("Products updated successfully.")
        else:
            self.is_updated = False

    def get_monthly_costs_and_revenue(self):
        ''' Get monthly production costs and total sales revenue '''
        dbc = DBConnector()
        results = dbc.execute_query(query='get_costs_sales_month', args={'comp_id': self.company_id, 'month': self.month})
        self.month_revenue = float(results['TotalSellingPrice'])
        self.month_prod_costs = float(results['TotalFactoryPrice'])

    def get_company_revenue(self):
        """Get total sales for a specific company by summing the prices."""
        dbc = DBConnector()
        self.revenue = dbc.execute_query(query='get_company_revenue', args=self.company_id)

    def get_sales_and_commission_by_employee(self):
        """ Get total sales and commission for each employee in a specific company. """

        dbc = DBConnector()
        self.employees = dbc.execute_query(query='get_employees_return', args={'comp_id': self.company_id, 'month': self.month})

    def get_VAT(self):
        ''' Execute GOV provided script '''
        try:
            abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "vat.py"))
            result = subprocess.run(
                ['python', abs_path, self.country_code],
                capture_output=True, text=True, check=True
            )
            print(f'Stdout: {result.stdout}')
            output_lines = result.stdout.strip().splitlines()
            vat_value = int(output_lines[-1].strip())
            self.vat = vat_value
            
            if result.stderr:
                print(f"Error: {result.stderr}")

        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
    
    def calculate(self):
        ''' Calculate cash flow '''
        total_payment: float = 0.0
        for employee in self.employees:
            self.total_payment += total_payment + float(employee['TotalCommission'])
        self.vat_value = self.month_revenue * (self.vat*0.01)
        self.profit = round((self.month_revenue - self.vat_value - total_payment - self.month_prod_costs), 2)
