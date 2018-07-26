""""""
from tkinter import font, Label, Frame, N, E, W, S
from classes.widgets.speed_gauge import SpeedGauge
from classes.widgets.main_gauge import MainGauge

class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.initializeGauges()
        self.setGaugeTitles()
        self.placeGauges()
        
    def initializeGauges(self):
        self.speedGauge = SpeedGauge(self, background='white')
        #self.app.parser.register("UBX-NAV-PVT", self.speedGauge)
        self.satelliteGauge = MainGauge(self, background='white')
        self.consumptionGauge = MainGauge(self, background='white')

        self.altitudeGauge = MainGauge(self, background='white')
        self.distanceGauge = MainGauge(self, background='white')
        self.engineGauge = MainGauge(self, background='white')


    def setGaugeTitles(self):
        self.speedGauge.update_values(title="HRAÐI (km/klst)")
        self.satelliteGauge.update_values(title="MERKI")
        self.consumptionGauge.update_values(title="GÍR, ÚTIHITI, GJÖF")

        self.altitudeGauge.update_values(title="HÆÐ Y. S.")
        self.distanceGauge.update_values(title="FERÐ", subvalue2="--:--")
        self.engineGauge.update_values(title="VÉL")

    def placeGauges(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.speedGauge.grid(row=1, column=0, sticky=N+E+W+S, pady=(0,1), padx=(0,1))
        self.consumptionGauge.grid(row=1, column=1, sticky=N+E+W+S, pady=(0,1), padx=(0,1))
        self.engineGauge.grid(row=1, column=2, sticky=N+E+W+S, pady=(0,1))

        self.altitudeGauge.grid(row=2, column=0, sticky=N+E+W+S, padx=(0,1))
        self.distanceGauge.grid(row=2, column=1, sticky=N+E+W+S, padx=(0,1))
        self.satelliteGauge.grid(row=2, column=2, sticky=N+E+W+S)

def get_current_gear(speed, rpm):
    """Woo"""
    if rpm == 0.0:
        return "N"
    
    ratio = (speed/rpm)*100.0

    if (0.65 < ratio and ratio < 1.0) and speed > 5:
        return "1"
    elif (1.1 < ratio and ratio < 1.6) and speed > 9:
        return "2"
    elif (1.75 < ratio and ratio < 2.2) and speed > 13:
        return "3"
    elif (2.3 < ratio and ratio < 2.8) and speed > 19:
        return "4"
    elif (3.2 < ratio and ratio < 3.6) and speed > 25:
        return "5"
    else:
        return "N"