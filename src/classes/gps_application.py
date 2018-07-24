import threading
import serial
import constants
import os
import csv

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
    hasGPSConnection = False
    hasOBDConnection = False
    def __init__(self):
        self.initializeGpsConnection()
        self.initializeObdConnection()
        
        self.ui = GPS_UI(self)
        self.config = UBX_Configurator(self.serial)
        
        self.checkForInternet()
        self.tick()
        
        time = datetime.now()
        filename = time.strftime("%Y-%m-%d %H%M%S.csv")
        filepath = os.path.join(constants.LOG_DIRECTORY, filename)
        self.logFile = open(filepath, 'a')
        for obdType in constants.OBDTypes.getAllTypes():
            self.oldData[obdType] = None

        constants.OBDTypes.getAllTypes()

    def initializeGpsConnection(self):
        #print("Initializing GPS serial...")
        self.serial = self.getSerial("/dev/ttyAMA0", 38400)
        if self.serial is not None:
            self.parser = UBX_Serial_Parser(self.serial, self)
            self.parser.start()
            self.hasGPSConnection = True
        else:
            print("GPS port not available")

    def initializeObdConnection(self):
        #print("Initializing OBD serial...")
        obdSerial = self.getSerial("/dev/ttyUSB0", 9600)
        if obdSerial is None:
            pass#print("OBD port not available")
        else:
            obdSerial.close()
            self.obd_comm = OBD_Communicator(self)
            self.obd_comm.start()
            self.hasOBDConnection = True


    ### INITIALIZATION
    '''
        Starts the UI and parser threads
    '''
    def start(self):
        self.ui.start()
        if self.hasGPSConnection:
            self.configureUBX()

    def getSerial(self, port, baud):
        try:
           return serial.Serial(port=port, baudrate=baud)
        except:
           return None

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
            #self.uploadLogFiles()
        else:
            self.hasInternet = False
        self.ui.updateWiFi(self.hasInternet)

    '''
        Runs every second to keep the UI updated,
        Even if the GPS or OBD-II do not work.
    '''
    def tick(self):
        self.checkForInternet()
        if not self.hasGPSConnection:
            self.initializeGpsConnection()
        if not self.hasOBDConnection:
            self.initializeObdConnection()
        
        threading.Timer(1, self.tick).start()

    def uploadLogFiles(self):
        for f in listdir(constants.LOG_DIRECTORY):
            filePath = join(constants.LOG_DIRECTORY, f)
            if isfile(filePath):
                pass
                # with open(filePath, 'r') as originalFile:
                #     print(originalFile.readlines())

    ### EVENTS
    def didClickUpdateRate(self, rate):
        self.config.setRateSettings(rate, 1, 1)

    def update_metric(self, metric, value):
        self.ui.setMetric(metric, value)
        self.oldData[metric] = value

    def notify(self, solution):
        # TODO: check if PVT
        myPvt = PVT(solution)
        self.logFile.write(str(myPvt) + "\n")
        self.logFile.write("$OBD," + str(myPvt.getDate().isoformat() + ","))
        self.logFile.write(
            str(self.oldData[constants.OBDTypes.RPM]) + "," + 
            str(self.oldData[constants.OBDTypes.ENGINE_LOAD]) + "," +
            str(self.oldData[constants.OBDTypes.COOLANT_TEMP]) + "," +
            str(self.oldData[constants.OBDTypes.AMBIANT_AIR_TEMP]) + "," +
            str(self.oldData[constants.OBDTypes.THROTTLE_POS]) + "\n"
        )
        self.logFile.flush()
        self.ui.updatePVT(myPvt)
        self.oldData['PVT'] = myPvt
