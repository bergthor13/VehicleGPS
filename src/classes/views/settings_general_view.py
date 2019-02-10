""""""
from tkinter import font, Label, Frame, Button
from classes.widgets.speed_gauge import SpeedGauge
from classes.widgets.main_gauge import MainGauge

class SettingsGeneralView(Frame):
    timing_selection = 0
    ui_cont = None
    primary_color = ""
    secondary_color= ""
    def __init__(self, ui_cont, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.ui_cont = ui_cont
        self.initializeGauges()
        self.placeGauges()
        
    def initializeGauges(self):
        self.title_font = font.Font(family="FreeMono", size=15, weight="bold")
        self.subtitle_font = font.Font(family="FreeMono", size=13)
        self.trip_label = Label(self, text="Ferð", font=self.title_font)
        self.time_display_label = Label(self, text="Tímataka", font=self.subtitle_font)
        self.timing_moving_label = Button(self, text= "Moving", width=5, relief="flat", command=self.set_timing_moving, font=self.subtitle_font)
        self.timing_all_label = Button(self, text= "All", width=5, relief="flat", command=self.set_timing_all, font=self.subtitle_font)

        if self.ui_cont.is_night:
            self.set_theme("green", "black")
        else:
            self.set_theme("black", "white")
        self.set_timing_segment_active(self.timing_selection)

    def set_theme(self, primary, secondary):
        self.primary_color = primary
        self.secondary_color = secondary
        self.config(bg=secondary)
        self.trip_label.config(fg=primary, bg=secondary)
        self.time_display_label.config(fg=primary, bg=secondary)

    def set_timing_segment_active(self, index):
        if index == 0:
            self.timing_all_label.config(highlightbackground=self.primary_color, bg=self.primary_color, activeforeground=self.secondary_color, foreground=self.secondary_color, activebackground=self.primary_color)
            self.timing_moving_label.config(highlightbackground=self.primary_color, bg=self.secondary_color, activeforeground=self.primary_color, foreground=self.primary_color, activebackground=self.secondary_color)
        elif index == 1:
            self.timing_all_label.config(highlightbackground=self.primary_color, bg=self.secondary_color, activeforeground=self.primary_color, foreground=self.primary_color, activebackground=self.secondary_color)
            self.timing_moving_label.config(highlightbackground=self.primary_color, bg=self.primary_color, activeforeground=self.secondary_color, foreground=self.secondary_color, activebackground=self.primary_color)


    def placeGauges(self):
        self.trip_label.pack(fill="x")
        self.time_display_label.pack(side="left")
        self.timing_moving_label.pack(side="right")
        self.timing_all_label.pack(side="right")

    def set_timing_all(self):
        self.timing_selection = 0
        self.set_timing_segment_active(self.timing_selection)


    def set_timing_moving(self):
        self.timing_selection = 1
        self.set_timing_segment_active(self.timing_selection)
