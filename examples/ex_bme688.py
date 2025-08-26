from machine import I2C
from machine import Pin
from bme688 import *


i2c = I2C(0, sda=Pin(4), scl=Pin(5))

bme = BME680_I2C(i2c)

while True:
    # Get sensor data
    temperature = bme.temperature
    pressure = bme.pressure
    humidity = bme.humidity
    gas = bme.gas
    # Output data
    print("Temperature: {:.2f} °C".format(temperature))
    print("Pressure: {:.2f} hPa".format(pressure))
    print("Humidity: {:.2f} %".format(humidity))
    print("Gas: {:.2f} kOhms".format(gas))
    # Wait for a second before reading again
    time.sleep(1)
