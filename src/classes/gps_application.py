import serial
import threading
from datetime import datetime
from subprocess import check_output
from classes.ubx_configurator import UBX_Configurator
from classes.ubx_serial_parser import UBX_Serial_Parser
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
        self.configureUBX()
        self.checkForInternet()
        self.tick()
        time = datetime.now()
        filename = time.strftime("%Y-%m-%d %H%M%S.csv")
        self.logFile = open(filename, 'a')

    ### INITIALIZATION
    '''
        Starts the UI and parser threads
    '''
    def start(self):
        self.ui.start()
        self.parser.start()

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
        else:
            self.hasInternet = False
        self.ui.updateWiFi(self.hasInternet)

    '''
        Runs every second to keep the UI updated,
        Even if the GPS or OBD-II do not work.
    '''
    def tick(self):
        self.checkForInternet()
        threading.Timer(1.0, self.tick).start()

    ### EVENTS
    def didClickUpdateRate(self, rate):
        self.config.setRateSettings(rate, 1, 1)

    def notify(self, solution):
        # TODO: check if PVT
        myPvt = PVT(solution)
        self.logFile.write(str(myPvt) + '\n')
        self.ui.updatePVT(myPvt)
        self.oldData['PVT'] = myPvt