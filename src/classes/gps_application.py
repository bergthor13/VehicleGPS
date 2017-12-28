import serial

from classes.ubx_configurator import UBX_Configurator
from classes.ubx_serial_parser import UBX_Serial_Parser
from classes.ui import GPS_UI

class GPS_Application:
    pvt = None
    def __init__(self):
        self.serial = serial.Serial(port="/dev/ttyS0", baudrate=38400)
        self.ui = GPS_UI(self)
        self.config = UBX_Configurator(self.serial)
        self.parser = UBX_Serial_Parser(self.serial, self)
        #self.configureUBX()
    
    def configureUBX(self):
        self.config.setMessageRate(1,7,1)
        self.config.setRateSettings(1000, 1, 1)
    
    def start(self):
        self.ui.start()
        self.parser.start()
        
    def updateSpeed(self, spd):
        self.ui.updateSpeed(spd)
        
    def didClickUpdateRate(self, rate):
        self.config.setRateSettings(rate, 1, 1)
