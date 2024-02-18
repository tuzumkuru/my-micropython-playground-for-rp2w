import asyncio
import config
from utilities import connect_wifi



async def get_sensor_data(sensor):
    return {
        "temperature": sensor.temperature,
        "pressure": sensor.pressure,
        "humidity": sensor.humidity,
        "gas": sensor.gas
    }




async def main():
    wifi = connect_wifi(ssid=config.WIFI_SSID, password=config.WIFI_PASSWORD)

    if wifi.isconnected:

    pass
    

# Run the event loop
loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()