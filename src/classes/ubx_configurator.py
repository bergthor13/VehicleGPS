import struct
class UBX_Configurator:
    syncChar1 = 0xB5
    syncChar2 = 0x62
    def __init__(self, serial):
        self.serial = serial
        
    # B5 62 06 01 03 00 01 07 00 12 50
    def setMessageRate(self, cls, id, rate):
        msgCls = 0x06; msgId = 0x01
        payload = bytes([cls, id, rate])
        self.sendMessage(msgCls, msgId, payload)
        
    def setRateSettings(self, measRate, navRate, timeRef):
        msgCls = 0x06; msgId = 0x08
        payload = struct.pack('HHH', measRate, navRate, timeRef)
        self.sendMessage(msgCls, msgId, payload)
    
    def sendMessage(self, cls, id, payload):
        message = bytes([cls, id]) + len(payload).to_bytes(2, byteorder="little") + payload
        checksum = self.calculateChecksum(message)
        solution = bytes([self.syncChar1, self.syncChar2]) + message + checksum
        self.serial.write(solution)
    
    # B5 62 06 09 0D 00 00 00 00 00 FF FF 00 00 00 00 00 00 17 31 BF
    def saveCurrentSettings(self):
        pass

    def set_gnss_config(self):
        msgCls = 0x06; msgId = 0x3E
        
        #self.sendMessage(msgCls, msgId, )


    def forceColdStart(self):
        msgCls = 0x06; msgId = 0x04
        navBbrMask = 0xFFFF.to_bytes(2, byteorder="little")
        resetMode = 2
        reserved1 = 0
        payload = navBbrMask + bytes([resetMode, reserved1])
        self.sendMessage(msgCls, msgId, payload)

    
    def getConvCode(self, payload):
        return str(len(payload)) + 's'
    
    def calculateChecksum(self, message):
        ckA, ckB = 0, 0
        
        for i in range(len(message)):
            ckA += message[i]
            ckB += ckA
        
        ckA = ckA & 0xFF
        ckB = ckB & 0xFF
        
        return bytes([ckA, ckB])