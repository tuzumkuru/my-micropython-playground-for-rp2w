import network
import uasyncio as asyncio
import time
from logger import log

class WiFi:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        

    def connect(self, ssid, password):
        log(f"Connecting to {ssid}")
        self.wlan.active(True)       # activate the interface
        if not self.is_connected(): # check if the station is connected to an AP
            self.wlan.connect(ssid, password) # connect to an AP
            while not self.is_connected():
                log(f"Waiting for connection to {ssid}")
                time.sleep(1)
        log(f"Wi-Fi connected: {self.wlan.ifconfig()}")
        return self.wlan

    async def connect_async(self, ssid, password):
        log(f"Connecting to {ssid}")
        self.wlan.active(True)       # activate the interface
        await asyncio.sleep(1)
        if not self.is_connected(): # check if the station is connected to an AP
            self.wlan.connect(ssid, password) # connect to an AP
            while not self.wlan.isconnected():
                log(f"Waiting for connection to {ssid}")
                log(f"State is {self.wlan.status()}")
                await asyncio.sleep(1)
        log(f"Wi-Fi connected: {self.wlan.ifconfig()}")
        return self.wlan

    def is_connected(self):
        return self.wlan.isconnected()

    def disconnect(self):
        self.wlan.disconnect()

    def scan(self):
        return self.wlan.scan()
        

    def get_ip(self):
        return self.wlan.ifconfig()[0]
