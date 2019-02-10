""""""
from tkinter import font, Label, Frame, Button, Listbox
from classes.widgets.speed_gauge import SpeedGauge
from classes.widgets.main_gauge import MainGauge

class SettingsOBDView(Frame):        
    settings_list = ["SAE J1850 PWM","SAE J1850 VPW","AUTO, ISO 9141-2","ISO 14230-4 (KWP 5BAUD)","ISO 14230-4 (KWP FAST)","ISO 15765-4 (CAN 11/500)","ISO 15765-4 (CAN 29/500)","ISO 15765-4 (CAN 11/250)","ISO 15765-4 (CAN 29/250)","SAE J1939 (CAN 29/250)"]
    def __init__(self, ui_cont, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.initializeGauges()
        self.placeGauges()
        self.ui_cont = ui_cont
        
    def initializeGauges(self):
        self.title_font = font.Font(family="FreeMono", size=15, weight="bold")
        self.list_font = font.Font(family="FreeMono", size=13)
        self.settings_text = Label(self, text="OBD Connection", background="white", font=self.title_font)
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
            self.listbox.selection_clear(item_id)