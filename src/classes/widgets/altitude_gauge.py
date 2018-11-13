"""File containing a class for the main gauge."""
from tkinter import font, Label, Frame
from classes.widgets.main_gauge import MainGauge
from classes.pub_sub import Subscriber
import datetime

class AltitudeGauge(MainGauge, Subscriber):
    """
        A gauge that displays the speed, acceleration and average speed.
    """
    altitude_round_count = 3
    partial_time = datetime.time(6, 50)
    total_time = datetime.time(6, 59)
    partial_distance = 31.5
    total_distance = 39.1
    def __init__(self, app, *args, **kwargs):
        MainGauge.__init__(self, *args, **kwargs)
        self.app = app

    def update(self, message, pvt):
        gpsHistory = self.app.get_history(message)
        if pvt.valid.validTime or pvt.valid.validDate:
            partial_target_time = self.get_time(pvt.getDate(), self.partial_time)
            total_target_time = self.get_time(pvt.getDate(), self.total_time)
            partial_speed = self.getTargetSpeed(pvt.getDate(), self.partial_distance, partial_target_time)
            total_speed = self.getTargetSpeed(pvt.getDate(), self.total_distance, total_target_time)
            
            self.display_total_speed(total_speed)
            self.display_partial_speed(partial_speed)
        
        if gpsHistory is None and len(gpsHistory) == 0:
            return

        if not gpsHistory[0].flags.gnssFixOK:
            return

        if len(gpsHistory) > 1:
            self.update_values(value=round(self.get_rounded_speed(gpsHistory),1))

    def display_total_speed(self, speed):
        if speed is not None:
            self.update_values(subvalue="{0:.2f}".format(round(speed,2)))
        else:
            self.update_values(subvalue="--.-")
    
    def display_partial_speed(self, speed):
        if speed is not None:
            self.update_values(subvalue2="{0:.2f}".format(round(speed,2)))
        else:
            self.update_values(subvalue2="--.-")


    def getTargetSpeed(self, current_date, distance, end_time):
        diff = end_time-current_date
        time_diff = diff.total_seconds()/60.0/60.0
        km_diff = distance - self.app.get_distance()

        if time_diff > 0:
            speed = km_diff/time_diff
            if current_date < end_time and speed < 150:
                return speed

    def get_time(self, currDate, time):
        if time is None or currDate is None:
            return
        day = datetime.date(currDate.year, currDate.month, currDate.day)
        target_time = datetime.datetime.combine(day, time)
        return target_time


    def get_rounded_speed(self, history):

        value_count = min(self.altitude_round_count, len(history))
        
        totalSpeed = 0.0
        
        for value in range(value_count):
            totalSpeed += history[value].hMSL

        if value_count == 0.0:
            return 0.0
        return totalSpeed/value_count