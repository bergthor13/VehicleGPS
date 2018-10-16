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
        if pvt.fixType < 1:
            self.update_values(value=pvt.numSv, subvalue="EKKERT", subvalue2="MERKI")
        else:
            if pvt.hAcc >= 100:
                self.update_values(subvalue="{0:.0f} m".format(pvt.hAcc))
            elif pvt.hAcc >= 10:
                self.update_values(subvalue="{0:.1f} m".format(pvt.hAcc))
            else:
                self.update_values(subvalue="{0:.2f} m".format(pvt.hAcc))
                
            self.update_values(value=pvt.numSv, subvalue2="{0:.2f}".format(pvt.pDop))