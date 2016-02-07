from ispi import SpeedTest
import sqlite3
import os

@given(u'I do a speed test that completes successfully')
def step_impl(context):
    context.test = SpeedTest()
    context.results = context.test.run_test()
    assert context.test.get_result_code == context.test.SUCCESS_CODE



@given(u'I save the information to a local database')
def step_impl(context):
    context.test.save()
    assert os.path.exists(os.path.join())

@then(u'I can retrieve the information from the database')
def step_impl(context):
    conn = sqlite3.connect(context.test.DB_NAME)
    cur = con.cursor()
    c.execute("SELECT * from ?",context.test.TBL_NAME)
    conn.commit()
    conn.close()
    assert cur.rowcount == 1
    a_row = cur.fetch_one()
    assert a_row.keys() == context.test.TABLE_COLUMNS
    # TODO: assert that each entry of the row is the type its supposed to be.


