""""""
from tkinter import font, Label, Frame, Button
from classes.widgets.speed_gauge import SpeedGauge
from classes.widgets.main_gauge import MainGauge

class SettingsAppearanceView(Frame):
    def __init__(self, ui_cont, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.initializeGauges()
        self.placeGauges()
        self.ui_cont = ui_cont
        
    def initializeGauges(self):
        self.title_font = font.Font(family="FreeMono", size=15, weight="bold")
        self.settings_text = Label(self, text="Appearance", background="white", font=self.title_font)

    def placeGauges(self):
        self.settings_text.pack(fill="x")