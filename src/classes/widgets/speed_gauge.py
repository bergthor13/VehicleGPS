"""File containing a class for the main gauge."""
from tkinter import font, Label, Frame
from classes.widgets.main_gauge import MainGauge
from classes.pub_sub import Subscriber
from classes.data.pvt import PVT
from datetime import timedelta

class SpeedGauge(MainGauge, Subscriber):
    """
        A gauge that displays the speed, acceleration and average speed.
    """

    speed_round_count = 2

    def __init__(self, app, *args, **kwargs):
        MainGauge.__init__(self, *args, **kwargs)
        self.app = app

    def update(self, message, pvt):
        gpsHistory = self.app.get_history(message)
        obd_speed_history = self.app.get_history("OBD-SPEED")
        curr_obd_speed = None
        if obd_speed_history is not None:
            if obd_speed_history:
                curr_obd_speed = obd_speed_history[0]

        if not gpsHistory:
            return

        if len(gpsHistory) > 2:
            filtered_speed = self.get_rounded_speed(gpsHistory)
            if pvt.fixType < 1 and curr_obd_speed is not None:
                filtered_speed = curr_obd_speed
            acceleration = self.calculateAcceleration(gpsHistory, timedelta(seconds=1), 3)
            average_speed = self.calculateAverageSpeed(self.app.get_distance(), self.app.get_start_date(), gpsHistory[0].getDate())
            if average_speed is not None:
                self.update_values(subvalue2="{0:.2f}".format(round(average_speed,2)))
            
            if filtered_speed > 0.5 and acceleration is not None:
                if acceleration < 0:
                    self.update_values(subvalue="-{0:.1f}".format(abs(acceleration)))
                else:
                    self.update_values(subvalue=" {0:.1f}".format(acceleration))
                if round(filtered_speed,1) < 100: 
                    self.update_values(value="{0:.1f}".format(filtered_speed))
                else:
                    self.update_values(value="{0:.0f}".format(filtered_speed))

            else:
                self.update_values(value=0.0, subvalue=" {0:.1f}".format(0.0))



    def get_rounded_speed(self, history):

        value_count = min(self.speed_round_count, len(history))
        
        totalSpeed = 0.0
        
        for value in range(value_count):
            totalSpeed += history[value].gSpeed

        if value_count == 0.0:
            return 0.0
        return totalSpeed/value_count

    def calculateAcceleration(self, history, interval, smoothing_count):
        if history is None:
            return 0.0
        if len(history) <= smoothing_count:
            return 0.0

        smoothedCurrSpeed = (history[0].gSpeed + history[1].gSpeed + history[2].gSpeed)/3
        smoothedOldSpeed = 0.0

        currentTime = history[0].getDate()
        history_by_interval = None

        for index, item in enumerate(history):
            if currentTime-interval <= item.getDate():
                history_by_interval = item
                if len(history) <= index + smoothing_count:
                    return 0.0
                smoothedOldSpeed = (history[index].gSpeed + history[index+1].gSpeed + history[index+2].gSpeed)/3
        acceleration = smoothedCurrSpeed - smoothedOldSpeed
        if acceleration > -0.1 and acceleration < 0.1:
            return 0.0
        return acceleration

    def calculateAverageSpeed(self, distance, start, end):
        if not start or not end:
            return
        duration = ((end-start).microseconds+(end-start).seconds*1000000)/60/60/1000000
        if not(duration == 0):
            return distance/duration
        return 0.0
