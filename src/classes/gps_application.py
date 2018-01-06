import serial
import threading
from subprocess import check_output
from classes.ubx_configurator import UBX_Configurator
from classes.ubx_serial_parser import UBX_Serial_Parser
from classes.ui import GPS_UI

'''
GPSApp
'''
class GPS_Application:
    pvt = None
    hasInternet = False
    def __init__(self):
        self.serial = serial.Serial(port="/dev/ttyUSB0", baudrate=38400)
        self.ui = GPS_UI(self)
        self.config = UBX_Configurator(self.serial)
        self.parser = UBX_Serial_Parser(self.serial, self)
        self.configureUBX()
        self.checkForInternet()
        self.tick()
    
    def tick(self):
        self.checkForInternet()
        threading.Timer(1.0, self.tick).start()


    def checkForInternet(self):
        wifi_ip = check_output(['hostname', '-I'])
        if not (wifi_ip == b'\n'):
            self.hasInternet = True
        else:
            self.hasInternet = False
        self.ui.updateWiFi(self.hasInternet)

    def configureUBX(self):
        self.config.setMessageRate(1, 7, 1)
        self.config.setRateSettings(100, 1, 1)

    def start(self):
        self.ui.start()
        self.parser.start()

    def updatePVT(self, pvt):
        self.pvt = pvt
        self.ui.updatePVT(pvt)

    def didClickUpdateRate(self, rate):
        self.config.setRateSettings(rate, 1, 1)
