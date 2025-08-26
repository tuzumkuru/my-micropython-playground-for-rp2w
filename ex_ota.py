import network
import time
import ujson as json
from umqtt.simple import MQTTClient
import ubinascii
import urequests
import os
import config
import machine

# WiFi configuration
WIFI_SSID = config.WIFI_SSID
WIFI_PASSWORD = config.WIFI_PASSWORD

# MQTT configuration
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_BROKER = config.MQTT_BROKER
MQTT_TOPIC = b"firmware_updates"
MQTT_USER =  config.MQTT_USER
MQTT_PASSWORD = config.MQTT_PASSWORD

# Function to connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("Connected to WiFi:", wlan.ifconfig())

# Function to handle OTA updates
def perform_ota_update(update_url):
    print("Downloading firmware update...")
    response = urequests.get(update_url)
    if response.status_code == 200:
        with open('firmware_update.bin', 'wb') as f:
            f.write(response.content)
        print("Firmware update downloaded successfully.")
        # Perform update logic here (e.g., using machine.Flash().write())
        # Ensure to handle errors and cleanup
        # After successful update, you may need to reboot the device
    else:
        print("Failed to download firmware update:", response.status_code)

# Function to handle MQTT messages
def mqtt_callback(topic, msg):
    if topic == MQTT_TOPIC:
        print(msg)
        update_info = json.loads(msg)
        update_url = update_info.get("url")
        if update_url:
            perform_ota_update(update_url)
        else:
            print("Invalid update message:", msg)

# Main function
def main():
    connect_wifi()
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
    client.set_callback(mqtt_callback)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Subscribed to MQTT topic:", MQTT_TOPIC)
    
    try:
        while True:
            client.wait_msg()
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
