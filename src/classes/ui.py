import threading
from tkinter import *
class GPS_UI (threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.lblSpd = None
        self.app = app
    
    def updateSpeed(self, spd):
        if not self.lblSpd == None:
            #print("Updating text")
            self.lblSpd.config(text=spd)
    
    def didClickUpdateRate1000(self):
        print("1000")
        self.app.didClickUpdateRate(1000)
    
    def didClickUpdateRate100(self):
        print("100")
        self.app.didClickUpdateRate(100)
    
    def run(self):
        root = Tk()
        self.lblSpd = Label(root)
        self.btnRate1000 = Button(root,
                                  text="1 s Update Rate",
                                  command = self.didClickUpdateRate1000)
        self.btnRate100 = Button(root,
                                 text="100 ms Update Rate",
                                 command = self.didClickUpdateRate100)
        
        self.lblSpd.pack()
        self.btnRate1000.pack()
        self.btnRate100.pack()
        
        root.mainloop()