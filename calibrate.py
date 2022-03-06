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

# scd.measurement_interval = 4
print("Measurement interval:", scd.measurement_interval)
# scd.temperature_offset = 10
print("Temperature offset:", scd.temperature_offset)
# scd.ambient_pressure = 1100
print("Ambient Pressure:", scd.ambient_pressure)
# scd.altitude = 100
print("Altitude:", scd.altitude, "meters above sea level")
# scd.forced_recalibration_reference = 409
print("Forced recalibration reference:", scd.forced_recalibration_reference)
# scd.self_calibration_enabled = True
print("Self calibration enabled:", scd.self_calibration_enabled)

print("#####")

scd.self_calibration_enabled = False
scd.forced_recalibration_reference = 409

print("#####")

# scd.forced_recalibration_reference = 409
print("Forced recalibration reference:", scd.forced_recalibration_reference)
# scd.self_calibration_enabled = False
print("Self-calibration enabled:", scd.self_calibration_enabled)

