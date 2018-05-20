import threading
import serial
import constants
import os
import obd

from os import listdir
from os.path import isfile, join

from datetime import datetime
from subprocess import check_output
from classes.ubx_configurator import UBX_Configurator
from classes.ubx_serial_parser import UBX_Serial_Parser
from classes.obd_communicator import OBD_Communicator
from classes.ui import GPS_UI
from classes.data.pvt import *
'''
GPSApp
'''
class GpsApplication:
    hasInternet = False
    oldData = {}
    logFile = None
    def __init__(self):
        self.serial = serial.Serial(port="/dev/ttyAMA0", baudrate=38400)
        self.ui = GPS_UI(self)
        self.config = UBX_Configurator(self.serial)
        self.parser = UBX_Serial_Parser(self.serial, self)
        self.obd_comm = OBD_Communicator(self)
        self.configureUBX()
        self.checkForInternet()
        self.tick()
        time = datetime.now()
        filename = time.strftime("%Y-%m-%d %H%M%S.csv")
        filepath = os.path.join(constants.LOG_DIRECTORY, filename)
        self.logFile = open(filepath, 'a')

    ### INITIALIZATION
    '''
        Starts the UI and parser threads
    '''
    def start(self):
        self.ui.start()
        self.parser.start()
        self.obd_comm.start()

    '''
        Sends commands to the u-blox chip to initialize it.
    '''
    def configureUBX(self):
        #self.config.forceColdStart()
        self.config.setMessageRate(1, 7, 1)
        self.config.setRateSettings(100, 1, 1)

    '''
        Checks if we have an IP address.
    '''
    def checkForInternet(self):
        wifi_ip = check_output(['hostname', '-I'])
        if not (wifi_ip == b'\n'):
            self.hasInternet = True
            self.uploadLogFiles()
        else:
            self.hasInternet = False
        self.ui.updateWiFi(self.hasInternet)

    '''
        Runs every second to keep the UI updated,
        Even if the GPS or OBD-II do not work.
    '''
    def tick(self):
        self.checkForInternet()
        threading.Timer(1, self.tick).start()

    def uploadLogFiles(self):
        for f in listdir(constants.LOG_DIRECTORY):
            if isfile(join(constants.LOG_DIRECTORY, f)):
                pass
                #print(f)

    ### EVENTS
    def didClickUpdateRate(self, rate):
        self.config.setRateSettings(rate, 1, 1)

    def update_coolant_temp(self, temp):
         self.ui.setEngineTemp(temp)
    def update_engine_load(self, load):
        self.ui.setEngineLoad(load)
    def update_engine_rpm(self, rpm):
        self.ui.setEngineRPM(rpm)

    def notify(self, solution):
        # TODO: check if PVT
        myPvt = PVT(solution)
        
        self.logFile.write(str(myPvt) + '\n')
        self.ui.updatePVT(myPvt)
        self.oldData['PVT'] = myPvt
