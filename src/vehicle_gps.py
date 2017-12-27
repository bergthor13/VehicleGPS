import os
print("PWD:" + os.getcwd())
import serial
import math
from tkinter import *
from classes.ubx_configurator import UBX_Configurator
from classes.ubx_serial_parser import UBX_Serial_Parser

ser = serial.Serial(port="/dev/ttyS0", baudrate=38400)

config = UBX_Configurator(ser)
parser = UBX_Serial_Parser(ser)
parser.start()

config.setMessageRate(1,7,1)
config.setRateSettings(1000, 1, 1)

root = Tk()
lblTime = Label(root, text="Time")
lblTime.pack()
root.mainloop()