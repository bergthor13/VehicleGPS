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
from classes.ui_controller import UI_Controller
from classes.pub_sub import Subscriber
from classes.data.pvt import *
from classes.history_delegate import HistoryDelegate
from geopy.distance import vincenty


import RPi.GPIO as GPIO

'''
GPSApp
'''

class GpsApplication(Subscriber, HistoryDelegate):
    hasInternet = False
    log_file = None
    hasGPSConnection = False
    hasOBDConnection = False

    __max_history = 5
    __history = {}

    __distance = 0.0
    __start_date = None

    __engine_running = False
    __engine_start_time = None
    __engine_run_seconds = 0.0

    def get_history(self, messageType):
        return self.__history.get(messageType)

    def get_distance(self):
        return self.__distance

    def get_start_date(self):
        return self.__start_date

    def get_engine_running(self):
        return self.__engine_running
    def get_engine_start_time(self):
        return self.__engine_start_time 
    def get_engine_run_seconds(self):
        return self.__engine_run_seconds
    
    def __init__(self):
        self.initialize_gpio()
        self.initializeGpsConnection()
        self.initializeObdConnection()

        self.ui = UI_Controller(self)
        self.config = UBX_Configurator(self.serial)

        # Start the 1-second interval ticker.
        self.tick()

        filename = datetime.now().strftime("%Y-%m-%d %H%M%S.csv")
        filepath = os.path.join(constants.LOG_DIRECTORY, filename)
        self.log_file = open(filepath, 'a')

        for obdType in constants.OBDTypes.getAllTypes():
            pass #self.obd_history[0][obdType] = None

        constants.OBDTypes.getAllTypes()

    def handle1(self, channel):
        self.ui.display_settings()
    
    def handle2(self, channel):
        print("Clicked2!")

    def handle3(self, channel):
        print("Clicked3!")

    def handle4(self, channel):
        print("Clicked4!")

    def initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(17, GPIO.FALLING, callback=self.handle1, bouncetime=500)
        GPIO.add_event_detect(22, GPIO.FALLING, callback=self.handle2, bouncetime=500)
        GPIO.add_event_detect(23, GPIO.FALLING, callback=self.handle3, bouncetime=500)
        GPIO.add_event_detect(27, GPIO.FALLING, callback=self.handle4, bouncetime=500)

    def initializeGpsConnection(self):
        #print("Initializing GPS serial...")
        self.serial = self.getSerial("/dev/ttyAMA0", 38400)
        if self.serial is not None:
            self.parser = UBX_Serial_Parser(self.serial, self)
            self.parser.register("UBX-NAV-PVT", self)
            self.parser.start()
            self.hasGPSConnection = True
        else:
            print("GPS port not available")
    def update(self, message, data):
        if message == "OBD-RPM":
            history = self.get_history("UBX-NAV-PVT")
            if history is None and len(history) == 0:
                return
            last_gps_msg = history[0]
            if data is not None:
                # Engine has started.
                if self.__engine_running is False and data != 0.0:
                    if last_gps_msg is not None:
                        self.__engine_start_time = last_gps_msg.getDate()
                
                # Engine has stopped
                if self.__engine_running is True and data == 0.0:
                    if last_gps_msg is not None and last_gps_msg.getDate() is not None:
                        self.__engine_run_seconds += (last_gps_msg.getDate()-self.__engine_start_time).total_seconds()
                
                # Engine already running
                if data != 0.0 and self.__engine_start_time is None:
                    self.__engine_start_time = last_gps_msg.getDate()
                if data == 0.0:
                    self.__engine_running = False
                else:
                    self.__engine_running = True


        if message == "UBX-NAV-PVT":
            if not data.flags.gnssFixOK:
                return

            if data.fixType < 1:
                return

            #self.log_to_file(data)
            if self.__start_date is None:
                self.__start_date = datetime.now()
            gpsHistory = self.get_history("UBX-NAV-PVT")
            if gpsHistory is not None:
                self.__distance += vincenty((gpsHistory[0].lat, gpsHistory[0].lon), (data.lat, data.lon)).meters/1000

        
        msgDict = self.__history.get(message)
        if msgDict is None:
            msgDict = self.__history[message] = []
        msgDict.insert(0, data)
        if len(self.__history.get(message)) > self.__max_history:
            del self.__history.get(message)[-1]

        


    def initializeObdConnection(self):
        #print("Initializing OBD serial...")
        obdSerial = self.getSerial("/dev/ttyUSB0", 9600)
        if obdSerial is None:
            pass#print("OBD port not available")
        else:
            obdSerial.close()
            self.obd_comm = OBD_Communicator(self)

            self.obd_comm.register("OBD-RPM", self)
            self.obd_comm.register("OBD-THROTTLE_POS", self)
            self.obd_comm.register("OBD-AMBIANT_AIR_TEMP", self)
            self.obd_comm.register("OBD-ENGINE_LOAD", self)
            self.obd_comm.register("OBD-COOLANT_TEMP", self)
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
        self.config.forceColdStart()
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

    def log_to_file(self, solution):
        # TODO: check if PVT
        print("PVT")
        myPvt = PVT(solution)
        self.log_file.write(str(myPvt) + ",")
        self.log_file.write(
            str(self.oldData[constants.OBDTypes.RPM]) + "," + 
            str(self.oldData[constants.OBDTypes.ENGINE_LOAD]) + "," +
            str(self.oldData[constants.OBDTypes.COOLANT_TEMP]) + "," +
            str(self.oldData[constants.OBDTypes.AMBIANT_AIR_TEMP]) + "," +
            str(self.oldData[constants.OBDTypes.THROTTLE_POS]) + "\n"
        )
        self.log_file.flush()
        self.ui.updatePVT(myPvt)
        self.oldData['PVT'] = myPvt
