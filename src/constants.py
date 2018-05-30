LOG_DIRECTORY = "/home/pi/Tracks"
ORIGINAL_LOG_DIRECTORY = "/home/pi/Tracks/Original"
GPX_LOG_DIRECTORY = "/home/pi/Tracks/GPX"
JSON_LOG_DIRECTORY = "/home/pi/Tracks/JSON"
BACKGROUND_COLOR = "white"
TEXT_COLOR = "black"

class OBDTypes:
	RPM = "RPM"
	COOLANT_TEMP = "COOLANT_TEMP"
	ENGINE_LOAD = "ENGINE_LOAD"
	AMBIANT_AIR_TEMP = "AMBIANT_AIR_TEMP"
	THROTTLE_POS = "THROTTLE_POS"
	FUEL_STATUS = "FUEL_STATUS"
	INTAKE_PRESSURE = "INTAKE_PRESSURE"
	TIMING_ADVANCE = "TIMING_ADVANCE"
	INTAKE_TEMP = "INTAKE_TEMP"
	
	@staticmethod
	def getAllTypes():
		return [attr for attr in dir(OBDTypes) if not callable(getattr(OBDTypes, attr)) and not attr.startswith("__")]