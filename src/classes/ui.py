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
    sb = None
    mg1 = None
    mg2 = None
    mg3 = None
    mg4 = None
    mg5 = None
    mg6 = None
    oldPvt = None
    distance = 0.0
    startDate = None
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
    
    def updatePVT(self, pvt):
        if self.sb is None:
            return
        
        if self.mg1 is None:
            return

        if self.oldPvt is None:
            self.startDate = pvt.getDate()
            self.oldPvt = pvt
            return

        if pvt.fixType >= 1:
            if pvt.gSpeed > 0.5:
                self.distance+= vincenty((self.oldPvt.lat, self.oldPvt.lon), (pvt.lat, pvt.lon)).meters
                rndSpeed = round(pvt.gSpeed, 1)
                rndAccel = round(self.calculateMotionShift(self.oldPvt, pvt),1)
                self.mg1.updateValues(value=rndSpeed, subvalue=rndAccel)
            else:
                self.mg1.updateValues(value=round(0.0, 1), subvalue=round(self.calculateMotionShift(self.oldPvt, pvt),1))
            
            rndAvgSp = round(self.calculateAverageSpeed(pvt), 1)
            self.mg1.updateValues(subvalue2=rndAvgSp)

            self.mg5.updateValues(value=pvt.numSv, subvalue=str(round(pvt.hAcc/1000, 2)) + ' m')
            self.mg2.updateValues(subvalue=round(pvt.headMot/100000, 1))

            self.mg4.updateValues(value=round(pvt.hMSL/1000, 1))
        self.mg3.updateValues(value="10.4", subvalue="7.3", subvalue2="10.223 L")
        self.mg6.updateValues(value="55%", subvalue="90°C")

        if pvt.valid.validDate:
            self.sb.setDate(pvt.getDate())

        if pvt.valid.validTime:
            self.sb.setTime(pvt.getDate())
        self.calculateAverageSpeed(pvt)
        self.oldPvt = pvt

    def calculateMotionShift(self, oldPvt, pvt):
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
        if self.sb is None:
            return
        self.sb.updateWifiSymbol(isConnected)

    def run(self):
        self.root = Tk()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+40" % (self.windowWidth,self.windowHeight))
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
        self.mg1.updateValues(title="HRAÐI")
        self.mg2.updateValues(title="ÁTT")
        self.mg3.updateValues(title="EYÐSLA")

        self.mg4.updateValues(title="HÆÐ Y. S.")
        self.mg5.updateValues(title="VEGALENGD")
        self.mg6.updateValues(title="VÉL")

    def placeGauges(self):
        self.mg1.grid(row=1, column=0, sticky=N+E+W+S, pady=(0,1), padx=(0,1))
        self.mg3.grid(row=1, column=1, sticky=N+E+W+S, pady=(0,1), padx=(0,1))
        self.mg6.grid(row=1, column=2, sticky=N+E+W+S, pady=(0,1))

        self.mg4.grid(row=2, column=0, sticky=N+E+W+S, padx=(0,1))
        self.mg5.grid(row=2, column=1, sticky=N+E+W+S, padx=(0,1))
        self.mg2.grid(row=2, column=2, sticky=N+E+W+S, pady=(0,1))

        
        #self.btnRate1000.pack()
        #self.btnRate100.pack()
        self.root.config(background="green")
        self.root.mainloop()
