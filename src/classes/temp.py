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

        self.calculateAverageSpeed(pvt)
        self.oldOldPvt = self.oldPvt
        self.oldPvt = pvt
        



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
