import os
import pandas as pd
from db.db_connector import DBConnector

class ProcessFile:
    ''' Calss to process uploaded file '''

    def __init__(self, file, comp_id):
        self.comp_id = comp_id
        self.file = file
        self.dir = os.path.join(os.path.dirname(__file__), 'files')
        self.status = False
        self.file_path = self.save_file()
        self.update_products_from_file(self.file_path)

    def save_file(self) -> str:
        ''' save file in system '''
        filename = self.file.filename
        comp_folder = os.path.join(self.dir, str(self.comp_id))
        os.makedirs(comp_folder, exist_ok=True)
        print(comp_folder)

        # Save the file
        file_path = os.path.join(comp_folder, filename)
        try:
            self.file.save(file_path)
            return file_path
        except Exception as error:
            print(error)
            raise

    def update_products_from_file(self, file_path):
        ''' upload database according to the escell data '''
        # Load the Excel or CSV file into a DataFrame
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

        # Establish a connection with the database (assuming mariadb)
        dbc = DBConnector()
        results = dbc.execute_query(query='update_products_by_comp_id', args={'file':df, 'comp_id':self.comp_id})
        if results is True:
            self.is_updated = True
            print("Products updated successfully.")
        else:
            self.is_updated = False
