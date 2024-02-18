import time
import ubinascii
import machine
from machine import Pin, I2C
from umqtt.simple import MQTTClient
import config
import utilities

utilities.connect_wifi(config.WIFI_SSID,config.WIFI_PASSWORD)


# Default MQTT server to connect to
SERVER = config.MQTT_BROKER
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = "test_topic"
MQTT_USER = config.MQTT_USER
MQTT_PASSWORD = config.MQTT_PASSWORD


def main(server=SERVER):
    c = MQTTClient(CLIENT_ID, server, user=MQTT_USER, password=MQTT_PASSWORD)
    
    c.connect()
    print("Connected to %s" % server)

    while True:
        print(f"Publishing to {TOPIC}")
        c.publish(TOPIC, "HELLO MQTT!")
        time.sleep_ms(1000)

    c.disconnect()

if __name__ == "__main__":
    main()