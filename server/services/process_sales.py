import subprocess
import pandas as pd
import os
from db.db_connector import DBConnector

class ProcessSales:
    ''' Calss to process sales '''

    def __init__(self, sales: list, comp_id):
        self.sales: list = sales
        self.comp_id: int = comp_id
        self.last_3_sales:list = []

    def get_3_most_recent_sales(self) -> str:
        ''' start processing teams cashflow '''
        dbc = DBConnector()
        self.last_3_sales = dbc.execute_query(query='get_last_3_sales', args=self.comp_id)
