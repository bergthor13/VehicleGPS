import threading
from tkinter import *
from classes.widgets.status_bar import StatusBar
import datetime
import tkinter.font

class GPS_UI (threading.Thread):
    #windowWidth = 800
    #windowHeight = 480
    windowWidth = 320
    windowHeight = 240
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.lblSpd = None
        self.app = app
    
    def updatePVT(self, pvt):
        if not self.lblSpd == None:
            #print("Updating text")
            self.lblSpd.config(text=round(pvt.gSpeed*3.6/1000, 1))
            dateTime = datetime.datetime(pvt.year, pvt.month, pvt.day, pvt.hour, pvt.min, pvt.sec)
            self.sb.dateText.config(text=dateTime.strftime("%d.%m.%Y"))
            self.sb.timeText.config(text=dateTime.strftime("%H:%M:%S"))
    
    def didClickUpdateRate1000(self):
        self.app.didClickUpdateRate(1000)
    
    def didClickUpdateRate100(self):
        self.app.didClickUpdateRate(100)
        
    def exit(self):
        self.root.destroy()
    
    def run(self):
        self.root = Tk()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (self.windowWidth,self.windowHeight))
        self.root.focus_set()
        self.root.configure(background='black')
        self.root.bind("<Escape>", lambda e: e.widget.quit())
        myFont = tkinter.font.Font(family="Helvetica", size= 60, weight="bold")
        self.lblSpd = Label(self.root, background='black', fg='green', font=myFont)
        self.btnRate1000 = Button(self.root,
                                  text="1 s Update Rate",
                                  command = self.didClickUpdateRate1000)
        self.btnRate100 = Button(self.root,
                                 text="100 ms Update Rate",
                                 command = self.didClickUpdateRate100)
        self.sb = StatusBar(self.root, width=self.windowWidth, height=20, background='green')
        
        self.sb.pack()
        
        self.lblSpd.pack()
        self.btnRate1000.pack()
        self.btnRate100.pack()
        self.root.mainloop()