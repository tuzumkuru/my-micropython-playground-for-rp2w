import ntptime
from utilities import connect_wifi
import config
import time

connect_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)

time.sleep(1)

print("Local time before synchronization：%s" %str(time.localtime()))
ntptime.settime()
print("Local time after synchronization：%s" %str(time.localtime()))