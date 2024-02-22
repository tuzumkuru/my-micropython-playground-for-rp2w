import network
import uasyncio as asyncio
import time
from logger import log

class WiFi:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self, ssid, password):
        log(f"Connecting to {ssid}")
        self.wlan.active(True)  # Activate the interface
        try:
            if not self.is_connected():
                self.wlan.connect(ssid, password)
                while not self.is_connected():
                    log(f"Waiting for connection to {ssid}")
                    time.sleep(1)
            log(f"Wi-Fi connected: {self.wlan.ifconfig()}")
        except Exception as e:
            log(f"Error occurred while connecting: {e}")

    async def connect_async(self, ssid, password):
        log(f"Connecting to {ssid}")
        self.wlan.active(True)  # Activate the interface
        await asyncio.sleep(1)
        try:
            if not self.is_connected():
                self.wlan.connect(ssid, password)
                while not self.wlan.isconnected():
                    log(f"Waiting for connection to {ssid}")
                    log(f"State is {self.wlan.status()}")
                    await asyncio.sleep(1)
            log(f"Wi-Fi connected: {self.wlan.ifconfig()}")
        except Exception as e:
            log(f"Error occurred while connecting asynchronously: {e}")

    def is_connected(self):
        return self.wlan.isconnected()

    def disconnect(self):
        try:
            self.wlan.disconnect()
        except Exception as e:
            log(f"Error occurred while disconnecting: {e}")

    def scan(self):
        try:
            return self.wlan.scan()
        except Exception as e:
            log(f"Error occurred while scanning: {e}")
            return []

    def get_ip(self):
        try:
            return self.wlan.ifconfig()[0]
        except Exception as e:
            log(f"Error occurred while getting IP address: {e}")
            return None
