"""File containing a class for the main gauge."""
from tkinter import font, Label, Frame
from classes.widgets.main_gauge import MainGauge
from classes.pub_sub import Subscriber

class SpeedGauge(MainGauge, Subscriber):
    """
        A gauge that displays any kind of information.
        It contains a title and three data fields.
        One large and two smaller ones.
    """

    
    def __init__(self, *args, **kwargs):
        MainGauge.__init__(self, *args, **kwargs)

    def update(self, pvt):
        self.history.insert(0, pvt)
        if len(self.history) > self.maxHistory:
            del self.history[-1]

        # Update Speed Gauge
        if len(self.history) > 2:
            round_speed = self.get_rounded_speed(self.history[0].gSpeed, self.history[1].gSpeed)
            self.update_values(value=(round(round_speed,1)))

        # Update Acceleration Gauge

        # Update Average Speed Gauge
        


    def get_rounded_speed(self, new_speed, old_speed):
        """
        get_rounded_speed
        """
        if old_speed is None:
            return new_speed
        
        return (new_speed+old_speed)/2.0
