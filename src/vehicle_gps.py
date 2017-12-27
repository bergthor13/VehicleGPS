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
config.setRateSettings(1000, 1, 1)

def findHeader():
    while True:
        if syncChar1 == ser.read() and syncChar2 == ser.read():
            return

def unpackSolution():
    cls = ser.read()
    id = ser.read()
    size = int.from_bytes(ser.read(2), byteorder="little")
    pvt = namedtuple("PVT", "iTOW year month day hour min sec valid tAcc nano fixType flags flags2 numSv lon lat height hMSL hAcc vAcc velN velE velD gSpeed headMot sAcc headAcc pDop reserved1_1 reserved1_2 reserved1_3 reserved1_4 reserved1_5 reserved1_6 headVeh magDec magAcc")
    sol = parseSolution(cls, id, ser.read(size))
    if sol == None:
      return  
    return pvt._make(sol)

def parseSolution(cls, id, solution):
    if cls == b'\x01':
        if id == b'\x07':
            return struct.unpack("LHBBBBBcLlBccBllllLLlllllLLHBBBBBBlhH", solution)

while True:
    findHeader()
    pvt = unpackSolution()
    if pvt == None:
        continue
    print(datetime(pvt.year, pvt.month, pvt.day, pvt.hour, pvt.min, pvt.sec))

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
config.setRateSettings(1000, 1, 1)

def findHeader():
    while True:
        if syncChar1 == ser.read() and syncChar2 == ser.read():
            return

def unpackSolution():
    cls = ser.read()
    id = ser.read()
    size = int.from_bytes(ser.read(2), byteorder="little")
    pvt = namedtuple("PVT", "iTOW year month day hour min sec valid tAcc nano fixType flags flags2 numSv lon lat height hMSL hAcc vAcc velN velE velD gSpeed headMot sAcc headAcc pDop reserved1_1 reserved1_2 reserved1_3 reserved1_4 reserved1_5 reserved1_6 headVeh magDec magAcc")
    sol = parseSolution(cls, id, ser.read(size))
    if sol == None:
      return  
    return pvt._make(sol)

def parseSolution(cls, id, solution):
    if cls == b'\x01':
        if id == b'\x07':
            return struct.unpack("LHBBBBBcLlBccBllllLLlllllLLHBBBBBBlhH", solution)

while True:
    findHeader()
    pvt = unpackSolution()
    if pvt == None:
        continue
    print(datetime(pvt.year, pvt.month, pvt.day, pvt.hour, pvt.min, pvt.sec))