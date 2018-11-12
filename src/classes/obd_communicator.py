import threading
import time
import constants
from classes.pub_sub import Publisher

class OBD_Communicator(threading.Thread, Publisher):
    
    connection = None
    coolantCount = 10
    ambientCount = 100
    refreshAll = True
    hasConnection = False
    hasGPSFix = False

    def __init__(self, app):
        threading.Thread.__init__(self)
        Publisher.__init__(self, ["OBD-SPEED", "OBD-COOLANT_TEMP", "OBD-ENGINE_LOAD", "OBD-AMBIANT_AIR_TEMP", "OBD-RPM", "OBD-THROTTLE_POS"])
        self.requests = []
        self.app = app
        #obd.logger.setLevel(obd.logging.DEBUG)

    def createConnection(self):
        try:
            self.connection = self.obd.OBD("/dev/ttyUSB0", protocol="7", baudrate=9600)
        except:
            hasConnection = False

    def establishConnection(self):
        if self.connection == None:
            self.createConnection()
        print(self.connection.status())
        if not self.connection.status() == self.obd.OBDStatus.CAR_CONNECTED:
            threading.Timer(1, self.establishConnection).start()
            self.createConnection()

    def register(self, event, sub, callback=None, interval=None):
        super(OBD_Communicator, self).register(event, sub, callback)
        self.requests.append({"sentence": event, "command": None})

    def update_values(self, sentence_name, command):
        try:
            response = self.connection.query(command, force=True)
        except:
            hasConnection = False
        if response.value is not None:
            self.hasConnection = True
            self.dispatch(sentence_name, response.value.magnitude)
        else:
            self.refreshAll = True
        return response.value

    def run(self):
        self.obd = __import__('obd')
        self.establishConnection()
        for request in self.requests:
            if len(request["sentence"]) > 4:
                request["command"] = self.obd.commands[request["sentence"][4:]]
        while not self.connection.status() == self.obd.OBDStatus.CAR_CONNECTED:
            pass

        while self.connection.status() == self.obd.OBDStatus.CAR_CONNECTED:
            # for request in self.requests:
            # 	response = self.update_values(request["sentence"], request["command"])

            response = self.update_values("OBD-ENGINE_LOAD", self.obd.commands.ENGINE_LOAD)
            response = self.update_values("OBD-THROTTLE_POS", self.obd.commands.THROTTLE_POS)
            response = self.update_values("OBD-RPM", self.obd.commands.RPM)
            response = self.update_values("OBD-SPEED", self.obd.commands.SPEED)


            if self.coolantCount == 10 or self.refreshAll:
                response = self.update_values("OBD-COOLANT_TEMP", self.obd.commands.COOLANT_TEMP)
                self.coolantCount = 0
            self.coolantCount = self.coolantCount + 1

            if self.ambientCount == 100 or self.refreshAll:
                response = self.update_values("OBD-AMBIANT_AIR_TEMP", self.obd.commands.AMBIANT_AIR_TEMP)
                self.ambientCount = 0
            self.ambientCount = self.ambientCount + 1

            if self.hasConnection:
                self.refreshAll = False

            if response is None:
                self.hasConnection = False
                self.dispatch("OBD-COOLANT_TEMP", None)
                self.dispatch("OBD-ENGINE_LOAD", None)
                self.dispatch("OBD-AMBIANT_AIR_TEMP", None)
                self.dispatch("OBD-RPM", None)
                self.dispatch("OBD-THROTTLE_POS", None)
                self.connection.close()
                self.createConnection()
