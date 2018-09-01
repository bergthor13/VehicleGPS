from datetime import datetime, timedelta

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
        self.hMSL = pvt.hMSL/1000.0
        self.hAcc = pvt.hAcc/1000.0
        self.vAcc = pvt.vAcc/1000.0
        self.velN = pvt.velN
        self.velE = pvt.velE
        self.velD = pvt.velD
        self.gSpeed = pvt.gSpeed*3.6/1000
        self.headMot = pvt.headMot
        self.sAcc = pvt.sAcc
        self.headAcc = pvt.headAcc
        self.pDop = pvt.pDop/100.0
        self.headVeh = pvt.headVeh
        self.magDec = pvt.magDec
        self.magAcc = pvt.magAcc

    def getDate(self):
        checkedNano = round(self.nano/1000)
        if checkedNano < 0:
            checkedNano = 0
        elif checkedNano > 999999:
            checkedNano = 999999
        date = datetime(self.year, self.month, self.day, self.hour, self.min, self.sec, checkedNano)
        if checkedNano > 999000:
            date = date - timedelta(seconds=1)
        return date
    
    def __str__(self):
        pvt_string = self.getDate().isoformat() + ","
        pvt_string += str(self.lat) + ","
        pvt_string += str(self.lon) + ","
        pvt_string += str(self.hMSL) + ","
        pvt_string += str(self.numSv) + ","
        pvt_string += str(self.hAcc) + ","
        pvt_string += str(self.vAcc) + ","
        pvt_string += str(self.pDop) + ","
        pvt_string += str(self.flags) + ","
        pvt_string += str(self.valid)
        return pvt_string

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

    def __str__(self):
        return str(self.fullyResolved)

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

    def __str__(self):
        return str(self.gnssFixOK)

class PVT_flags2:
    def __init__(self, flags2):
        pass
