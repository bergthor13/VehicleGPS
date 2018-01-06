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