import time
import uasyncio as asyncio
import ubinascii
import machine
from machine import Pin, I2C
from umqtt.simple import MQTTClient
from bme688 import *
import config
from utilities import connect_wifi, sync_time
import math
import json
from logger import log



# Default MQTT server to connect to
MQTT_BROKER = config.MQTT_BROKER
CLIENT_ID = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
MQTT_TOPIC = CLIENT_ID + '/' + "BME688"
MQTT_USER = config.MQTT_USER
MQTT_PASSWORD = config.MQTT_PASSWORD

DATA_SEND_PERIOD = 60
wifi_connection = False


async def task_flash_led():
    led = Pin('LED', Pin.OUT)
    BLINK_DELAY_MS_FAST = const(200)
    BLINK_DELAY_MS_SLOW = const(500)
    while True:
        led.toggle()
        if wifi_connection:
            await asyncio.sleep_ms(BLINK_DELAY_MS_SLOW)
        else:
            await asyncio.sleep_ms(BLINK_DELAY_MS_FAST)

async def get_sensor_data(sensor):
    return {
        "temperature": sensor.temperature,
        "pressure": sensor.pressure,
        "humidity": sensor.humidity,
        "gas": sensor.gas
    }

# Main function to run the asyncio event loop
async def task_main():
    log("Setting up I2C and BME Sensor")
    i2c = I2C(0, sda=Pin(4), scl=Pin(5))
    bme = BME680_I2C(i2c)
    
    log(f"Connecting to the mqtt broker {MQTT_BROKER}")
    mqtt_client = MQTTClient(CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
    mqtt_client.connect()

    # Time settings
    start_time = time.time()
    previous_time = 0
    period = 0

    log(f"Starting loop at {start_time}")

    while True:
        current_time = time.time()
        
        if current_time-previous_time >= DATA_SEND_PERIOD: 
            bme_data = await get_sensor_data(bme)        
            bme_data["timestamp"] = time.time()
            log(f"{current_time-previous_time} seconds passed. Sending data!")
            mqtt_client.publish(MQTT_TOPIC, json.dumps(bme_data))
            previous_time = current_time

        await asyncio.sleep(1)

    mqtt_client.disconnect()

async def main():
    log("Starting program.")

    tasks = []
    tasks.append(asyncio.create_task(task_flash_led()))

    wifi = connect_wifi(config.WIFI_SSID,config.WIFI_PASSWORD)

    wifi_connection = wifi.isconnected()

    sync_time()
    
    tasks.append(asyncio.create_task(task_main()))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
  asyncio.run(main())
