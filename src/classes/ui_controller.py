"""The UI of the device."""
import threading
import constants

from tkinter import Tk, Entry
from classes.widgets.status_bar import StatusBar
from classes.widgets.main_gauge import MainGauge
from classes.widgets.speed_gauge import SpeedGauge
from classes.views.main_view import MainView
from classes.views.settings_view import SettingsView
from classes.views.alert_view import AlertView

class UI_Controller (threading.Thread):
    window_width = 320
    window_height = 240
    window_x_offset = 0
    window_y_offset = 0

        
    status_bar = None
    main_view = None
    settings_view = None
    current_view = None
    upload_alert_view = None
    is_night = False


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
        self.status_bar.bind("<Button-1>", self.display_settings, True)
        self.app.parser.register("UBX-NAV-PVT", self.status_bar)
        self.main_view = MainView(self.app, self.root)
        self.settings_view = SettingsView(self, self.root)
        self.upload_alert_view = AlertView(self.root, width=280, height=75, relief='raised')
        if self.is_night:
            self.set_theme("black", "green")
        else:
            self.set_theme("white", "black")
        

    def set_theme(self, main_color, back_color):
        self.main_view.configure(background=back_color)
        self.main_view.set_background_color(main_color)
        self.main_view.set_text_color(back_color)
        self.status_bar.set_background_color(back_color)
        self.status_bar.set_text_color(main_color)

    def pack_views(self):
        self.status_bar.pack(fill="x")
        self.main_view.pack(fill="both")


    def run(self):
        self.configure_window()
        self.initialize_views()
        self.pack_views()

        self.current_view = self.main_view

        self.root.mainloop()
    
    def change_color(self):
        if self.is_night:
            self.set_theme("white", "black")
            self.is_night = False
            self.save_theme("light")
        else:
            self.set_theme("black", "green")
            self.is_night = True
            self.save_theme("dark")

    def save_theme(self, theme_name):
        with open(constants.COLOR_MODE_FILE, 'w') as color_mode:
            color_mode.write(theme_name)


    def display_view(self, view):
        self.current_view.pack_forget()
        view.pack(fill="both")
        self.current_view = view

    def display_settings(self, event):
        if self.current_view is not self.main_view:
            self.display_view(self.main_view)
        else:
            self.display_view(self.settings_view)

    def display_upload_alert(self):
        self.upload_alert_view.place(x=20, y=82.5,anchor="nw")

    def hide_upload_alert(self):
        self.upload_alert_view.place_forget()

