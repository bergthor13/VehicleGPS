"""File containing a class for the main gauge."""
from tkinter import font, Label, Frame
from classes.widgets.main_gauge import MainGauge
from classes.pub_sub import Subscriber
from geopy.distance import vincenty


class EngineGauge(MainGauge, Subscriber):
    """
        A gauge that displays the speed, acceleration and average speed.
    """

    def __init__(self, app, *args, **kwargs):
        MainGauge.__init__(self, *args, **kwargs)
        self.app = app

    def update(self, message, value):
        
        if message == "OBD-ENGINE_LOAD":
            if value is None:
                self.update_values(value="--%")
            else:
                self.update_values(value=str(int(value))+"%")

        if message == "OBD-COOLANT_TEMP":
            if value is None:
                self.update_values(subvalue="--°C")
            else:
                self.update_values(subvalue=str(int(value))+"°C")

        if message == "OBD-RPM":
            if value is None:
                self.update_values(subvalue2="----")
            else:
                self.update_values(subvalue2=int(value))