"""File containing a class for the main gauge."""
from tkinter import font, Label, Frame
from classes.widgets.main_gauge import MainGauge
from classes.pub_sub import Subscriber
from geopy.distance import vincenty
import time



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
        elif int(distance) >= 1000:
            self.update_values(value=str(int(distance)))
        else:
            self.update_values(value="{0:.1f}".format(distance))

        on_seconds = 0.0

        if self.app.get_start_date() is None or not(pvt.valid.validDate and pvt.valid.validTime):
            on_seconds = time.time()-self.app.get_time_since_start()
        else:
            on_seconds = (pvt.getDate()-self.app.get_start_date()).total_seconds()

        interval = self.get_formatted_interval(on_seconds)
        self.update_values(subvalue=interval)


        if self.app.get_engine_start_time() is not None and self.app.get_engine_running() is True:
            prev_engine_time = self.app.get_engine_run_seconds()
            curr_engine_time = time.time()-self.app.get_engine_start_time()
            engine_interval = self.get_formatted_interval(prev_engine_time + curr_engine_time)
            self.update_values(subvalue2=engine_interval)

    def get_formatted_interval(self, total_seconds):
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if total_seconds <= 3600:
            return '%02d:%02d' % (minutes, seconds)
        
        return '%02d:%02d:%02d' % (hours, minutes, seconds)

