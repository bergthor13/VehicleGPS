"""
App
"""
from classes.gps_application import GPS_Application

import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

APP = GPS_Application()
APP.start()
