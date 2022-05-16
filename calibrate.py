#!/usr/bin/env python3
import datetime as dt
import time
import board
import busio
import adafruit_scd30

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

print("#####")

print("Measurement interval:", scd.measurement_interval)
print("Temperature offset:", scd.temperature_offset)
print("Ambient Pressure:", scd.ambient_pressure)
print("Altitude:", scd.altitude, "meters above sea level")
print("Self calibration enabled:", scd.self_calibration_enabled)
print("Forced recalibration reference:", scd.forced_recalibration_reference)

print("#####")

scd.forced_recalibration_reference = 409
time.sleep(3.0)
scd.self_calibration_enabled = False
time.sleep(3.0)

print("#####")

print("Self-calibration enabled:", scd.self_calibration_enabled)
print("Forced recalibration reference:", scd.forced_recalibration_reference)

while True:
    if scd.data_available:
        datetime = dt.datetime.now()
        timestamp = datetime.timestamp()
        CO2 = scd.CO2
        temperature = scd.temperature
        relative_humidity = scd.relative_humidity
        # Monitoring these settings shouldn't be necessary, but self calibration keeps getting automatically re-enabled
        self_calibration_enabled = scd.self_calibration_enabled
        forced_recalibration_reference = scd.forced_recalibration_reference
    
        print("{}  {:6.1f} ppm  {:4.1f} C  {:4.1f} %rH   Auto={}   Ref={}".format(datetime , CO2, temperature, relative_humidity, self_calibration_enabled, forced_recalibration_reference))
    
    time.sleep(0.5)
