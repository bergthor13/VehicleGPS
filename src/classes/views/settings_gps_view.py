""""""
from tkinter import font, Label, Frame, Button
from classes.widgets.speed_gauge import SpeedGauge
from classes.widgets.main_gauge import MainGauge

class SettingsGPSView(Frame):
    def __init__(self, ui_cont, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.initializeGauges()
        self.placeGauges()
        self.ui_cont = ui_cont
        
    def initializeGauges(self):
        self.title_font = font.Font(family="FreeMono", size=15, weight="bold")
        self.settings_text = Label(self, text="GPS Chip", background="white", font=self.title_font)
        self.force_cold_start_button = Button(self, text= "Force Cold Start", command=self.force_cold_start)
        self.update_rate_title = Label(self, text="GPS Update Rate", background="white", font=self.title_font)
        self.update_rate_1hz_button = Button(self, text= "1 Hz", command=self.set_update_rate_1hz)
        self.update_rate_2hz_button = Button(self, text= "2 Hz", command=self.set_update_rate_2hz)
        self.update_rate_5hz_button = Button(self, text= "5 Hz", command=self.set_update_rate_5hz)
        self.update_rate_10hz_button = Button(self, text= "10 Hz", command=self.set_update_rate_10hz)
        
            

    def placeGauges(self):
        self.settings_text.pack(fill="x")
        self.force_cold_start_button.pack()
        self.update_rate_title.pack(fill="x")
        self.update_rate_1hz_button.pack(side="left")
        self.update_rate_2hz_button.pack(side="left")
        self.update_rate_5hz_button.pack(side="left")
        self.update_rate_10hz_button.pack(side="left")

    def force_cold_start(self):
        self.ui_cont.app.config.forceColdStart()

    def set_update_rate_1hz(self):
        self.ui_cont.app.config.setRateSettings(1000, 1, 1)

    def set_update_rate_2hz(self):
        self.ui_cont.app.config.setRateSettings(500, 1, 1)

    def set_update_rate_5hz(self):
        self.ui_cont.app.config.setRateSettings(200, 1, 1)

    def set_update_rate_10hz(self):
        self.ui_cont.app.config.setRateSettings(100, 1, 1)
