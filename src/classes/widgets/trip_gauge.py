"""File containing a class for the main gauge."""
from tkinter import font, Label, Frame
from classes.widgets.main_gauge import MainGauge
from classes.pub_sub import Subscriber
from geopy.distance import vincenty


class TripGauge(MainGauge, Subscriber):
    """
        A gauge that displays the speed, acceleration and average speed.
    """

    def __init__(self, app, *args, **kwargs):
        MainGauge.__init__(self, *args, **kwargs)
        self.app = app
        self.sub_gauge1_label.config(text="00:00")
        self.sub_gauge2_label.config(text="00:00")

    def update(self, message, pvt):
        history = self.app.get_history("UBX-NAV-PVT")
        last_gps_msg = None
        
        if history is not None and len(history) > 0:
            last_gps_msg = history[0]

        distance = self.app.get_distance()
        
        if distance < 1.0:
            self.update_values(value=str(int(distance*1000)) + " m")
        elif round(distance,2) >= 1.0 and round(distance,2) < 100.0:
            self.update_values(value="{0:.2f}".format(distance))
        else:
            self.update_values(value="{0:.1f}".format(distance))
        if self.app.get_start_date() is not None:
            if pvt.getDate() < self.app.get_start_date():
                self.update_values(subvalue='00:00')
                return
            on_seconds = (pvt.getDate()-self.app.get_start_date()).total_seconds()
            hours, remainder = divmod(on_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            if on_seconds > 3600:
                self.update_values(subvalue='%02d:%02d:%02d' % (hours, minutes, seconds))
            else:
                self.update_values(subvalue='%02d:%02d' % (minutes, seconds))

        if self.app.get_engine_start_time() is not None and self.app.get_engine_running() == True:
            if last_gps_msg is not None:
                total_seconds = self.app.get_engine_run_seconds()+(last_gps_msg.getDate()-self.app.get_engine_start_time()).total_seconds()
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                if total_seconds > 3600:
                    self.update_values(subvalue2='%02d:%02d:%02d' % (hours, minutes, seconds))
                else:
                    self.update_values(subvalue2='%02d:%02d' % (minutes, seconds))

