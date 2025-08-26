import asyncio
from machine import I2C, Pin
from bme688 import *
import network
import config

print("Starting program.")

led = Pin('LED', Pin.OUT)
i2c = I2C(0, sda=Pin(4), scl=Pin(5))
bme = BME680_I2C(i2c)
wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface

temperature = bme.temperature
pressure = bme.pressure
humidity = bme.humidity
gas = bme.gas



async def task_peripheral():
  if(not wlan.isconnected()): # check if the station is connected to an AP
    print(f"Trying to connect.")
    wlan.connect(config.ssid, config.password) # connect to an AP

  while(wlan.isconnected()):
    print("Temperature: {:.2f} °C".format(temperature))
    print("Pressure: {:.2f} hPa".format(pressure))
    print("Humidity: {:.2f} %".format(humidity))
    print("Gas: {:.2f} kOhms".format(gas))
    await asyncio.sleep(5)

 

async def task_flash_led():
  print(f"task_flash_led")
  """ Blink the on-board LED, faster if !connected and slower if connected  """
  BLINK_DELAY_MS_FAST = const(200)
  BLINK_DELAY_MS_SLOW = const(500)
  while True:
    print(f"led.toggle(). {wlan.isconnected()}")
    led.toggle()
    if wlan.isconnected():
      await asyncio.sleep(BLINK_DELAY_MS_SLOW/1000)
    else:
      await asyncio.sleep(BLINK_DELAY_MS_FAST/1000)

async def task_sensor():
  while True:
    # Get sensor data
    temperature = bme.temperature
    pressure = bme.pressure
    humidity = bme.humidity
    gas = bme.gas
    await asyncio.sleep(1)

async def main():
  """ Create all the tasks """
  tasks = [
    asyncio.create_task(task_peripheral()),
    asyncio.create_task(task_flash_led()),
    asyncio.create_task(task_sensor()),
  ]

  await asyncio.gather(*tasks)


asyncio.run(main())
