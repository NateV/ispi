import os
import sqlite3

class SpeedTest:

    DB_PATH = os.path.abspath('.')
    SCHEMA = {'DB_NAME': 'ispi_db.sqlite',
              'TABLE_NAME': 'TestResults',
              'COLUMNS': {'_id':'INTEGER PRIMARY KEY AUTOINCREMENT',
                          'timestamp': 'TEXT',
                          'result': 'TEXT',},}

    SUCCESS_CODE = None
    __result_code__ = None

    def __init__(self):
        pass

    def get_full_db_path(self):
        return os.path.join(self.DB_PATH, self.SCHEMA['DB_NAME'])

    def create_db(self):
        if os.path.exists(self.get_full_db_path()):
            raise "This method should not get called if the db already exists"
        print("creating db at {}".format(self.get_full_db_path()))
        conn = sqlite3.connect(self.get_full_db_path())
        cur = conn.cursor()
        table_string = "CREATE TABLE {table_name}\
                ({col_1}, {col_2}, {col_3})".\
                format(table_name=self.SCHEMA['TABLE_NAME'],\
                       col_1='_id INTEGER PRIMARY KEY AUTOINCREMENT',
                       col_2='timestamp TEXT',
                       col_3='result TEXT')
        #TODO: Actually use the SCHEMA in the create_string
        
        cur.execute(table_string)
        conn.commit()
        conn.close()
            

    def run_test(self):
        pass

    def result_code(self):
        pass

    def get_result_code(self):
        pass
