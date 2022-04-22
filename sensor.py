#!/usr/bin/env python3

from collections import deque
import datetime as dt
import threading
import time
import board
import busio
import adafruit_scd30

class Sensor:
    '''
    Sensor class for the SCD30 C02 sensor
    '''
    def __init__(self):
        # SCD-30 has tempremental I2C with clock stretching, datasheet recommends
        # starting at 50KHz
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
        self.scd = adafruit_scd30.SCD30(self.i2c)
        # stuff that is only read once
        self.temperature_offset = self.scd.temperature_offset
        self.measurement_interval = self.scd.measurement_interval
        self.self_calibration_enabled = self.scd.self_calibration_enabled
        self.ambient_pressure = self.scd.ambient_pressure
        self.altitude = self.scd.altitude
        self.forced_recalibration_reference = self.scd.forced_recalibration_reference
        # stuff that will be polled
        self.datetime = None
        self.timestamp = None
        self.CO2 = None
        self.temperature = None
        self.relative_humidity = None
        #
        self.historySize = 60
        self.historyTS = deque([])
        self.historyCO2 = deque([])
        #
        self.poll_period = 1.0
        self.done = False
        # start the poller thread
        self._startPollerThread()

    def _startPollerThread(self):
        '''
        '''
        poller_thread = threading.Thread(target=self._poller)
        poller_thread.daemon = True
        poller_thread.start()

    def _poller(self):
        '''
        '''
        while self.done == False:
            data_available = self.scd.data_available
            if data_available:
                self.datetime = dt.datetime.now()
                self.timestamp = self.datetime.timestamp()
                self.CO2 = self.scd.CO2
                self.temperature = self.scd.temperature
                self.relative_humidity = self.scd.relative_humidity
                # Monitoring these settings shouldn't be necessary, but self calibration keeps getting automatically re-enabled
                self.self_calibration_enabled = self.scd.self_calibration_enabled
                self.forced_recalibration_reference = self.scd.forced_recalibration_reference
                # append the lastest reading
                self.historyTS.append(self.timestamp)
                self.historyCO2.append(self.CO2)
                if len(self.historyTS) > self.historySize:
                    # remove the oldest reading
                    self.historyTS.popleft()
                    self.historyCO2.popleft()
            time.sleep(self.poll_period)

        print()
        print("sensor poller quitting...")

    def printConfig(self):
        print("#####")
        # scd.temperature_offset = 10
        print("Temperature offset:", self.temperature_offset)
        
        # scd.measurement_interval = 4
        print("Measurement interval:", self.measurement_interval)
        
        # scd.self_calibration_enabled = True
        print("Self-calibration enabled:", self.self_calibration_enabled)
        
        # scd.ambient_pressure = 1100
        print("Ambient Pressure:", self.ambient_pressure)
        
        # scd.altitude = 100
        print("Altitude:", self.altitude, "meters above sea level")
        
        # scd.forced_recalibration_reference = 409
        print("Forced recalibration reference:", self.forced_recalibration_reference)
        print("#####")

    def printData(self):
        '''
        '''
        if self.CO2 != None:
            print("{}  {:6.1f} ppm  {:4.1f} C  {:4.1f} %rH".format(self.datetime , self.CO2, self.temperature, self.relative_humidity))

    def getDict(self):
        '''
        '''
        if self.CO2 != None:
            return {"timestamp":self.timestamp, "datetime":self.datetime.strftime("%Y-%m-%d %H:%M:%S"), "CO2":"{:.2f}".format(self.CO2), "temperature":"{:.2f}".format(self.temperature), "humidity":"{:.2f}".format(self.relative_humidity), "self_calibration":self.self_calibration_enabled , "calibration_reference":"{}".format(self.forced_recalibration_reference)}
        else:
            return {"timestamp":self.timestamp, "datetime":self.datetime.strftime("%Y-%m-%d %H:%M:%S")}

    def getHist(self):
        '''
        '''
        # Assume no one will load the web page in the 1st two seconds after starting the server
        return {"timestamps":list(self.historyTS), "values":list(self.historyCO2), "timestamp":self.timestamp, "datetime":self.datetime.strftime("%Y-%m-%d %H:%M:%S"), "CO2":"{:.2f}".format(self.CO2), "temperature":"{:.2f}".format(self.temperature), "humidity":"{:.2f}".format(self.relative_humidity), "self_calibration":self.self_calibration_enabled , "calibration_reference":"{}".format(self.forced_recalibration_reference)}

    def quit(self):
        self.done = True


if __name__ == '__main__':
    sensorObj = Sensor()
    sensorObj.printConfig()
    while True:
        try:
            sensorObj.printData()
            #print(sensorObj.getHist())
            time.sleep(2.0)
        except KeyboardInterrupt:
            sensorObj.quit()
            time.sleep(2.0)
            break

