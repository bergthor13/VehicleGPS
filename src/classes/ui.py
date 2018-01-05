import threading
from tkinter import *
from classes.widgets.status_bar import StatusBar
from classes.widgets.main_gauge import MainGauge
import datetime
import tkinter.font

class GPS_UI (threading.Thread):
    #windowWidth = 800
    #windowHeight = 480
    windowWidth = 320
    windowHeight = 240
    sb = None
    mg1 = None
    weekdays=["mán","þri","mið","fim","fös","lau","sun"]
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
    
    def updatePVT(self, pvt):
        if self.mg1 is not None:
            if pvt.gSpeed*3.6/1000 > 0.5:
                self.mg1.updateValues(value=round(pvt.gSpeed*3.6/1000, 1))
            else:
                self.mg1.updateValues(value=0.0)

            dateTime = datetime.datetime(pvt.year, pvt.month, pvt.day, pvt.hour, pvt.min, pvt.sec)
            self.sb.dateText.config(text=dateTime.strftime("{0}, %d.%m.%Y".format(self.weekdays[dateTime.weekday()])))
            self.sb.timeText.config(text=dateTime.strftime("%H:%M:%S"))
    
    '''
        asdf
    '''
    def didClickUpdateRate1000(self):
        self.app.didClickUpdateRate(1000)
    
    def didClickUpdateRate100(self):
        self.app.didClickUpdateRate(100)
        
    def exit(self):
        self.root.destroy()

    def updateWiFi(self, isConnected):
        if self.sb is None:
            return
        self.sb.updateWifiSymbol(isConnected)

    def run(self):
        self.root = Tk()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (self.windowWidth,self.windowHeight))
        self.root.focus_set()
        self.root.configure(background='black')
        self.root.bind("<Escape>", lambda e: e.widget.quit())
        self.btnRate1000 = Button(self.root,
                                  text="1 s Update Rate",
                                  command = self.didClickUpdateRate1000)
        self.btnRate100 = Button(self.root,
                                 text="100 ms Update Rate",
                                 command = self.didClickUpdateRate100)
        self.sb = StatusBar(self.root, height=20, background='green')
        self.sb.grid(row=0,column=0, columnspan=3, sticky=W+E)
        for i in range(0,3):
            self.root.columnconfigure(i, weight=1, uniform="fred")

        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)


        self.initializeGauges()
        self.setGaugeTitles()
        self.placeGauges()

    def initializeGauges(self):
        self.mg1 = MainGauge(self.root, background='black')
        self.mg2 = MainGauge(self.root, background='black')
        self.mg3 = MainGauge(self.root, background='black')

        self.mg4 = MainGauge(self.root, background='black')
        self.mg5 = MainGauge(self.root, background='black')
        self.mg6 = MainGauge(self.root, background='black')

    def setGaugeTitles(self):
        self.mg1.updateValues("SPEED", 10, 1)
        self.mg2.updateValues("DIRECTION", 10, 1)
        self.mg3.updateValues("TEMPERATURE", 10, 1)

        self.mg4.updateValues("ALTITUDE", 10, 1)
        self.mg5.updateValues("SATELLITES", 10, 1)
        self.mg6.updateValues("POINTS", 10, 1)

    def placeGauges(self):
        self.mg1.grid(row=1, column=0, sticky=N+E+W+S, pady=(0,1), padx=(0,1))
        self.mg2.grid(row=1, column=1, sticky=N+E+W+S, pady=(0,1), padx=(0,1))
        self.mg3.grid(row=1, column=2, sticky=N+E+W+S, pady=(0,1))
        
        self.mg4.grid(row=2, column=0, sticky=N+E+W+S, padx=(0,1))
        self.mg5.grid(row=2, column=1, sticky=N+E+W+S, padx=(0,1))
        self.mg6.grid(row=2, column=2, sticky=N+E+W+S)
        
        #self.btnRate1000.pack()
        #self.btnRate100.pack()
        self.root.config(background="green")
        self.root.mainloop()