import time
import uasyncio as asyncio
import ubinascii
import machine
from machine import Pin, I2C
from umqtt.simple import MQTTClient
from bme688 import *
import config
from utilities import sync_time
import wifi
import json
from logger import log


# Default MQTT server to connect to
MQTT_BROKER = config.MQTT_BROKER
CLIENT_ID = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
MQTT_TOPIC = CLIENT_ID + '/' + "BME688"

LOG_FILE_PATH = "log.log"

def get_mqtt_broker_parameters():
    MQTT_ARGS = {
    'client_id': ubinascii.hexlify(machine.unique_id()).decode('utf-8'),
    'server': config.MQTT_BROKER
    }

    if hasattr(config, 'MQTT_PORT') and config.MQTT_PORT:
        MQTT_ARGS['port'] = config.MQTT_PORT

    if hasattr(config, 'MQTT_USER') and config.MQTT_USER:
        MQTT_ARGS['user'] = config.MQTT_USER

    if hasattr(config, 'MQTT_USER') and config.MQTT_PASSWORD:
        MQTT_ARGS['password'] = config.MQTT_PASSWORD

    return MQTT_ARGS

DATA_SEND_PERIOD = 60

wlan = wifi.WiFi()

async def task_flash_led():
    led = Pin('LED', Pin.OUT)
    BLINK_DELAY_MS_FAST = const(500)
    BLINK_DELAY_MS_SLOW = const(1000)
    while True:
        led.toggle()
        if wlan.is_connected():
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
    
    mqtt_client = MQTTClient(**get_mqtt_broker_parameters(), keepalive=120)

    mqtt_client.connect()

    # Time settings
    start_time = time.time()
    previous_time = 0
    period = 0

    log(f"Starting loop at {start_time}")

    while True:
        current_time = time.time()
        
        if current_time - previous_time >= DATA_SEND_PERIOD: 
            try:
                bme_data = await get_sensor_data(bme)        
                bme_data["timestamp"] = time.time()
                log(f"{current_time - previous_time} seconds passed. Sending data to {MQTT_TOPIC}!")
                mqtt_client.publish(MQTT_TOPIC, json.dumps(bme_data))
                log(f"Data sent!")
                previous_time = current_time
            except OSError as e:
                # Handle connection error
                log(f"Error occurred while sending data: {e}", file_path=LOG_FILE_PATH)
                if not wlan.is_connected:
                    log("No internet connection. Trying to connect again!")
                    wifi = await wlan.connect_async(config.WIFI_SSID,config.WIFI_PASSWORD)
                log(f"Reconnecting to mqtt_client!", file_path=LOG_FILE_PATH)
                try:
                    mqtt_client.connect(False)
                except Exception as e:
                    log(f"Error connecting: {e}", file_path=LOG_FILE_PATH)
            except Exception as e:
                log(f"Other error occurred while sending data: {e}", file_path=LOG_FILE_PATH)

        await asyncio.sleep(1)

    mqtt_client.disconnect()

async def main():
    log("Starting program.")

    tasks = []
    tasks.append(asyncio.create_task(task_flash_led()))

    await wlan.connect_async(config.WIFI_SSID,config.WIFI_PASSWORD)

    sync_time()
    
    tasks.append(asyncio.create_task(task_main()))

    await asyncio.gather(*tasks)    


if __name__ == "__main__":
  asyncio.run(main())
