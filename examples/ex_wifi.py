import network
import config
import time

print(f"Connecting to {config.ssid} with password {config.password}")

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface

# wlan.scan()             # scan for access points

if(not wlan.isconnected()): # check if the station is connected to an AP
    wlan.connect(config.ssid, config.password) # connect to an AP
    while(wlan.isconnected()):
        time.sleep(0.1)
        pass

print(f"Connected to {wlan.config('mac')}")      # get the interface's MAC address
print(wlan.ifconfig())         # get the interface's IP/netmask/gw/DNS addresses