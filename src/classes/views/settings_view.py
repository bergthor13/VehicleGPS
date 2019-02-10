""""""
from tkinter import font, Label, Frame, Listbox
from classes.views.settings_general_view import SettingsGeneralView
from classes.views.settings_wifi_view import SettingsWifiView
from classes.views.settings_appearance_view import SettingsAppearanceView
from classes.views.settings_gps_view import SettingsGPSView
from classes.views.settings_obd_view import SettingsOBDView

class SettingsView(Frame):
    settings_list = ["General", "Wi-Fi", "Appearance", "GPS Chip", "OBD Connection"]
    def __init__(self, ui_cont, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.initializeGauges()
        self.placeGauges()
        self.ui_cont = ui_cont
        self.gps_chip_view = SettingsGPSView(ui_cont, self.ui_cont.root)
        self.general_view = SettingsGeneralView(ui_cont, self.ui_cont.root)
        self.wifi_view = SettingsWifiView(ui_cont, self.ui_cont.root)
        self.appearance_view = SettingsAppearanceView(ui_cont, self.ui_cont.root)
        self.obd_view = SettingsOBDView(ui_cont, self.ui_cont.root)
        
    def initializeGauges(self):
        self.title_font = font.Font(family="FreeMono", size=15, weight="bold")
        self.list_font = font.Font(family="FreeMono", size=28)
        self.settings_text = Label(self, text="Settings", background="white", font=self.title_font)
        self.listbox = Listbox(self, font=self.list_font, selectmode="single", borderwidth=0, relief="flat", highlightthickness=0)
        self.listbox.bind('<ButtonRelease-1>', self.item_deselected)
        for item in self.settings_list:
            self.listbox.insert(10, item)
            

    def placeGauges(self):
        self.settings_text.pack(fill="x")
        self.listbox.pack(fill="both", expand=1)

    def item_deselected(self, event):
        curr_selct = self.listbox.curselection()
        if len(curr_selct) > 0:
            item_id = self.listbox.curselection()[0]
            item_name = self.settings_list[item_id]
            if item_name == "General":
                self.ui_cont.display_view(self.general_view)
            if item_name == "Wi-Fi":
                self.ui_cont.display_view(self.wifi_view)
            if item_name == "Appearance":
                self.ui_cont.display_view(self.appearance_view)
            if item_name == "GPS Chip":
                self.ui_cont.display_view(self.gps_chip_view)
            if item_name == "OBD Connection":
                self.ui_cont.display_view(self.obd_view)
            self.listbox.selection_clear(item_id)