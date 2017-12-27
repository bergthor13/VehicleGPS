import serial
from classes.ubx_configurator import UBX_Configurator

ser = serial.Serial(
    port="/dev/ttyS0",
    baudrate=38400
)

config = UBX_Configurator(ser)

config.setMessageRate(1,7,1)

while True:
    print(ser.readline().hex())