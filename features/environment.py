from ispi import SpeedTest
import os

def before_feature(context, feature):
    #Make sure database doesn't exist already.
    st = SpeedTest()
    if os.path.exists(st.get_full_db_path()):
        os.remove(st.get_full_db_path())
