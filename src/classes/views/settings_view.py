""""""
from tkinter import font, Label, Frame
from classes.widgets.speed_gauge import SpeedGauge
from classes.widgets.main_gauge import MainGauge

class SettingsView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.initializeGauges()
        self.placeGauges()
        
    def initializeGauges(self):
        self.settings_text = Label(self, text="Settings", background="white")

    def placeGauges(self):
        self.settings_text.pack(fill="both")
