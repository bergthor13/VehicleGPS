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
		Publisher.__init__(self, ["OBD-COOLANT_TEMP", "OBD-ENGINE_LOAD", "OBD-AMBIANT_AIR_TEMP", "OBD-RPM", "OBD-THROTTLE_POS"])

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

	def run(self):
		self.obd = __import__('obd')
		self.establishConnection()
		while not self.connection.status() == self.obd.OBDStatus.CAR_CONNECTED:
			pass
		
		while self.connection.status() == self.obd.OBDStatus.CAR_CONNECTED:
			
			if self.coolantCount == 10 or self.refreshAll:
				try:
					response = self.connection.query(self.obd.commands.COOLANT_TEMP, force=True)
				except:
					hasConnection = False
				if response.value is not None:
					self.hasConnection = True
					self.dispatch("OBD-COOLANT_TEMP", response.value.magnitude)
				else:
					self.refreshAll = True
				self.coolantCount = 0
			self.coolantCount = self.coolantCount + 1
			
			try:
				response = self.connection.query(self.obd.commands.ENGINE_LOAD, force=True)
			except:
				hasConnection = False

			if response.value is not None:
				self.hasConnection = True
				self.dispatch("OBD-ENGINE_LOAD", response.value.magnitude)
			else:
				self.refreshAll = True

			if self.ambientCount == 100 or self.refreshAll:
				try:
					response = self.connection.query(self.obd.commands.AMBIANT_AIR_TEMP, force=True)
				except:
					hasConnection = False
				if response.value is not None:
					self.hasConnection = True
					self.dispatch("OBD-AMBIANT_AIR_TEMP", response.value.magnitude)
				else:
					self.refreshAll = True
				self.ambientCount = 0
			self.ambientCount = self.ambientCount + 1

			try:
				response = self.connection.query(self.obd.commands.RPM, force=True)
			except:
				hasConnection = False
			if response.value is not None:
				self.hasConnection = True
				self.dispatch("OBD-RPM", response.value.magnitude)
			else:
				self.refreshAll = True


			try:
				response = self.connection.query(self.obd.commands.THROTTLE_POS, force=True)
			except:
				hasConnection = False
			if response.value is not None:
				self.hasConnection = True
				self.dispatch("OBD-THROTTLE_POS", response.value.magnitude)
			else:
				self.refreshAll = True

			# response = self.connection.query(obd.commands.FUEL_STATUS, force=True)
			# if response.value is not None:
			# 	print(response.value)
			# 	#self.app.update_metric("FUEL_STATUS", response.value.magnitude)
			# else:
			# 	self.app.update_metric("FUEL_STATUS", None)

			# response = self.connection.query(obd.commands.INTAKE_PRESSURE, force=True)
			# if response.value is not None:
			# 	self.app.update_metric("INTAKE_PRESSURE", response.value.magnitude)
			# else:
			# 	self.app.update_metric("INTAKE_PRESSURE", None)

			# response = self.connection.query(obd.commands.TIMING_ADVANCE, force=True)
			# if response.value is not None:
			# 	self.app.update_metric("TIMING_ADVANCE", response.value.magnitude)
			# else:
			# 	self.app.update_metric("TIMING_ADVANCE", None)

			# response = self.connection.query(obd.commands.INTAKE_TEMP, force=True)
			# if response.value is not None:
			# 	self.app.update_metric("INTAKE_TEMP", response.value.magnitude)
			# else:
			# 	self.app.update_metric("INTAKE_TEMP", None)
			if self.hasConnection:
				self.refreshAll = False

			if response.value is None:
				self.hasConnection = False
				self.dispatch("OBD-COOLANT_TEMP", None)
				self.dispatch("OBD-ENGINE_LOAD", None)
				self.dispatch("OBD-AMBIANT_AIR_TEMP", None)
				self.dispatch("OBD-RPM", None)
				self.dispatch("OBD-THROTTLE_POS", None)
				self.connection.close()
				self.createConnection()
