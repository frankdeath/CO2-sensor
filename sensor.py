#!/usr/bin/env python3

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
        self.timestamp = None
        self.CO2 = None
        self.temperature = None
        self.relative_humidity = None
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
                self.timestamp = "{}".format(dt.datetime.now())
                self.CO2 = self.scd.CO2
                self.temperature = self.scd.temperature
                self.relative_humidity = self.scd.relative_humidity
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
            print("{}  {:6.1f} ppm  {:4.1f} C  {:4.1f} %rH".format(self.timestamp, self.CO2, self.temperature, self.relative_humidity))

    def quit(self):
        self.done = True


if __name__ == '__main__':
    sensorObj = Sensor()
    sensorObj.printConfig()
    while True:
        try:
            sensorObj.printData()
            time.sleep(2.0)
        except KeyboardInterrupt:
            sensorObj.quit()
            time.sleep(2.0)
            break

