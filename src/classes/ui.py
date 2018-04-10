import threading
from tkinter import *
from classes.widgets.status_bar import StatusBar
from classes.widgets.main_gauge import MainGauge
from classes.data.pvt import *
from datetime import datetime
import tkinter.font
from geopy.distance import vincenty

class GPS_UI (threading.Thread):
    windowWidth = 320
    windowHeight = 240
    statusBar = None
    speedGauge = None
    satelliteGauge = None
    consumptionGauge = None
    altitudeGauge = None
    distanceGauge = None
    engineGauge = None
    oldPvt = None
    distance = 0.0
    startDate = None
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
    
    def updatePVT(self, pvt):
        if self.statusBar is None:
            return
        
        if (self.speedGauge is None or
            self.satelliteGauge is None or
            self.altitudeGauge is None):
            return

        if self.oldPvt is None:
            self.startDate = pvt.getDate()
            self.oldPvt = pvt
            return

        if pvt.fixType >= 1:
            if pvt.gSpeed > 0.5:
                self.distance += vincenty((self.oldPvt.lat, self.oldPvt.lon), (pvt.lat, pvt.lon)).meters
                self.setSpeed(pvt.gSpeed)
                accel = self.calculateAcceleration(self.oldPvt, pvt)
                self.setAcceleration(accel)
            else:
                self.setSpeed(0.0)
                self.setAcceleration(0.0)
            
            avgSpeed = self.calculateAverageSpeed(pvt)
            self.setAverageSpeed(avgSpeed)

            self.satelliteGauge.updateValues(value=pvt.numSv, subvalue=str(round(pvt.hAcc/1000, 2)) + ' m')
            self.altitudeGauge.updateValues(value=round(pvt.hMSL/1000, 1))
            #self.satelliteGauge.updateValues(subvalue=round(pvt.headMot/100000, 1))

        self.setDate(pvt.valid, pvt.getDate())

        self.calculateAverageSpeed(pvt)
        self.oldPvt = pvt
        self.distanceGauge.updateValues(value=round(self.distance/1000,1))

    def setDate(self, valid, date):
        if valid.validDate:
            self.statusBar.setDate(date)

        if valid.validTime:
            self.statusBar.setTime(date)

    def setSpeed(self, speed):
        self.speedGauge.updateValues(value=int(round(speed,0)))

    def setAcceleration(self, acceleration):
        self.speedGauge.updateValues(subvalue=round(acceleration,1))

    def setAverageSpeed(self, avgSpeed):
        self.speedGauge.updateValues(subvalue2=round(avgSpeed,1))

    def calculateAcceleration(self, oldPvt, pvt):
        newTime = pvt.getDate()
        oldTime = oldPvt.getDate()

        newSpeed = pvt.gSpeed
        oldSpeed = oldPvt.gSpeed

        spdDiff = newSpeed-oldSpeed
        timDiff = (newTime-oldTime).microseconds
        
        return spdDiff*(1000000/timDiff)

    def calculateAverageSpeed(self, pvt):
        duration = (pvt.getDate()-self.startDate).seconds/60/60
        if not(duration == 0):
            return (self.distance/1000)/duration
        return 0.0
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
        if self.statusBar is None:
            return
        self.statusBar.updateWifiSymbol(isConnected)

    def didClickSettings(self, event):
        print("Settings Clicked")

    def run(self):
        self.root = Tk()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+40" % (self.windowWidth,self.windowHeight))
        self.root.focus_set()
        # self.root.bind("<Escape>", lambda e: e.widget.quit())
        # self.btnRate1000 = Button(self.root,
        #                           text="1 s Update Rate",
        #                           command = self.didClickUpdateRate1000)
        # self.btnRate100 = Button(self.root,
        #                          text="100 ms Update Rate",
        #                          command = self.didClickUpdateRate100)
        self.statusBar = StatusBar(self.root, height=20, background='black')
        self.statusBar.grid(row=0,column=0, columnspan=3, sticky=W+E)
        self.statusBar.bind('<Button-1>', self.didClickSettings)

        for i in range(0,3):
            self.root.columnconfigure(i, weight=1, uniform="fred")

        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)


        self.initializeGauges()
        self.setGaugeTitles()
        self.placeGauges()

    def initializeGauges(self):
        self.speedGauge = MainGauge(self.root, background='white')
        self.satelliteGauge = MainGauge(self.root, background='white')
        self.consumptionGauge = MainGauge(self.root, background='white')

        self.altitudeGauge = MainGauge(self.root, background='white')
        self.distanceGauge = MainGauge(self.root, background='white')
        self.engineGauge = MainGauge(self.root, background='white')

        self.consumptionGauge.updateValues(value="10.4", subvalue="7.3", subvalue2="10.223 L")
        self.engineGauge.updateValues(value="55%", subvalue="90°C", subvalue2="13.0 V")
        


    def setGaugeTitles(self):
        self.speedGauge.updateValues(title="HRAÐI (km/klst)")
        self.satelliteGauge.updateValues(title="MERKI")
        self.consumptionGauge.updateValues(title="EYÐSLA (L/100 km)")

        self.altitudeGauge.updateValues(title="HÆÐ Y. S.")
        self.distanceGauge.updateValues(title="VEGALENGD")
        self.engineGauge.updateValues(title="VÉL")

    def placeGauges(self):
        self.speedGauge.grid(row=1, column=0, sticky=N+E+W+S, pady=(0,1), padx=(0,1))
        self.consumptionGauge.grid(row=1, column=1, sticky=N+E+W+S, pady=(0,1), padx=(0,1))
        self.engineGauge.grid(row=1, column=2, sticky=N+E+W+S, pady=(0,1))

        self.altitudeGauge.grid(row=2, column=0, sticky=N+E+W+S, padx=(0,1))
        self.distanceGauge.grid(row=2, column=1, sticky=N+E+W+S, padx=(0,1))
        self.satelliteGauge.grid(row=2, column=2, sticky=N+E+W+S)

        
        #self.btnRate1000.pack()
        #self.btnRate100.pack()
        self.root.config(background="black")
        self.root.mainloop()
