from tkinter import *
import tkinter.font
class StatusBar(Frame):
    dateText = None
    timeText = None
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        myFont = tkinter.font.Font(family="Helvetica", size= 10, weight="bold")
        self.dateText = Label(self, background="green", fg="black", font = myFont)
        self.timeText = Label(self,background="green", fg="black", font = myFont)

        self.dateText.pack(side=LEFT)
        self.timeText.pack(side=RIGHT)