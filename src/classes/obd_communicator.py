import threading
import obd
import time
from obd import OBDStatus
from classes.gps_logger import Observable

class OBD_Communicator(threading.Thread, Observable):
	
	connection = None

	def __init__(self, app):
		threading.Thread.__init__(self)
		self.app = app
		#obd.logger.setLevel(obd.logging.DEBUG)

	def createConnection(self):
		self.connection = obd.OBD("/dev/ttyUSB0", protocol="7", baudrate=9600)

	def establishConnection(self):
		if self.connection == None:
			self.createConnection()
		print(self.connection.status())
		if not self.connection.status() == OBDStatus.CAR_CONNECTED:
			threading.Timer(1, self.establishConnection).start()
			self.createConnection()

	def run(self):
		self.establishConnection()
		while not self.connection.status() == OBDStatus.CAR_CONNECTED:
			pass
		
		while self.connection.status() == OBDStatus.CAR_CONNECTED:
			response = self.connection.query(obd.commands.COOLANT_TEMP, force=True)
			if response.value is not None:
				self.app.update_coolant_temp(response.value.magnitude)

			response = self.connection.query(obd.commands.ENGINE_LOAD, force=True)
			if response.value is not None:
				self.app.update_engine_load(response.value.magnitude)
			
			response = self.connection.query(obd.commands.RPM, force=True)
			if response.value is not None:
				self.app.update_engine_rpm(response.value.magnitude)

			if response.value is None:
				self.connection.close()
				self.createConnection()
				time.sleep(1)
