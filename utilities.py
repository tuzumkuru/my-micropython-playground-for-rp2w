import network
import time
from logger import log

def connect_wifi(ssid, password):
    log(f"Connecting to {ssid}")
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
    wlan.scan()
    if not wlan.isconnected(): # check if the station is connected to an AP
        wlan.connect(ssid, password) # connect to an AP
        while not wlan.isconnected():
            log(f"Waiting for connection to {ssid}")
            time.sleep(1)
    log(f"Wi-Fi connected: {wlan.ifconfig()}")
    return wlan


class DerivativeAndJerkCalculator:
    def __init__(self):
        self.previous_data = None

    async def calculate_derivative_and_jerk(self, current_data):
        if self.previous_data is None:
            # If it's the first iteration, just store the current data for future calculations
            self.previous_data = {'data': current_data, 'derivative': None}
            return None, None

        # Calculate the derivative
        derivative = {key: current_data[key] - self.previous_data['data'].get(key, 0) for key in current_data}

        if self.previous_data.get('derivative') is not None:
            # Calculate the jerk
            jerk = {key: derivative[key] - self.previous_data['derivative'].get(key, 0) for key in derivative}
        else:
            jerk = None

        # Update previous data with the current data and derivatives
        self.previous_data = {'data': current_data, 'derivative': derivative}

        return derivative, jerk
    
def sync_time():
    import ntptime
    if network.WLAN(network.STA_IF).isconnected():
        try:
            ntptime.settime()
            return True
        except Exception as e:
            log(f"Error in sync_time: {e}")
            return False
    return False
