"""File containing a class for the main gauge."""
from tkinter import font, Label, Frame
from classes.widgets.main_gauge import MainGauge
from classes.pub_sub import Subscriber
from geopy.distance import vincenty


class AltitudeGauge(MainGauge, Subscriber):
    """
        A gauge that displays the speed, acceleration and average speed.
    """

    def __init__(self, app, *args, **kwargs):
        MainGauge.__init__(self, *args, **kwargs)
        self.app = app

    def update(self, message, pvt):
        
        gpsHistory = self.app.get_history(message)

        if gpsHistory is None and len(gpsHistory) == 0:
            return

        self.update_values(value=round(self.get_rounded_speed(pvt.hMSL, gpsHistory[1].hMSL),1))

    def get_rounded_speed(self, new_speed, old_speed):
        """
        get_rounded_speed
        """
        if old_speed is None:
            return new_speed
        
        return (new_speed+old_speed)/2.0
            