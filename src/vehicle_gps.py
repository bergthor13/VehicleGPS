import os
import serial
import math

from classes.ubx_configurator import UBX_Configurator
from classes.ubx_serial_parser import UBX_Serial_Parser
from classes.ui import GPS_UI

ser = serial.Serial(port="/dev/ttyS0", baudrate=38400)

ui = GPS_UI()
ui.start()

config = UBX_Configurator(ser)
parser = UBX_Serial_Parser(ser, ui)
parser.start()

#config.setMessageRate(1,7,1)
#config.setRateSettings(1000, 1, 1)

