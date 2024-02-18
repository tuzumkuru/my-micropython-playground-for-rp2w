import asyncio
from machine import Pin
import network
import config

print("Starting program.")

led = Pin('LED', Pin.OUT)

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface

async def connect_to_wifi(timeout=10):
    try:
        await asyncio.wait_for(_connect_to_wifi(), timeout)
        return True
    except asyncio.TimeoutError:
        print("Wi-Fi connection timed out.")
        return False

async def _connect_to_wifi():
    if not wlan.isconnected():
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    while not wlan.isconnected():
        await asyncio.sleep(1) 

    # Connected to WiFi
    print("Connected to WiFi!")
    print("Connection details:", wlan.ifconfig())

async def task_flash_led():
    BLINK_DELAY_MS_FAST = const(200)
    BLINK_DELAY_MS_SLOW = const(500)
    while True:
        led.toggle()
        if wlan.isconnected():
            await asyncio.sleep_ms(BLINK_DELAY_MS_SLOW)
        else:
            await asyncio.sleep_ms(BLINK_DELAY_MS_FAST)

async def main():
    """ Create all the tasks """
    tasks = [
        asyncio.create_task(connect_to_wifi(timeout=20)),
        asyncio.create_task(task_flash_led())
    ]

    await asyncio.gather(*tasks)

asyncio.run(main())
