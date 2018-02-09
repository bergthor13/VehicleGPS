from datetime import datetime

class PVT():
    iTOW = None
    year = None
    month = None
    day = None
    hour = None
    min = None
    sec = None
    valid = None
    tAcc = None
    nano = None
    fixType = None
    flags = None
    flags2 = None
    numSv = None
    lon = None
    lat = None
    height = None
    hMSL = None
    hAcc = None
    vAcc = None
    velN = None
    velE = None
    velD = None
    gSpeed = None
    headMot = None
    sAcc = None
    headAcc = None
    pDop = None
    headVeh = None
    magDec = None
    magAcc = None

    def __init__(self, pvt):
        self.iTOW = pvt.iTOW
        self.year = pvt.year
        self.month = pvt.month
        self.day = pvt.day
        self.hour = pvt.hour
        self.min = pvt.min
        self.sec = pvt.sec
        self.valid = PVT_valid(pvt.valid)
        self.tAcc = pvt.tAcc
        if pvt.nano < 0:
            self.nano = 1000000000+pvt.nano
        else:
            self.nano = pvt.nano

        self.fixType = pvt.fixType
        self.flags = PVT_flags(pvt.flags)
        self.flags2 = PVT_flags2(pvt.flags2)
        self.numSv = pvt.numSv
        self.lon = pvt.lon/10000000
        self.lat = pvt.lat/10000000
        self.height = pvt.height
        self.hMSL = pvt.hMSL
        self.hAcc = pvt.hAcc
        self.vAcc = pvt.vAcc
        self.velN = pvt.velN
        self.velE = pvt.velE
        self.velD = pvt.velD
        self.gSpeed = pvt.gSpeed*3.6/1000
        self.headMot = pvt.headMot
        self.sAcc = pvt.sAcc
        self.headAcc = pvt.headAcc
        self.pDop = pvt.pDop
        self.headVeh = pvt.headVeh
        self.magDec = pvt.magDec
        self.magAcc = pvt.magAcc

    def getDate(self):
        checkedNano = round(self.nano/1000)
        if checkedNano < 0:
            checkedNano = 0
        elif checkedNano > 999999:
            checkedNano = 999999
        return datetime(self.year, self.month, self.day, self.hour, self.min, self.sec, checkedNano)
    
    def __str__(self):
        return str(self.iTOW) + ", " + str(self.year) + ", " + str(self.month) + ", " + str(self.day) + ", " + str(self.hour) + ", " + str(self.min) + ", " + str(self.sec) + ", " + ", " + str(self.tAcc) + ", " + str(self.nano) + ", " + str(self.fixType) + ", " + ", " + str(self.numSv) + ", " + str(self.lon) + ", " + str(self.lat) + ", " + str(self.height) + ", " + str(self.hMSL) + ", " + str(self.hAcc) + ", " + str(self.vAcc) + ", " + str(self.velN) + ", " + str(self.velE) + ", " + str(self.velD) + ", " + str(self.gSpeed) + ", " + str(self.headMot) + ", " + str(self.sAcc) + ", " + str(self.headAcc) + ", " + str(self.pDop) + ", " + str(self.headVeh) + ", " + str(self.magDec) + ", " + str(self.magAcc)

class PVT_valid:
    validDate = None
    validTime = None
    fullyResolved = None
    validMag = None

    def getBitFromByte(self, byte, index):
        return not((byte[0] & (1 << index)) == 0)

    def __init__(self, valid):
        self.validDate     = self.getBitFromByte(valid, 0)
        self.validTime     = self.getBitFromByte(valid, 1)
        self.fullyResolved = self.getBitFromByte(valid, 2)
        self.validMag      = self.getBitFromByte(valid, 3)

class PVT_flags:
    gnssFixOK    = None
    diffSoln     = None
    psmState     = None
    headVehValid = None
    carrSoln     = None

    def getBitFromByte(self, byte, index):
        return not((byte[0] & (1 << index)) == 0)

    def getBitsFromByte(self, byte, start, end):
        maskSize = (end-start)+c1
        return byte[0] >> start

    def __init__(self, valid):
        self.gnssFixOK     = self.getBitFromByte(valid, 0)
        self.diffSoln      = self.getBitFromByte(valid, 1)
        #self.psmState      = self.getBitsFromByte(valid, 2, 4)
        self.headVehValid  = self.getBitFromByte(valid, 5)
        #self.carrSoln      = self.getBitsFromByte(valid, 6, 7)

class PVT_flags2:
    def __init__(self, flags2):
        pass
