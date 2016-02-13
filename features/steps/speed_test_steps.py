from ispi import SpeedTest
import sqlite3
import os

@given(u'I do a speed test that completes successfully')
def step_impl(context):
    context.test = SpeedTest()
    context.results = context.test.get_speeds(context.test.run_speedtest())
    assert 'download_speed' in context.results
    assert context.test.result_code() ==\
        context.test.__possible_result_codes__['SUCCESS']

@given(u'I save the information to a local database')
def step_impl(context):
    context.test.save_results(context.results)
    assert os.path.exists(context.test.get_full_db_path())

@then(u'I can retrieve the information from the database')
def step_impl(context):
    conn = sqlite3.connect(context.test.get_full_db_path())
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    select_string = "SELECT * from {}".format(context.test.SCHEMA['TABLE_NAME'])
    cur.execute(select_string)
    #conn.commit()
    #conn.close()
    rows = cur.fetchall()
    print(rows[0])
    assert len(rows) == 1, "Rowcount should be 1, but is{}".\
        format(len(rows))
    for col_name in rows[0].keys():
        assert col_name in context.test.SCHEMA['COLUMNS'].keys(),\
            "{col_name} not in {keys}".format(col_name=col_name,\
            keys=context.test.SCHEMA['COLUMNS'].keys())
    # TODO: assert that each entry of the row is the type its supposed to be.


