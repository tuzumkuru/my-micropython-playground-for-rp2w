import time
import uasyncio as asyncio
import ubinascii
import machine
from machine import Pin, I2C
import config
from utilities import sync_time
import wifi
import json
from logger import log
import uos
from install_deps import check_missing_packages, install_packages


# Default MQTT server to connect to
MQTT_BROKER = config.MQTT_BROKER
CLIENT_ID = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
MQTT_TOPIC = CLIENT_ID + '/' + config.SENSOR_NAME

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
    # import hardware and MQTT modules locally so missing packages don't crash module import
    try:
        from bme680i import BME680_I2C
        from umqtt.simple import MQTTClient
    except Exception as e:
        log(f"Required modules not available: {e}. Ensure packages are installed and reboot.")
        # give logger a moment, then reboot to try provisioning path again
        await asyncio.sleep(1)
        machine.reset()

    bme = BME680_I2C(i2c)
    
    mqtt_client = None

    # Time settings
    start_time = time.time()
    previous_time = 0
    period = 0

    log(f"Starting loop at {start_time}")

    while True:
        current_time = time.time()
        
        if not mqtt_client:
            log(f"Connecting to the mqtt broker {MQTT_BROKER}")
            try:
                mqtt_client = MQTTClient(**get_mqtt_broker_parameters(), keepalive=120)
                mqtt_client.connect()
            except Exception as e:
                log(f"Error connecting to MQTT: {e}", file_path=LOG_FILE_PATH)
                mqtt_client = None # Reset client on connection error
                await asyncio.sleep(5) # Wait before retrying
                continue

        if current_time - previous_time >= DATA_SEND_PERIOD: 
            try:
                bme_data = await get_sensor_data(bme)        
                bme_data["timestamp"] = time.time()
                log(f"{current_time - previous_time} seconds passed. Sending data to {MQTT_TOPIC}")
                mqtt_client.publish(MQTT_TOPIC, json.dumps(bme_data))
                log(f"Data sent!")
                previous_time = current_time
            except OSError as e:
                # Handle connection error
                log(f"Error occurred while sending data: {e}", file_path=LOG_FILE_PATH)
                if mqtt_client:
                    try:
                        mqtt_client.disconnect()
                    except Exception as ex:
                        log(f"Error disconnecting MQTT client: {ex}", file_path=LOG_FILE_PATH)
                mqtt_client = None # Reset client to trigger reconnection
                
                if not wlan.is_connected():
                    log("No internet connection. Trying to connect again!")
                    reconnected = await wlan.connect_async(config.WIFI_SSID, config.WIFI_PASSWORD)
                    if not reconnected:
                        log("Reconnection attempt failed — rebooting device to retry.", file_path=LOG_FILE_PATH)
                        await asyncio.sleep(1)
                        machine.reset()

            except Exception as e:
                log(f"Other error occurred while sending data: {e}", file_path=LOG_FILE_PATH)

        await asyncio.sleep(1)

async def main():
    log("Starting program.")

    tasks = []
    tasks.append(asyncio.create_task(task_flash_led()))

    # Try to connect and reboot if we fail to obtain a connection.
    connected = await wlan.connect_async(config.WIFI_SSID, config.WIFI_PASSWORD)
    if not connected:
        log("Wi-Fi connect attempt failed — rebooting device to retry.")
        # small delay to flush logs
        await asyncio.sleep(1)
        machine.reset()

    sync_time()
    
    # After syncing time, ensure required packages are installed only on first boot.
    try:
        if check_missing_packages is not None and install_packages is not None:
            MARKER_PATH = "installed_once.flag"
            first_boot = False
            try:
                uos.stat(MARKER_PATH)
                first_boot = False
            except Exception:
                first_boot = True

            if first_boot:
                log("First boot detected: checking for missing packages")
                missing = check_missing_packages()
                if missing:
                    log(f"Missing packages detected: {missing}")
                    results = install_packages(packages=missing)
                    for pkg, status in results.items():
                        if status is True:
                            log(f"Installed {pkg}")
                        else:
                            log(f"Failed to install {pkg}: {status}")
                else:
                    log("All required packages are already installed.")

                # write marker so we don't attempt again
                try:
                    with open(MARKER_PATH, "w") as mf:
                        mf.write("installed\n")
                except Exception as e:
                    log(f"Failed to write install marker: {e}")
            else:
                log("Install marker present; skipping package installation.")
    except Exception as e:
        log(f"Error while checking/installing packages: {e}")
    
    tasks.append(asyncio.create_task(task_main()))

    await asyncio.gather(*tasks)    


if __name__ == "__main__":
  asyncio.run(main())
