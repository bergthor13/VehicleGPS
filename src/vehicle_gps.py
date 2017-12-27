import serial
import struct
from datetime import datetime
from collections import namedtuple
from classes.ubx_configurator import UBX_Configurator


syncChar1 = b'\xB5'
syncChar2 = b'\x62'

ser = serial.Serial(
    port="/dev/ttyS0",
    baudrate=38400
)

config = UBX_Configurator(ser)

#config.setMessageRate(1,7,1)

def findHeader():
    while True:
        if syncChar1 == ser.read() and syncChar2 == ser.read():
            return

def parseSolution(cls, id, solution):
    return {
        b'\x01': {
            b'\x07': struct.unpack("LHBBBBBcLlBccBllllLLlllllLLHBBBBBBlhH", solution)
        }.get(id)
    }.get(cls)

while True:
    findHeader()
    cls = ser.read()
    id = ser.read()
    size = int.from_bytes(ser.read(2), byteorder="little")
    pvt = namedtuple("PVT", "iTOW year month day hour min sec valid tAcc nano fixType flags flags2 numSv lon lat height hMSL hAcc vAcc velN velE velD gSpeed headMot sAcc headAcc pDop reserved1_1 reserved1_2 reserved1_3 reserved1_4 reserved1_5 reserved1_6 headVeh magDec magAcc")
    pvt = pvt._make(parseSolution(cls, id, ser.read(size)))
    print(pvt.lat, pvt.lon)
    print(datetime(pvt.year, pvt.month, pvt.day, pvt.hour, pvt.min, pvt.sec))
