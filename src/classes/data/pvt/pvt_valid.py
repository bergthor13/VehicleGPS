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