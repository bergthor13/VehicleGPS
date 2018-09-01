"""File containing a class for the status bar."""
from tkinter import font, Label, PhotoImage, Frame, LEFT, RIGHT
from classes.pub_sub import Subscriber

class StatusBar(Frame, Subscriber):  # pylint: disable=too-many-ancestors
    """
        A status bar that displays the status of the device.
        Date, Time, Internet connectivity, OBD communication
    """
    
    date_label = None
    time_label = None
    wifi_symbol = None
    img_wifi = None
    img_no_wifi = None
    weekdays = None

    # Private methods
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.__initialize()
        self.__initialize_widgets()
        self.__place_widgets()

    def __initialize(self):
        self.status_bar_font = font.Font(family="FreeMono", size=14, weight="bold")
        self.img_no_wifi = PhotoImage(file=r"img/white-no-wifi.png")
        self.img_wifi = PhotoImage(file=r"img/white-wifi.png")
        self.weekdays = ["mán", "þri", "mið", "fim", "fös", "lau", "sun"]

    def __initialize_widgets(self):
        self.date_label = Label(self,
                                text="---, --.--.----",
                                background="black",
                                fg="white",
                                font=self.status_bar_font)

        self.time_label = Label(self,
                                text="--:--:--",
                                background="black",
                                fg="white",
                                font=self.status_bar_font)

        self.wifiSymbol = Label(self,
                                image=self.img_no_wifi,
                                background="black",
                                fg="white")

    def __place_widgets(self):
        self.date_label.pack(side=LEFT, padx=(3, 0))
        self.time_label.pack(side=RIGHT, padx=(0, 3))
        self.wifiSymbol.pack(side=RIGHT, padx=(0, 3))

    # Public methods
    def set_date(self, date):
        """Sets the date in the status bar according to a pre-determined format."""
        weekday = self.weekdays[date.weekday()]
        self.date_label.config(text=date.strftime("{0}, %d.%m.%Y".format(weekday)))

    def set_time(self, date):
        """Sets the time in the status bar according to a pre-determined format."""
        self.time_label.config(text=date.strftime("%H:%M:%S"))

    def update_wifi_symbol(self, hasInternet):
        """Updates the Wi-Fi symbol in the status bar."""
        if hasInternet:
            self.wifiSymbol.config(image=self.img_wifi)
        else:
            self.wifiSymbol.config(image=self.img_no_wifi)

    def update(self, message, pvt):
        # Update Speed Gauge

        if pvt.valid.validDate:
            self.set_date(pvt.getDate())

        if pvt.valid.validTime:
            self.set_time(pvt.getDate())

        # Update Acceleration Gauge

        # Update Average Speed Gauge
    
    def set_background_color(self, color):
        self.configure(background=color)
        self.date_label.configure(background=color)
        self.time_label.configure(background=color)

    def set_text_color(self, color):
        self.date_label.configure(fg=color)
        self.time_label.configure(fg=color)
