import threading
import struct
from datetime import datetime
from collections import namedtuple

class UBX_Serial_Parser (threading.Thread):
    syncChar1 = b'\xB5'
    syncChar2 = b'\x62'
    def __init__(self, serial):
        threading.Thread.__init__(self)
        self.serial = serial
        print("parser init")
        
    def findHeader(self):
        while True:
            if self.syncChar1 == self.serial.read() and self.syncChar2 == self.serial.read():
                return

    def unpackSolution(self):
        cls = self.serial.read()
        id = self.serial.read()
        size = int.from_bytes(self.serial.read(2), byteorder="little")
        return self.parseSolution(cls, id, self.serial.read(size))
    
    def parseSolution(self, cls, id, solution):
        if cls == b'\x01':
            if id == b'\x07':
                return self.getTupleFromMessage(
                    solution,
                    "LHBBBBBcLlBccBllllLLlllllLLHBBBBBBlhH",
                    "PVT",
                    ("iTOW year month day hour min sec valid tAcc nano "
                    "fixType flags flags2 numSv lon lat height hMSL hAcc "
                    "vAcc velN velE velD gSpeed headMot sAcc headAcc pDop "
                    "reserved1_1 reserved1_2 reserved1_3 reserved1_4 reserved1_5 "
                    "reserved1_6 headVeh magDec magAcc")
                )

    def getTupleFromMessage(self, msg, msgFormat, tClass, tVars):
        tuple = namedtuple(tClass, tVars)
        unpacked = struct.unpack(msgFormat, msg)
        return tuple._make(unpacked)
                
    def run(self):
        print("Starting...")
        while True:
            self.findHeader()
            sol = self.unpackSolution()
            if sol == None:
                continue
            print(datetime(sol.year, sol.month, sol.day, sol.hour, sol.min, sol.sec), round(sol.gSpeed*3.6/1000, 2))

