import os
import sqlite3
import io
import speedtest_cli
from contextlib import redirect_stdout
import re

try:
    assert os.environ['ENV_NAME'] == 'dev'
    from fixtures import sample_speedtest
except:
    pass


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
    

    def run_speedtest(self):
        """
        Runs the main method of speedtest-cli.py, 
        captures and returns the stdout output in a StringIO object.
        """
        #TODO: Handle errors by speedtest_cli.  i.e. if output has "Cancelling"
        stdout_capturer = io.StringIO()
        if os.environ['ENV_NAME'] != 'dev':
            with redirect_stdout(stdout_capturer):
                speedtest_cli.main()
            return stdout_capturer.getvalue()
        else:
            return sample_speedtest.result


    def get_speeds(self, speedtest_results):
        """
        Input: results from speedtest as a string,
        Output: A Dict with keys "download_speed" and "upload_speed"
        """
        download_pattern = re.compile("Download: (?P<download_speed>[0-9\.]*)")
        upload_pattern = re.compile("Upload: (?P<upload_speed>[0-9\.]*)")
        return {'download_speed':
                    download_pattern.search(speedtest_results).group('download_speed'),
                'upload_speed':
                    upload_pattern.search(speedtest_results).group('upload_speed')}

    def run_test(self):
        pass

    def result_code(self):
        pass

    def get_result_code(self):
        pass
