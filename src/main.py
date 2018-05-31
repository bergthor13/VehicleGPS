"""
App
"""
import os
from classes.gps_application import GpsApplication
import constants

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Create the folders that hold the logs.
if not os.path.exists(constants.LOG_DIRECTORY):
    os.makedirs(constants.LOG_DIRECTORY)

APP = GpsApplication()
APP.start()
