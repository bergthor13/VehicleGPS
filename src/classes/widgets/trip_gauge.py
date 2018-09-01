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

    def update(self, message, pvt):
        history = self.app.get_history("UBX-NAV-PVT")
        last_gps_msg = None
        if history is not None and len(history) > 0:
            last_gps_msg = history[0]

        distance = self.app.get_distance()
        if distance < 1.0:
            self.update_values(value=str(int(distance*1000)) + " m")
        else:
            self.update_values(value=round(distance,2))
        if self.app.get_start_date() is not None:
            on_seconds = (pvt.getDate()-self.app.get_start_date()).total_seconds()
            hours, remainder = divmod(on_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            if on_seconds > 3600:
                self.update_values(subvalue='%02d:%02d:%02d' % (hours, minutes, seconds))
            else:
                self.update_values(subvalue='%02d:%02d' % (minutes, seconds))

        if self.app.get_engine_start_time() is not None and self.app.get_engine_running() == True:
            print("WOO")
            print(last_gps_msg)
            if last_gps_msg is not None:
                print("lastgps")
                total_seconds = self.app.get_engine_run_seconds()+(last_gps_msg.getDate()-self.app.get_engine_start_time()).total_seconds()
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                if total_seconds > 3600:
                    print("total_secs")
                    self.update_values(subvalue2='%02d:%02d:%02d' % (hours, minutes, seconds))
                else:
                    print("else_total")
                    self.update_values(subvalue2='%02d:%02d' % (minutes, seconds))

