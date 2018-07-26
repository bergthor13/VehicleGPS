"""The UI of the device."""
import threading
from tkinter import Tk, Entry
from classes.widgets.status_bar import StatusBar
from classes.widgets.main_gauge import MainGauge
from classes.widgets.speed_gauge import SpeedGauge
from classes.views.main_view import MainView
from classes.views.settings_view import SettingsView
from classes.data.pvt import *
from datetime import datetime
from geopy.distance import vincenty


class UI_Controller (threading.Thread):
    window_width = 320
    window_height = 240
    window_x_offset = 0
    window_y_offset = 50

        
    status_bar = None
    main_view = None
    settings_view = None
    current_view = None


    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app

    def exit(self):
        self.root.destroy()

    def updateWiFi(self, isConnected):
        if self.status_bar is None:
            return
        self.status_bar.update_wifi_symbol(isConnected)

    def configure_window(self):
        self.root = Tk()
        self.root.overrideredirect(1)
        geo = "{}x{}+{}+{}".format(self.window_width,
                                   self.window_height,
                                   self.window_x_offset,
                                   self.window_y_offset)
        self.root.geometry(geo)
        self.root.focus_set()
        self.root.config(background="white")


    def initialize_views(self):
        self.status_bar = StatusBar(self.root, background='black')
        self.main_view = MainView(self.app, self.root, background="black")
        self.settings_view = SettingsView(self.root, background="white")

    def pack_views(self):
        self.status_bar.pack(fill="x")
        self.main_view.pack(fill="both")


    def run(self):
        self.configure_window()
        self.initialize_views()
        self.pack_views()

        self.current_view = self.main_view

        self.root.mainloop()
    
    def display_settings(self):
        if self.current_view is self.settings_view:
            self.settings_view.pack_forget()
            self.main_view.pack(fill="both")
            self.current_view = self.main_view
        else:
            self.main_view.pack_forget()
            self.settings_view.pack(fill="both")
            self.current_view = self.settings_view

