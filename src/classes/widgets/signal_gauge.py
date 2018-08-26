"""File containing a class for the main gauge."""
from tkinter import font, Label, Frame
from classes.widgets.main_gauge import MainGauge
from classes.pub_sub import Subscriber
from geopy.distance import vincenty


class SignalGauge(MainGauge, Subscriber):
    """
        A gauge that displays the speed, acceleration and average speed.
    """

    def __init__(self, app, *args, **kwargs):
        MainGauge.__init__(self, *args, **kwargs)
        self.app = app

    def update(self, message, pvt):
        if not pvt.flags.gnssFixOK:
            self.update_values(value=pvt.numSv, subvalue="EKKERT", subvalue2="MERKI")
        else:
            self.update_values(value=pvt.numSv, subvalue=str(round(pvt.hAcc, 2)) + ' m', subvalue2=str(round(pvt.pDop, 2)))