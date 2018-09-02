"""File containing a class for the main gauge."""
from tkinter import font, Label, Frame
from classes.widgets.main_gauge import MainGauge
from classes.pub_sub import Subscriber
from geopy.distance import vincenty


class SpeedGauge(MainGauge, Subscriber):
    """
        A gauge that displays the speed, acceleration and average speed.
    """

    def __init__(self, app, *args, **kwargs):
        MainGauge.__init__(self, *args, **kwargs)
        self.app = app

    def update(self, message, pvt):
        gpsHistory = self.app.get_history(message)
        
        if not gpsHistory:
            return

        if len(gpsHistory) > 2:
            round_speed = self.get_rounded_speed(gpsHistory[0].gSpeed, gpsHistory[1].gSpeed)
            acceleration = self.calculateAcceleration(gpsHistory[2], gpsHistory[1], gpsHistory[0])
            average_speed = self.calculateAverageSpeed(self.app.get_distance(), self.app.get_start_date(), gpsHistory[0].getDate())
            if round_speed > 0.5:
                self.update_values(value=(round(round_speed,1)),
                                   subvalue=round(acceleration,2),
                                   subvalue2=round(average_speed,2))
            else:
                self.update_values(value=0.0, subvalue=0.0, subvalue2=0.0)
        


    def get_rounded_speed(self, new_speed, old_speed):
        """
        get_rounded_speed
        """
        if old_speed is None:
            return new_speed
        
        return (new_speed+old_speed)/2.0

    def calculateAcceleration(self, oldOldPvt, oldPvt, pvt):
        if oldOldPvt is None or oldPvt is None or pvt is None:
            return 0.0
        
        time1 = oldOldPvt.getDate()
        time2 = oldPvt.getDate()
        time3 = pvt.getDate()

        timDiff1 = (time3-time2).total_seconds()
        timDiff2 = (time2-time1).total_seconds()

        disDiff1 = vincenty((oldOldPvt.lat, oldOldPvt.lon), (oldPvt.lat, oldPvt.lon)).meters
        disDiff2 = vincenty((oldPvt.lat, oldPvt.lon), (pvt.lat, pvt.lon)).meters
        spdDiff1 = disDiff1/timDiff1 
        spdDiff2 = disDiff2/timDiff2

        if (time1-time3).total_seconds() != 0.0:
            return ((spdDiff2-spdDiff1)/(time3-time1).total_seconds())*3.6
        else:
            return 0.0

    def calculateAverageSpeed(self, distance, start, end):
        if not start or not end:
            return
        duration = (end-start).seconds/60/60
        if not(duration == 0):
            return (distance/1000)/duration
        return 0.0