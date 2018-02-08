import threading
import struct
import binascii
from datetime import datetime
from collections import namedtuple
from classes.gps_logger import Observable

class UBX_Serial_Parser (threading.Thread, Observable):
    observers = []
    syncChar1 = b'\xB5'
    syncChar2 = b'\x62'
    def __init__(self, serial, app):
        threading.Thread.__init__(self)
        self.serial = serial
        self.app = app

    def addObserver(self, obs):
        self.observers.append(obs)

    def notifyObservers(self, data):
        for observer in self.observers:
            observer.update(data)


    def findHeader(self):
        while True:
            if self.syncChar1 == self.serial.read() and self.syncChar2 == self.serial.read():
                return

    def unpackSolution(self):
        cls = self.serial.read()
        id = self.serial.read()
        size = int.from_bytes(self.serial.read(2), byteorder="little")
        payload = self.serial.read(size)
        calcdChecksum = self.calculateChecksum(cls+id+size.to_bytes(2, byteorder="little")+payload)
        recvdChecksum = self.serial.read(2)
        if calcdChecksum == recvdChecksum:
            return self.parseSolution(cls, id, payload)

    def unpackPVT(self, solution):
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
    
    def parseSolution(self, cls, id, solution):
        if cls == b'\x01':
            if id == b'\x07':
                pvtmsg = self.unpackPVT(solution)
                return pvtmsg


    def getTupleFromMessage(self, msg, msgFormat, tClass, tVars):
        tuple = namedtuple(tClass, tVars)
        unpacked = struct.unpack(msgFormat, msg)
        return tuple._make(unpacked)
                
    def run(self):
        while True:
            self.findHeader()
            sol = self.unpackSolution()
            if sol == None:
                continue
            self.notifyObservers(sol)
            self.app.notify(sol)

    def calculateChecksum(self, message):
        ckA, ckB = 0, 0
        
        for i in range(len(message)):
            ckA += message[i]
            ckB += ckA
        
        ckA = ckA & 0xFF
        ckB = ckB & 0xFF
        
        return bytes([ckA, ckB])
