"""File containing a class for the main gauge."""
from tkinter import font, Label, Frame
from classes.widgets.main_gauge import MainGauge
from classes.pub_sub import Subscriber
from geopy.distance import vincenty


class AltitudeGauge(MainGauge, Subscriber):
    """
        A gauge that displays the speed, acceleration and average speed.
    """
    altitude_round_count = 3
    def __init__(self, app, *args, **kwargs):
        MainGauge.__init__(self, *args, **kwargs)
        self.app = app

    def update(self, message, pvt):
        
        gpsHistory = self.app.get_history(message)

        if gpsHistory is None and len(gpsHistory) == 0:
            return

        if not gpsHistory[0].flags.gnssFixOK:
            return
        if len(gpsHistory) > 1:
            self.update_values(value=round(self.get_rounded_speed(gpsHistory),1))

    def get_rounded_speed(self, history):

        value_count = min(self.altitude_round_count, len(history))
        
        totalSpeed = 0.0
        
        for value in range(value_count):
            totalSpeed += history[value].hMSL

        if value_count == 0.0:
            return 0.0
        return totalSpeed/value_count