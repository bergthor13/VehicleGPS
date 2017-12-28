import threading
from tkinter import *
class GPS_UI (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.lblSpd = None
    
    def updateSpeed(self, spd):
        if not self.lblSpd == None:
            #print("Updating text")
            self.lblSpd.config(text=spd)
    
    def didClickUpdateRate1000():
        print("1000")
    
    def didClickUpdateRate100():
        print("100")
    
    def run(self):
        root = Tk()
        self.lblSpd = Label(root, text="SPEED")
        self.lblSpd.pack()
        
        self.btnRate1000 = Button(root, text="1 s Update Rate", command="didClickUpdateRate1000")
        self.btnRate100 = Button(root, text="100 ms Update Rate", command="didClickUpdateRate100")
        
        self.btnRate1000.pack()
        self.btnRate100.pack()
        
        root.mainloop()