class Observable:
	def addObserver(self, obs):
		pass

	def notifyObservers(self):
		pass

class Observer:
	def update(self):
		pass

class GpsLogger(Observer):
	def __init__(self):
		Observer.__init__()

	def update(self):
		pass