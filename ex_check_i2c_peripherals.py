from machine import Pin, I2C

# Define the pins for SDA and SCL
i2c = I2C(0, sda=Pin(4), scl=Pin(5))

# Scan for connected devices
devices = i2c.scan()

# Print out the addresses of connected devices
print("Connected devices on the I2C bus:")
for device in devices:
    print(hex(device))
