""""""
from tkinter import font, Label, Frame, Button
from classes.widgets.speed_gauge import SpeedGauge
from classes.widgets.main_gauge import MainGauge
import os, subprocess

class SettingsWifiView(Frame):
    timing_selection = 0
    ui_cont = None
    primary_color = ""
    secondary_color= ""
    def __init__(self, ui_cont, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        cmd = 'rfkill list all'
        result = subprocess.run(['rfkill', 'list', 'all'], stdout=subprocess.PIPE)
        if "Soft blocked: yes" in str(result.stdout):
            self.timing_selection = 0
        else:
            self.timing_selection = 1
        self.ui_cont = ui_cont
        self.initializeGauges()
        self.placeGauges()
        
        
    def initializeGauges(self):
        self.title_font = font.Font(family="FreeMono", size=15, weight="bold")
        self.subtitle_font = font.Font(family="FreeMono", size=13)
        self.trip_label = Label(self, text="Wi-Fi", font=self.title_font)
        self.time_display_label = Label(self, text="Wi-Fi", font=self.subtitle_font)
        self.wifi_on_button = Button(self, text= "On", width=5, relief="flat", command=self.set_wifi_on, font=self.subtitle_font)
        self.wifi_off_button = Button(self, text= "Off", width=5, relief="flat", command=self.set_wifi_off, font=self.subtitle_font)

        if self.ui_cont.is_night:
            self.set_theme("green", "black")
        else:
            self.set_theme("black", "white")
        self.set_timing_segment_active(self.timing_selection)

    def set_theme(self, primary, secondary):
        self.primary_color = primary
        self.secondary_color = secondary
        self.config(bg=secondary)
        self.trip_label.config(fg=primary, bg=secondary)
        self.time_display_label.config(fg=primary, bg=secondary)

    def set_timing_segment_active(self, index):
        if index == 0:
            self.wifi_off_button.config(highlightbackground=self.primary_color, bg=self.primary_color, activeforeground=self.secondary_color, foreground=self.secondary_color, activebackground=self.primary_color)
            self.wifi_on_button.config(highlightbackground=self.primary_color, bg=self.secondary_color, activeforeground=self.primary_color, foreground=self.primary_color, activebackground=self.secondary_color)
        elif index == 1:
            self.wifi_off_button.config(highlightbackground=self.primary_color, bg=self.secondary_color, activeforeground=self.primary_color, foreground=self.primary_color, activebackground=self.secondary_color)
            self.wifi_on_button.config(highlightbackground=self.primary_color, bg=self.primary_color, activeforeground=self.secondary_color, foreground=self.secondary_color, activebackground=self.primary_color)


    def placeGauges(self):
        self.trip_label.pack(fill="x")
        self.time_display_label.pack(side="left")
        self.wifi_on_button.pack(side="right")
        self.wifi_off_button.pack(side="right")

    def set_wifi_off(self):
        self.timing_selection = 0
        self.set_timing_segment_active(self.timing_selection)
        cmd1 = 'rfkill block wifi'
        cmd2 = 'ifconfig wlan0 down'
        os.system(cmd1)
        os.system(cmd2)


    def set_wifi_on(self):
        self.timing_selection = 1
        self.set_timing_segment_active(self.timing_selection)
        cmd1 = 'rfkill unblock wifi'
        cmd2 = 'ifconfig wlan0 up'
        os.system(cmd1)
        os.system(cmd2)

