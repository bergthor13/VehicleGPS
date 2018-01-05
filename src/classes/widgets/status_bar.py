from tkinter import *
import tkinter.font

class StatusBar(Frame):
    dateText = None
    timeText = None
    wifiSymbol = None
    imgWifi = None
    imgNoWifi = None
    thisFrame = None
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        myFont = tkinter.font.Font(family="Helvetica", size=10, weight="bold")

        self.dateText = Label(self, background="green", fg="black", font=myFont)
        self.timeText = Label(self,background="green", fg="black", font=myFont)
        
        self.imgNoWifi = PhotoImage(file="src/img/no-wifi.png")
        self.imgWifi = PhotoImage(file="src/img/wifi.png")

        self.wifiSymbol = Label(self, image=self.imgNoWifi, background="green", fg="black")

        self.dateText.pack(side=LEFT)
        self.timeText.pack(side=RIGHT)
        self.wifiSymbol.pack(side=RIGHT, padx=(0,3))
        

    def updateWifiSymbol(self, hasInternet):
        if hasInternet:
            self.wifiSymbol.config(image=self.imgWifi)
        else:
            self.wifiSymbol.config(image=self.imgNoWifi)