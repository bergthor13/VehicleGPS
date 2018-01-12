"""
App
"""
from classes.gps_application import GpsApplication

import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

APP = GpsApplication()
APP.start()
