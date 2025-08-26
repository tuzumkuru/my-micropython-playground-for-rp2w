import math
import time
from machine import I2C
from machine import Pin
from bme688 import *


class RunningStats:
    def __init__(self):
        self.n = 0
        self.mean = 0.0
        self.M2 = 0.0

    def update(self, x):
        self.n += 1
        delta = x - self.mean
        self.mean += delta / self.n
        delta2 = x - self.mean
        self.M2 += delta * delta2

    def variance(self):
        if self.n < 2:
            return float('nan')
        return self.M2 / (self.n - 1)

    def standard_deviation(self):
        return math.sqrt(self.variance())

# Function to generate random sensor data
def get_sensor_data():
    # Simulate getting sensor data (replace this with actual sensor data retrieval)
    return bme.temperature  # Generate a random data point between 0 and 100

# Define threshold for significant change (e.g., two standard deviations)
threshold_multiplier = 2

# Initialize running statistics
stats = RunningStats()

i2c = I2C(0, sda=Pin(4), scl=Pin(5))

bme = BME680_I2C(i2c)

previous_sensor_value = 0

while True:
    # Example sensor data retrieval (replace with actual data retrieval)
    sensor_value = get_sensor_data()

    print(f"Got sensor data: {sensor_value}")

    # Update running statistics
    stats.update(sensor_value)

    # Calculate standard deviation
    std_dev = stats.standard_deviation()

    print(f"std_dev: {std_dev}")

    # Calculate threshold
    threshold = threshold_multiplier * std_dev

    # Function to check for significant change
    def is_significant_change(current_value, previous_value, threshold):
        return abs(current_value - previous_value) > threshold

    # Check for significant change
    if stats.n > 1 and is_significant_change(sensor_value, previous_sensor_value, threshold):
        print("Significant change detected:", sensor_value)
        # Send data or take appropriate action

    previous_sensor_value = sensor_value

    # Wait for 1 second before getting next sensor data
    time.sleep(1)
