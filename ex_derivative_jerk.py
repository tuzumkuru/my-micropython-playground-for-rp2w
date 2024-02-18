# Import necessary modules
import time
import uasyncio as asyncio
import network
import ubinascii
import machine
from machine import Pin, I2C
from umqtt.simple import MQTTClient
from bme688 import *
import config
import utilities
from utilities import DerivativeAndJerkCalculator
import math
import json

# Default MQTT server to connect to
MQTT_BROKER = config.MQTT_BROKER
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_TOPIC = config.MQTT_TOPIC
MQTT_USER = config.MQTT_USER
MQTT_PASSWORD = config.MQTT_PASSWORD

# Function to calculate average
def calculate_average(data):
    return sum(data) / len(data)

async def get_sensor_data(bme):
    return {
    "temperature": bme.temperature,
    "pressure": bme.pressure,
    "humidity": bme.humidity,
    "gas": bme.gas
    }

def calculate_period(data, derivative, jerk, derivative_threshold, jerk_threshold):
    immediate_period = 0
    high_dramaticity_period = 10
    normal_period = 60

    if(derivative is None or jerk is None):
        return immediate_period, 0, 0


    derivative_magnitude = math.sqrt(sum(value ** 2 for value in derivative.values()))
    jerk_magnitude = math.sqrt(sum(value ** 2 for value in jerk.values()))

    # print(derivative_magnitude, jerk_magnitude)

    if derivative_magnitude > derivative_threshold or jerk_magnitude > jerk_threshold:
        return immediate_period, derivative_magnitude, jerk_magnitude
    elif derivative_magnitude > derivative_threshold and jerk_magnitude > jerk_threshold:
        return high_dramaticity_period, derivative_magnitude, jerk_magnitude
    else:
        return normal_period, derivative_magnitude, jerk_magnitude


# Main function to run the asyncio event loop
async def main():
    print("Starting program.")

    wifi = utilities.connect_wifi(config.WIFI_SSID,config.WIFI_PASSWORD)

    utilities.sync_time()
    
    print(f"Connecting to the mqtt broker {MQTT_BROKER}")
    mqtt_client = MQTTClient(CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
    mqtt_client.connect()

    print(f"Setting up I2C and BME Sensor")
    i2c = I2C(0, sda=Pin(4), scl=Pin(5))
    bme = BME680_I2C(i2c)

    print(f"Creating Derivative and Jerk Calculator")
    calculator = DerivativeAndJerkCalculator()

        # Time settings
    start_time = time.time()
    previous_time = start_time
    period = 0

    print(f"Starting loop at {start_time}")
    while True:
        current_time = time.time()

        bme_data = await get_sensor_data(bme)
        derivative, jerk = await calculator.calculate_derivative_and_jerk(bme_data)
        print (bme_data)

        
        # Assuming bme_data is obtained from get_sensor_data(bme)
        
        # Filter out 'gas' key from bme_data
        bme_data_filtered = {key: value for key, value in bme_data.items() if key != 'gas'}
        if derivative is not None and jerk is not None:
            derivative_filtered = {key: value for key, value in derivative.items() if key != 'gas'}
            jerk_filtered = {key: value for key, value in jerk.items() if key != 'gas'}
            period, derivative_magnitude, jerk_magnitude = calculate_period(bme_data_filtered, derivative_filtered, jerk_filtered, 0.1, 0.05)
            mqtt_client.publish("derivative", json.dumps(derivative))
            mqtt_client.publish("jerk", json.dumps(jerk))
            mqtt_client.publish("derivative_magnitude", json.dumps(derivative_magnitude))
            mqtt_client.publish("jerk_magnitude", json.dumps(jerk_magnitude))
        
        # Call calculate_period with the filtered bme_data
        
        if current_time-previous_time >= period: 
            print(f"{current_time-previous_time} seconds passed. Sending data!")
            mqtt_client.publish(MQTT_TOPIC, json.dumps(bme_data))
            previous_time = current_time



        await asyncio.sleep(1)

    mqtt_client.disconnect()

# Run the event loop
loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()