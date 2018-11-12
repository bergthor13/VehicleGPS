"""File containing a class for the main gauge."""
from tkinter import font, Label, Frame
from classes.widgets.main_gauge import MainGauge
from classes.pub_sub import Subscriber


class MiscGauge(MainGauge, Subscriber):
    """
        A gauge that displays the speed, acceleration and average speed.
    """

    def __init__(self, app, *args, **kwargs):
        MainGauge.__init__(self, *args, **kwargs)
        self.app = app

    def update(self, message, value):
        if message == "OBD-RPM":
            if value is None:
                self.update_values(value="--%")
            else:

                history = self.app.get_history("UBX-NAV-PVT")
                if history is not None and len(history) > 0:
                    gear = self.getCurrentGear(history[0].gSpeed, value)
                    self.update_values(value=gear)
                else:
                    self.update_values(value="-")

        if message == "OBD-AMBIANT_AIR_TEMP":
            if value is None:
                self.update_values(subvalue="--°C")
            else:
                self.update_values(subvalue=str(int(value))+"°C")

        if message == "OBD-THROTTLE_POS":
            if value is None:
                self.update_values(subvalue2="----")
            else:
                mapped = self.translate(value, 11.372549019607844, 78.03921568627452, 0, 100)
                self.update_values(subvalue2=str(int(mapped))+"%")

    def getCurrentGear(self, speed, rpm):
        if rpm == 0.0:
            return "N"
        
        ratio = (speed/rpm)*100.0

        if (0.65 < ratio and ratio < 1.0) and speed > 5:
            return "1"
        elif (1.1 < ratio and ratio < 1.6) and speed > 9:
            return "2"
        elif (1.75 < ratio and ratio < 2.2) and speed > 13:
            return "3"
        elif (2.3 < ratio and ratio < 2.8) and speed > 19:
            return "4"
        elif (3.2 < ratio and ratio < 3.6) and speed > 25:
            return "5"
        else:
            return "N"

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)