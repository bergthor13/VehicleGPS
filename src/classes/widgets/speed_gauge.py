"""File containing a class for the main gauge."""
from tkinter import font, Label, Frame
from classes.widgets.main_gauge import MainGauge
from classes.pub_sub import Subscriber
from classes.data.pvt import PVT
from geopy.distance import vincenty
from datetime import timedelta


class SpeedGauge(MainGauge, Subscriber):
    """
        A gauge that displays the speed, acceleration and average speed.
    """

    speed_round_count = 4

    def __init__(self, app, *args, **kwargs):
        MainGauge.__init__(self, *args, **kwargs)
        self.app = app

    def update(self, message, pvt):
        gpsHistory = self.app.get_history(message)
        
        if not gpsHistory:
            return

        if len(gpsHistory) > 2:
            round_speed = self.get_rounded_speed(gpsHistory)
            acceleration = self.calculateAcceleration(gpsHistory, timedelta(seconds=1))
            average_speed = self.calculateAverageSpeed(self.app.get_distance(), self.app.get_start_date(), gpsHistory[0].getDate())
            if average_speed is not None:
                self.update_values(subvalue2="{0:.2f}".format(round(average_speed,2)))
            
            if round_speed > 0.5 and acceleration is not None:
                if acceleration < 0:
                    self.update_values(subvalue="-{0:.2f}".format(abs(acceleration)))
                else:
                    self.update_values(subvalue=" {0:.2f}".format(acceleration))
                self.update_values(value=(round(round_speed,1)))
            else:
                self.update_values(value=0.0, subvalue=" {0:.2f}".format(0.0))



    def get_rounded_speed(self, history):

        value_count = min(self.speed_round_count, len(history))
        
        totalSpeed = 0.0
        
        for value in range(value_count):
            totalSpeed += history[value].gSpeed

        if value_count == 0.0:
            return 0.0
        return totalSpeed/value_count

    def calculateAcceleration(self, history, interval):
        if history is None:
            return 0.0
        currentTime = history[0].getDate()
        history_by_interval = None
        for index, item in enumerate(history):
            if currentTime-interval <= history[index].getDate():
                history_by_interval = history[index]
        return history[0].gSpeed - history_by_interval.gSpeed

    def calculateAverageSpeed(self, distance, start, end):
        if not start or not end:
            return
        duration = ((end-start).microseconds+(end-start).seconds*1000000)/60/60/1000000
        if not(duration == 0):
            return distance/duration
        return 0.0