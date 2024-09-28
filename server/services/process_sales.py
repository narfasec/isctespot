import subprocess
import pandas as pd
import os
from db.db_connector import DBConnector

class ProcessSales:
    ''' Calss to process sales '''

    def __init__(self, sales: list, user_id):
        self.sales: list = sales
        self.revenue: float = self.get_total_revenue()
        self.user_id: int = user_id
        self.last_3_sales:list = []

    def get_3_most_recent_sales(self) -> str:
        ''' start processing teams cashflow '''
        dbc = DBConnector()
        self.last_3_sales = dbc.execute_query(query='get_last_3_sales', args=self.user_id)

    def get_total_revenue(self) -> float:
        ''' Calculate the total revenue of all sales '''
        revenue = 0
        for sale in self.sales:
            print(sale)
            revenue += float(sale['SellingPrice'])
        return round(revenue, 2)
