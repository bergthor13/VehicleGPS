        speedGauge = None
    satelliteGauge = None
    consumptionGauge = None
    altitudeGauge = None
    distanceGauge = None
    engineGauge = None

	def updatePVT(self, pvt):
        """
        updatePVT
        """
        if self.status_bar is None:
            return
        
        if (self.speedGauge is None or
            self.satelliteGauge is None or
            self.altitudeGauge is None):
            return
        
        self.setDate(pvt.valid, pvt.getDate())
        if not pvt.flags.gnssFixOK:
            self.satelliteGauge.update_values(value=pvt.numSv, subvalue="EKKERT", subvalue2="MERKI")
        else:
            self.satelliteGauge.update_values(value=pvt.numSv, subvalue=str(round(pvt.hAcc, 2)) + ' m', subvalue2=str(round(pvt.pDop, 2)))

        if not pvt.flags.gnssFixOK:
            return

        if self.oldPvt is None:
            self.startDate = pvt.getDate()
            self.oldPvt = pvt
            return
        roundedSpeed = self.get_rounded_speed(pvt.gSpeed)
        if pvt.fixType >= 1:
            if roundedSpeed > 0.5:
                traveledDistance = vincenty((self.oldPvt.lat, self.oldPvt.lon), (pvt.lat, pvt.lon)).meters
                self.distance += traveledDistance
                self.setSpeed(roundedSpeed)
                accel = self.calculateAcceleration(self.oldOldPvt, self.oldPvt, pvt)
                self.setAcceleration(accel)
            else:
                self.setSpeed(0.0)
                self.setAcceleration(0.0)
            
            avgSpeed = self.calculateAverageSpeed(pvt)
            self.setAverageSpeed(avgSpeed)

            
            self.altitudeGauge.update_values(value=round(pvt.hMSL, 1))
            onSeconds = (pvt.getDate()-self.startDate).total_seconds()
            hours, remainder = divmod(onSeconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            if onSeconds > 3600:
                self.distanceGauge.update_values(subvalue='%02d:%02d:%02d' % (hours, minutes, seconds))
            else:
                self.distanceGauge.update_values(subvalue='%02d:%02d' % (minutes, seconds))

        self.calculateAverageSpeed(pvt)
        self.oldOldPvt = self.oldPvt
        self.oldPvt = pvt
        
        if self.distance < 1000:
            self.distanceGauge.update_values(value=str(int(self.distance)) + " m")
        else:
            self.distanceGauge.update_values(value=round(self.distance/1000.0,1))

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

			    def setDate(self, valid, date):
        if valid.validDate:
            self.status_bar.set_date(date)

        if valid.validTime:
            self.status_bar.set_time(date)

    def setSpeed(self, speed):
        self.speedGauge.update_values(value=round(speed,1))

    def setAcceleration(self, acceleration):
        self.speedGauge.update_values(subvalue=round(acceleration,1))

    def setAverageSpeed(self, avgSpeed):
        self.speedGauge.update_values(subvalue2=round(avgSpeed,1))
    
    def setEngineTemp(self, temp):
        if self.engineGauge is None:
            return

        if temp is not None:
            self.engineGauge.update_values(subvalue=str(round(temp))+ "°C")
        else:
            self.engineGauge.update_values(subvalue="--°C")


    def setEngineLoad(self, load):
        if self.engineGauge is None:
            return

        if load is not None:
            self.engineGauge.update_values(value=str(round(load)) + "%")
        else:
            self.engineGauge.update_values(value="--%")

    def setEngineRPM(self, rpm):
        if self.engineGauge is None:
            return
        if self.consumptionGauge is None:
            return
        if self.distanceGauge is None:
            return
        
        if rpm is not None:
            self.engineGauge.update_values(subvalue2=str(round(rpm)))
            
            if self.oldPvt is not None:
                currentGear = self.getCurrentGear(self.oldPvt.gSpeed, rpm)
                self.consumptionGauge.update_values(value=currentGear)
            
            # Engine has started.
            if self.engineRunning == False and rpm != 0.0:
                if self.oldPvt is not None:
                    self.engineStartTime = self.oldPvt.getDate()
            
            # Engine has stopped
            if self.engineRunning == True and rpm == 0.0:
                if self.oldPvt is not None and self.oldPvt.getDate() is not None:
                    self.engineRunSeconds += (self.oldPvt.getDate()-self.engineStartTime).total_seconds()
            
            if rpm == 0.0:
                self.engineRunning = False
            else:
                self.engineRunning = True

            if self.engineStartTime is not None and self.engineRunning == True:
                if self.oldPvt is not None:
                    totalSeconds = self.engineRunSeconds+(self.oldPvt.getDate()-self.engineStartTime).total_seconds()
                    hours, remainder = divmod(totalSeconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    if totalSeconds > 3600:
                        self.distanceGauge.update_values(subvalue2='%02d:%02d:%02d' % (hours, minutes, seconds))
                    else:
                        self.distanceGauge.update_values(subvalue2='%02d:%02d' % (minutes, seconds))
        else:
            self.consumptionGauge.update_values(value="-")
            self.engineGauge.update_values(subvalue2="----")
            if self.engineRunSeconds == 0.0:
                self.distanceGauge.update_values(subvalue2="00:00")

    def setThrottlePos(self, throttle):
        if self.consumptionGauge is None:
            return

        if throttle is not None:
            self.consumptionGauge.update_values(subvalue2=str(round(throttle)) + "%")
        else:
            self.consumptionGauge.update_values(subvalue2="--%")


    def setVoltage(self, voltage):
        if self.engineGauge is None:
            return
        self.engineGauge.update_values(value=voltage)

    def setAmbientTemp(self, temp):
        if self.consumptionGauge is None:
            return
        if temp is not None:
            self.consumptionGauge.update_values(subvalue=str(round(temp))+ "°C")
        else:
            self.consumptionGauge.update_values(subvalue="--°C")


    def setMetric(self, metric, value):
        if metric == "COOLANT_TEMP":
            self.setEngineTemp(value)
        elif metric == "ENGINE_LOAD":
            self.setEngineLoad(value)
        elif metric == "RPM":
            self.setEngineRPM(value)
        elif metric == "AMBIANT_AIR_TEMP":
            self.setAmbientTemp(value)
        elif metric == "THROTTLE_POS":
            self.setThrottlePos(value)

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

    def calculateAverageSpeed(self, pvt):
        duration = (pvt.getDate()-self.startDate).seconds/60/60
        if not(duration == 0):
            return (self.distance/1000)/duration
        return 0.0

    engineStartTime = None
    engineRunSeconds = 0.0

	    oldPvt = None
    oldOldPvt = None
    distance = 0.0
    startDate = None
    engineRunning = False
