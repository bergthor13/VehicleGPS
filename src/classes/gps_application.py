import time
import threading
import serial
import constants
import os
import sys
import os.path
import csv
import RPi.GPIO as GPIO

from os import listdir
from os.path import isfile, join

from datetime import datetime, timedelta
from subprocess import check_output, Popen, CalledProcessError, PIPE, STDOUT
from classes.ubx_configurator import UBX_Configurator
from classes.ubx_serial_parser import UBX_Serial_Parser
from classes.obd_communicator import OBD_Communicator
from classes.ui_controller import UI_Controller
from classes.pub_sub import Subscriber, Publisher
from classes.data.pvt import *
from classes.history_delegate import HistoryDelegate
from geopy.distance import vincenty
import logging


'''
GPSApp
'''

class GpsApplication(Subscriber, Publisher, HistoryDelegate):
    hasInternet = False
    log_file = None
    hasGPSConnection = False
    hasOBDConnection = False
    parser = None
    obd_comm = None

    __time_since_start = None
    __max_history = 20
    __history = {}

    __distance = 0.0 # In kilometers
    __start_date = None

    __engine_running = False
    __engine_start_time = None
    __engine_run_seconds = 0.0
    __brightness = 100
    __brightness_pin = None

    __log_speed_threshold = 0.5

    def get_history(self, messageType):
        return self.__history.get(messageType)

    def get_distance(self):
        return self.__distance

    def get_start_date(self):
        return self.__start_date

    def get_time_since_start(self):
        return self.__time_since_start

    def get_engine_running(self):
        return self.__engine_running

    def get_engine_start_time(self):
        return self.__engine_start_time 

    def get_engine_run_seconds(self):
        return self.__engine_run_seconds

    def set_display_brightness(self, value):
        pass
        #if 1 <= value and value <= 100:
        #    self.__brightness_pin.ChangeDutyCycle(value)
    
    def __init__(self):
        self.__time_since_start = time.time()
        Publisher.__init__(self, ["UBX-NAV-PVT"])
        self.initialize_gpio()
        self.initializeGpsConnection()
        self.config = UBX_Configurator(self.serial)
        #self.config.forceColdStart()

        self.initializeObdConnection()
        if not os.path.isfile(constants.COLOR_MODE_FILE):
            with open(constants.COLOR_MODE_FILE, 'w+') as color_mode:
                color_mode.write("light")
        
        self.ui = UI_Controller(self)

        # Start the 1-second interval ticker.
        self.tick()

        filepath = self.get_file_name_from_date(datetime.now())
        self.log_file = open(filepath, 'a')

        for obdType in constants.OBDTypes.getAllTypes():
            pass #self.obd_history[0][obdType] = None

        constants.OBDTypes.getAllTypes()

    def handle1(self, channel):
        self.ui.display_settings(None)
    
    def handle2(self, channel):
        self.ui.change_color()

    def upload_log_files(self, channel):
        self.ui.upload_alert_view.set_alert_title("New Log File")
        self.ui.upload_alert_view.set_alert_message("Now writing to a new log file.")
        self.ui.display_upload_alert()
        
        filepath = ""
        if self.__start_date is None:
            self.__time_since_start = time.time()
            filepath = self.get_file_name_from_date(datetime.now())
        else:
            currDate = self.get_history("UBX-NAV-PVT")[0].getDate()
            self.__start_date = currDate
            filepath = self.get_file_name_from_date(currDate)
        self.log_file.close()
        self.log_file = open(filepath, 'a')
        self.__distance = 0.0
        self.__engine_start_time = time.time()
        self.__engine_run_seconds = 0.0
    
        time.sleep(1.5)
        self.ui.hide_upload_alert()

    def get_file_name_from_date(self, date):
        filename = date.strftime("%Y-%m-%d %H%M%S.csv")
        filepath = os.path.join(constants.LOG_DIRECTORY, filename)
        return filepath

    def initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   
        GPIO.add_event_detect(17, GPIO.FALLING, callback=self.handle1, bouncetime=500)
        GPIO.add_event_detect(22, GPIO.FALLING, callback=self.handle2, bouncetime=500)
        GPIO.add_event_detect(27, GPIO.FALLING, callback=self.upload_log_files, bouncetime=500)

    def initializeGpsConnection(self):
        self.serial = self.getSerial(constants.GPS_SERIAL_PORT, constants.GPS_BAUD_RATE)
        if self.serial is not None:
            self.parser = UBX_Serial_Parser(self.serial, self)
            self.parser.register("UBX-NAV-PVT", self)
            self.parser.start()
            self.hasGPSConnection = True
        else:
            print("GPS port not available")

    def update(self, message, data):

        # Save the message to memory.
        msgDict = self.__history.get(message)
        if msgDict is None:
            msgDict = self.__history[message] = []
        msgDict.insert(0, data)
        if len(self.__history.get(message)) > self.__max_history:
            del self.__history.get(message)[-1]

        # Let subscribers know there is new data.
        self.dispatch(message, data)

        if message == "OBD-RPM":
            if data is not None:
                # Engine has started.
                if self.__engine_running is False and data != 0.0:
                        self.__engine_start_time = time.time()
                
                # Engine has stopped
                if self.__engine_running is True and data == 0.0:
                        self.__engine_run_seconds += time.time() - self.__engine_start_time
                
                # Engine already running
                if data != 0.0 and self.__engine_start_time is None:
                    self.__engine_start_time = time.time()

                # Update the boolean
                if data == 0.0:
                    self.__engine_running = False
                else:
                    self.__engine_running = True


        if message == "UBX-NAV-PVT":
            self.log_to_file(data)
            if data.valid is None:
                return
            if self.__start_date is None and data.valid.validDate and data.valid.validTime:
                # Finally got an accurate date and time.
                since_start = timedelta(seconds=(time.time()-self.__time_since_start))

                self.__start_date = data.getDate() - since_start
                newFilePath = self.get_file_name_from_date(self.__start_date)
                if self.log_file is not None:
                    self.log_file.close()
                    os.rename(self.log_file.name, newFilePath)
                    self.log_file = open(newFilePath, 'a')


            if not data.flags.gnssFixOK:
                return

            if data.fixType < 1:
                return
            
            gpsHistory = self.get_history("UBX-NAV-PVT")

            if gpsHistory is not None and len(gpsHistory) > 1:
                if gpsHistory[0].gSpeed > self.__log_speed_threshold:
                    
                    if not gpsHistory[1].flags.gnssFixOK: return
                    if gpsHistory[1].fixType < 1: return
                    if gpsHistory[1].gSpeed > 200: return
                    self.__distance += vincenty((gpsHistory[1].lat, gpsHistory[1].lon), (data.lat, data.lon)).meters/1000

    def initializeObdConnection(self):
        obdSerial = self.getSerial(constants.OBD_SERIAL_PORT, constants.OBD_BAUD_RATE)
        if obdSerial is not None:
            obdSerial.close()
            self.obd_comm = OBD_Communicator(self)

            self.obd_comm.register("OBD-RPM", self)
            self.obd_comm.register("OBD-THROTTLE_POS", self)
            self.obd_comm.register("OBD-AMBIANT_AIR_TEMP", self, interval=5)
            self.obd_comm.register("OBD-ENGINE_LOAD", self)
            self.obd_comm.register("OBD-COOLANT_TEMP", self, interval=1)
            self.obd_comm.register("OBD-SPEED", self)
            self.obd_comm.start()
            self.hasOBDConnection = True


    ### INITIALIZATION
    '''
        Starts the UI and parser threads
    '''
    def start(self):
        with open(constants.COLOR_MODE_FILE, 'r') as color_mode:
            if color_mode.read() == "dark":
                self.ui.is_night = True
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
        pass
        #self.config.forceColdStart()
        #self.config.setMessageRate(1, 7, 1)
        #self.config.setRateSettings(100, 1, 1)

    '''
        Checks if we have an IP address.
    '''
    def checkForInternet(self):
        ps = Popen(['iwconfig'], stdout=PIPE, stderr=STDOUT)
        try:
            output = check_output(('grep', 'Access Point: Not-Associated'), stdin=ps.stdout)
            self.hasInternet = False
        except CalledProcessError:
            self.hasInternet = True
            
        finally:
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

    ### EVENTS
    def didClickUpdateRate(self, rate):
        self.config.setRateSettings(rate, 1, 1)

    def generate_log_item(self, message):
        history = self.get_history(message)
        if history is None:
            return "None"
        try:
            return str(history[0])
        except IndexError:
            return "None"
        return

    def log_to_file(self, solution):
        log_line = str(solution) + ","

        log_line += self.generate_log_item("OBD-RPM") + ","
        log_line += self.generate_log_item("OBD-ENGINE_LOAD") + ","
        log_line += self.generate_log_item("OBD-COOLANT_TEMP") + ","
        log_line += self.generate_log_item("OBD-AMBIANT_AIR_TEMP") + ","
        log_line += self.generate_log_item("OBD-THROTTLE_POS") + "\n"

        if self.log_file is None:
            return
        if not self.log_file.closed:
            self.log_file.write(log_line)
            self.log_file.flush()
