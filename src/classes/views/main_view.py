""""""
from tkinter import font, Label, Frame, N, E, W, S
from classes.widgets.speed_gauge import SpeedGauge
from classes.widgets.signal_gauge import SignalGauge
from classes.widgets.trip_gauge import TripGauge
from classes.widgets.altitude_gauge import AltitudeGauge
from classes.widgets.main_gauge import MainGauge
from classes.widgets.engine_gauge import EngineGauge
from classes.widgets.misc_gauge import MiscGauge

class MainView(Frame):

    def __init__(self, app, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.app = app
        self.initializeGauges()
        self.registerGauges()
        self.setGaugeTitles()
        self.placeGauges()

    def set_text_color(self, color):
        self.speedGauge.set_text_color(color)
        self.signalGauge.set_text_color(color)
        self.miscGauge.set_text_color(color)

        self.altitudeGauge.set_text_color(color)
        self.tripGauge.set_text_color(color)
        self.engineGauge.set_text_color(color)
        
    def set_background_color(self, color):

        self.speedGauge.set_background_color(color)
        self.signalGauge.set_background_color(color)
        self.miscGauge.set_background_color(color)

        self.altitudeGauge.set_background_color(color)
        self.tripGauge.set_background_color(color)
        self.engineGauge.set_background_color(color)

        
    def initializeGauges(self):
        self.speedGauge = SpeedGauge(self.app, self, background='white', width=106)
        self.signalGauge = SignalGauge(self.app, self, background='white', width=106)
        self.miscGauge = MiscGauge(self.app, self, background='white', width=108)

        self.altitudeGauge = AltitudeGauge(self.app, self, background='white', width=106)
        self.tripGauge = TripGauge(self.app, self, background='white', width=108)
        self.engineGauge = EngineGauge(self.app, self, background='white',width=106)

    def registerGauges(self):
        if self.app.parser is not None:
            self.app.register("UBX-NAV-PVT", self.speedGauge)
            self.app.register("UBX-NAV-PVT", self.signalGauge)
            self.app.register("UBX-NAV-PVT", self.tripGauge)
            self.app.register("UBX-NAV-PVT", self.altitudeGauge)
        
        if self.app.obd_comm is not None:
            self.app.obd_comm.register("OBD-ENGINE_LOAD", self.engineGauge)
            self.app.obd_comm.register("OBD-COOLANT_TEMP", self.engineGauge)
            self.app.obd_comm.register("OBD-RPM", self.engineGauge)

            self.app.obd_comm.register("OBD-RPM", self.miscGauge)
            self.app.obd_comm.register("OBD-AMBIANT_AIR_TEMP", self.miscGauge)
            self.app.obd_comm.register("OBD-THROTTLE_POS", self.miscGauge)


    def setGaugeTitles(self):
        self.speedGauge.update_values(title="HRAÐI (km/klst)")
        self.signalGauge.update_values(title="MERKI")
        self.miscGauge.update_values(title="GÍR, ÚTIHITI, GJÖF")

        self.altitudeGauge.update_values(title="HÆÐ Y. S.")
        self.tripGauge.update_values(title="FERÐ")
        self.engineGauge.update_values(title="VÉL")

    def placeGauges(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.speedGauge.grid(row=1, column=0, sticky=N+E+W+S, pady=(0,1), padx=(0,1))
        self.miscGauge.grid(row=1, column=1, sticky=N+E+W+S, pady=(0,1), padx=(0,1))
        self.engineGauge.grid(row=1, column=2, sticky=N+E+W+S, pady=(0,1))

        self.altitudeGauge.grid(row=2, column=0, sticky=N+E+W+S, padx=(0,1))
        self.tripGauge.grid(row=2, column=1, sticky=N+E+W+S, padx=(0,1))
        self.signalGauge.grid(row=2, column=2, sticky=N+E+W+S)