#!/usr/bin/env python3

import remi.gui as gui
from remi import start, App
import datetime as dt
import board
import busio
import adafruit_scd30
 
class MyApp(App):
    def __init__(self, *args):
        self.connect_sensor()
        super(MyApp, self).__init__(*args)
    
    def idle(self):
        self.update_clock()
        self.update_data()
    
    def connect_sensor(self):
        #
        #!self.i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=10000)
        self.scd = adafruit_scd30.SCD30(self.i2c)

    def main(self):
        # the margin '0px auto' centers the main container
        verticalContainer = gui.Container(width=540, margin='0px auto', style={'display': 'block', 'overflow': 'hidden'})
        
        # clock
        self.clockLabel = gui.Label('clock', width=200, height=30, margin='10px')
        
        # C02 (ppm)
        self.co2Label = gui.Label('co2', width=200, height=30, margin='10px')
        
        # Temperature (C)
        self.temperatureLabel = gui.Label('temperature', width=200, height=30, margin='10px')
        
        # Humidity (%rH)
        self.humidityLabel = gui.Label('humidity', width=200, height=30, margin='10px')
    
        verticalContainer.append([self.clockLabel, self.co2Label, self.temperatureLabel, self.humidityLabel])
        
        # return the root widget
        return verticalContainer

    def update_clock(self):
        self.clockLabel.set_text("{}".format(dt.datetime.now()))

    def update_data(self):
        if self.scd.data_available:
            self.co2Label.set_text("{:6.1f} ppm CO2".format(self.scd.CO2))
            self.temperatureLabel.set_text("{:4.1f} ° C".format(self.scd.temperature))
            self.humidityLabel.set_text("{:4.1f} % rH".format(self.scd.relative_humidity))

    def on_close(self):
        """ Overloading App.on_close event to stop the Timer.
        """
        # disconnect from the sensor

        super(MyApp, self).on_close()


if __name__ == "__main__":
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True, address='0.0.0.0', port=8081, update_interval=1.0, multiple_instance=True)

