import threading
from tkinter import *
class GPS_UI (threading.Thread):
    windowWidth = 800
    windowHeight = 480
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
        
    def exit(self):
        self.root.destroy()
    
    def run(self):
        self.root = Tk()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (self.windowWidth,self.windowHeight))
        self.root.focus_set()
        self.root.configure(background='black')
        self.root.bind("<Escape>", lambda e: e.widget.quit())
        self.lblSpd = Label(self.root, background='green')
        self.btnRate1000 = Button(self.root,
                                  text="1 s Update Rate",
                                  command = self.didClickUpdateRate1000)
        self.btnRate100 = Button(self.root,
                                 text="100 ms Update Rate",
                                 command = self.didClickUpdateRate100)
        
        self.lblSpd.pack()
        self.btnRate1000.pack()
        self.btnRate100.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.mainloop()