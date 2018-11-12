""""""
from tkinter import font, Label, Frame
from classes.widgets.speed_gauge import SpeedGauge
from classes.widgets.main_gauge import MainGauge

class AlertView(Frame):
    title_label = None
    message_label = None

    title_font = None
    message_font = None
    
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.config(relief="raised")
        self.__initialize_fonts()
        self.title_label = Label(self,
                                text="Title",
                                fg="black",
                                font = self.title_font)
        self.message_label = Label(self,
                                text="Message",
                                fg="black",
                                font = self.message_font)
        self.pack_propagate(0)
        self.message_label.config(wraplength=self["width"]-5)
        self.title_label.pack()
        self.message_label.pack()

    def __initialize_fonts(self):
        self.title_font = font.Font(family="Helvetica", size=15, weight="bold")
        self.message_font = font.Font(family="Helvetica", size=13, weight="normal")

    
    def set_alert_title(self, title):
        self.title_label["text"] = title
    
    def set_alert_message(self, message):
        self.message_label["text"] = message
