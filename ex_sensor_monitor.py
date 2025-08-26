import asyncio
import statistics
from machine import I2C
from machine import Pin
from bme688 import *

async def get_sensor_data(bme):
    return {
    "temperature": bme.temperature,
    "pressure": bme.pressure,
    "humidity": bme.humidity,
    "gas": bme.gas
    }

class SensorMonitor:
    def __init__(self, bme, time_interval=10, deviation_threshold=1):
        self.bme = bme
        self.time_interval = time_interval  # seconds between readings
        self.deviation_threshold = deviation_threshold  # standard deviations from mean to consider change

        self.data = {
            "temperature": [],
            "pressure": [],
            "humidity": [],
            "gas": []
        }

    async def get_sensor_data(self):
        while True: # Continuously gather data
            sensor_data = await get_sensor_data(self.bme)
            for key in self.data.keys():
                self.data[key].append(sensor_data[key])

            # Check if latest reading is outside standard deviation for each variable
            for key, values in self.data.items():
                if len(values) > 1: # Need at least two points to calculate standard deviation
                    mean = statistics.mean(values)
                    std_dev = statistics.stdev(values)
                    if abs(values[-1] - mean) > self.deviation_threshold * std_dev:
                        print(f"Significant change in {key}: {values[-1]}")

            await asyncio.sleep(self.time_interval)

async def main():
    i2c = I2C(0, sda=Pin(4), scl=Pin(5))
    bme = BME680_I2C(i2c)
    monitor = SensorMonitor(bme)
    await monitor.get_sensor_data()

if __name__ == "__main__":
    asyncio.run(main())