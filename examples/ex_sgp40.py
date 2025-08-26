import time
from machine import I2C, Pin
import micropython_sgp40

# If you have a temperature sensor, like the bme280, import that here as well
# import adafruit_bme280

i2c = I2C(0)
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sgp = micropython_sgp40.SGP40(i2c)
# And if you have a temp/humidity sensor, define the sensor here as well
# bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

while True:
    print("Raw Gas: ", sgp.raw)
    # Lets quickly grab the humidity and temperature
    # temperature = bme280.temperature
    # humidity = bme280.relative_humidity
    # compensated_raw_gas = sgp.measure_raw(temperature = temperature, relative_humidity = humidity)
    print("")
    time.sleep(1)