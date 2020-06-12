"""
App
"""
import os
import constants
from classes.gps_application import GpsApplication
import logging
logging.basicConfig(filename='vehiclegps.log', level=logging.DEBUG)


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Create the folders that hold the logs.
if not os.path.exists(constants.LOG_DIRECTORY):
    os.makedirs(constants.LOG_DIRECTORY)

APP = GpsApplication()
try:
    APP.start()
except:
	logging.exception('Exception')
	raise