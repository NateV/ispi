import os
import sqlite3
import io
import speedtest_cli
from contextlib import redirect_stdout
import re
import datetime

try:
    assert os.environ['ENV_NAME'] == 'dev'
    from fixtures import sample_speedtest
except:
    pass


class SpeedTest:
    """
    Instances of this class are used to test download speeds using
    speedtest-cli.
    """

    DB_PATH = os.path.abspath('.')
    SCHEMA = {'DB_NAME': 'ispi_db.sqlite',
              'TABLE_NAME': 'TestResults',
              'COLUMNS': {'_id':'INTEGER PRIMARY KEY AUTOINCREMENT',
                          'timestamp': 'TEXT',
                          'download_speed': 'TEXT',
                          'upload_speed': 'TEXT'},}

    __possible_result_codes__ = {'HAS_NOT_RUN': '0',
                                 'ERROR': '1',
                                 'SUCCESS': '2',}
    __result_code__ = __possible_result_codes__['HAS_NOT_RUN']

    def __init__(self):
        pass

    def get_full_db_path(self):
        """
        Returns the absolute path to the database, including the database's
        name.
        """
        return os.path.join(self.DB_PATH, self.SCHEMA['DB_NAME'])

    def create_db(self):
        """
        Create the sqlite database at the path identified by
        _get_full_db_path()_
        """
        if os.path.exists(self.get_full_db_path()):
            raise "This method should not get called if the db already exists"
        print("creating db at {}".format(self.get_full_db_path()))
        conn = sqlite3.connect(self.get_full_db_path())
        cur = conn.cursor()
        table_string = "CREATE TABLE {table_name}\
                ({col_1}, {col_2}, {col_3}, {col_4})".\
                format(table_name=self.SCHEMA['TABLE_NAME'],\
                       col_1='_id INTEGER PRIMARY KEY AUTOINCREMENT',
                       col_2='timestamp TEXT',
                       col_3='download_speed TEXT',
                       col_4='upload_speed TEXT')
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
        # If the ENV_NAME isn't set OR it is set but isn't equal to 'dev'
        # we'll run the real test that hits the Internet.
        # TODO: I feel like this isn't an elegant way to do this. Hmm.
        try:
            os.environ['ENV_NAME']
            if os.environ['ENV_NAME'] == 'dev':
                self.__result_code__ = self.__possible_result_codes__['SUCCESS']
                return sample_speedtest.result
            else:
                raise "Do the real test."
        except: 
            with redirect_stdout(stdout_capturer):
                speedtest_cli.main()
            self.__result_code__ = self.__possible_result_codes__['SUCCESS']
            return stdout_capturer.getvalue()


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
                    upload_pattern.search(speedtest_results).group('upload_speed'),
                'timestamp': datetime.datetime.now().isoformat()}

    def result_code(self):
        """Returns a code for success or failure."""
        return self.__result_code__

    def save_results(self, result_dict):
        """
        Input: Result dict from get_speeds with keys 
            'timestamp'
            'download_speed',
            'upload_speed'
        """
        try: 
            self.create_db()
        except:
            print("DB already exists, I think.")
        conn = sqlite3.connect(self.get_full_db_path())
        cur = conn.cursor()
        columns_and_values = (\
                 result_dict['timestamp'], result_dict['download_speed'],\
                 result_dict['upload_speed'])
        cur.execute("INSERT INTO {}\
            ('timestamp', 'download_speed', 'upload_speed')\
            values (?, ?, ?)".\
            format(self.SCHEMA['TABLE_NAME']),\
            columns_and_values)
        conn.commit()
        conn.close()
