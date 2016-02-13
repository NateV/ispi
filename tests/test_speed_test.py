from ispi import SpeedTest
import os
import pytest
import sqlite3
import re

class TestSpeedTest:
    
    def setup_method(self, method):
        self.tester = SpeedTest()

    def teardown_method(self, method):
        if os.path.exists(os.path.join(self.tester.DB_PATH,\
                self.tester.SCHEMA['DB_NAME'])):
            os.remove(os.path.join(self.tester.DB_PATH,\
                self.tester.SCHEMA['DB_NAME']))

    def test_init(self):
        tester = SpeedTest()
        assert isinstance(tester, SpeedTest)

    def test_database_schema(self):
        assert self.tester.DB_PATH == os.path.abspath('.')
        assert self.tester.SCHEMA['DB_NAME'] == 'ispi_db.sqlite'
        assert self.tester.SCHEMA['TABLE_NAME'] == 'TestResults'
        assert self.tester.SCHEMA['COLUMNS'] == {
            '_id':'INTEGER PRIMARY KEY AUTOINCREMENT',
            'timestamp': 'TEXT',
            'download_speed': 'TEXT',
            'upload_speed': 'TEXT',
            }

    def test_get_result_code(self):
        """Before running test, it returns an incomplete code."""
        assert self.tester.result_code() ==\
            self.tester.__possible_result_codes__['HAS_NOT_RUN']
        #TODO: Test value AFTER running speedtest

    def test_create_db_correctly(self):
        self.tester.create_db()
        conn = sqlite3.connect(self.tester.get_full_db_path())
        cur = conn.cursor()
        cur.execute('PRAGMA table_info("TestResults")')
        col_names = [col[1]  for col in cur.fetchall()]
        for col_name in col_names:
            assert col_name in self.tester.SCHEMA['COLUMNS'].keys()

    def test_get_full_db_path(self):
        assert self.tester.get_full_db_path() \
                == os.path.join(self.tester.DB_PATH, self.tester.SCHEMA['DB_NAME'])


    def test_creates_db_if_not_exists(self):
        assert not os.path.exists(os.path.join(self.tester.DB_PATH,
                        self.tester.SCHEMA['DB_NAME']))
        self.tester.create_db()
        assert os.path.exists(os.path.join(self.tester.DB_PATH,
                        self.tester.SCHEMA['DB_NAME']))

    def test_does_not_create_db_if_exists_already(self):
        assert not os.path.exists(os.path.join(self.tester.DB_PATH,
                        self.tester.SCHEMA['DB_NAME']))
        self.tester.create_db()
        assert pytest.raises(Exception)

    def test_run_speedtest(self):
        """
        When I run the speedtest, the results include a download speed.
        """
        results = self.tester.run_speedtest()
        pattern = re.compile("Download: (?P<download_speed>[0-9\.]*)")
        assert pattern.search(results)

    def test_get_speeds(self):
        """
        I pass results of a speedtest to get_speeds, I receive a dict with
        download and upload speeds.
        """
        speed_dict = self.tester.get_speeds(self.tester.run_speedtest())
        #TODO: I wonder if its bad practice to have  unit test that takes
        #       another function's output as its input.  I mean, its no 
        #       longer isolated, but how can you avoid doing that?
        assert isinstance(speed_dict, dict)
        assert 'download_speed' in speed_dict
        assert 'upload_speed' in speed_dict

    def test_save_results(self):
        """
        I save results in the database.
        """
        self.tester.create_db()
        result_string = self.tester.run_speedtest() 
        result_dict = self.tester.get_speeds(result_string)
        self.tester.save_results(result_dict)
        conn = sqlite3.connect(self.tester.get_full_db_path())
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT * from {}'.format(self.tester.SCHEMA['TABLE_NAME']))
        row = cur.fetchone()
        assert os.environ['ENV_NAME'] == 'dev'
        assert row['download_speed'] == result_dict['download_speed']
        assert row['upload_speed'] == result_dict['upload_speed']
