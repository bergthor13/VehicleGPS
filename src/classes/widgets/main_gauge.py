from tkinter import *
import tkinter.font

class MainGauge(Frame):
    titleText = None
    gaugeValue = None
    gaugeSubvalue = None
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.initialize()
        self.initializeWidgets()
        self.placeWidgets()
        
    def initialize(self):
        self.titleFont    = tkinter.font.Font(family="Helvetica", size=7, weight="normal")
        self.valueFont    = tkinter.font.Font(family="FreeMono", size=25, weight="bold")
        self.subvalueFont = tkinter.font.Font(family="FreeMono", size=15, weight="bold")

    def initializeWidgets(self):
        self.titleText     = Label(self, text="---", background="black", fg="green",  font=self.titleFont)
        self.gaugeValue    = Label(self, text="--.-", background="black", fg="green", font=self.valueFont)
        self.gaugeSubvalue = Label(self, text="--.-", background="black", fg="green", font=self.subvalueFont)

    def placeWidgets(self):
        self.titleText.pack(pady=(5,0))
        self.gaugeValue.pack(pady=(5,0))
        self.gaugeSubvalue.pack(pady=(5,0))

    def updateValues(self, title = None, value = None, subvalue = None):
        if title is not None:
            self.titleText.config(text=title)
        if value is not None:
            self.gaugeValue.config(text=str(value))
        if subvalue is not None:
            self.gaugeSubvalue.config(text=str(subvalue))