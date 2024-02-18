# Import necessary libraries
from collections import deque
import numpy as np

# Set the window size
window_size = 50

# Initialize your data windows
temperature_data = deque(maxlen=window_size)
pressure_data = deque(maxlen=window_size)
humidity_data = deque(maxlen=window_size)
gas_data = deque(maxlen=window_size)

while True:
    current_time = time.time()

    bme_data = await get_sensor_data(bme)

    # Store your data
    temperature_data.append(bme_data['temperature'])
    pressure_data.append(bme_data['pressure'])
    humidity_data.append(bme_data['humidity'])
    gas_data.append(bme_data['gas'])

    derivative, jerk = await calculator.calculate_derivative_and_jerk(bme_data)

    if len(temperature_data) == window_size:  # Check if window is filled
        # Calculate statistics
        temp_std = np.std(temperature_data)
        pressure_std = np.std(pressure_data)
        humidity_std = np.std(humidity_data)
        gas_std = np.std(gas_data)

        # Print or use them in your logic
        print('Temperature Standard Deviation:', temp_std)
        print('Pressure Standard Deviation:', pressure_std)
        print('Humidity Standard Deviation:', humidity_std)
        print('Gas Standard Deviation:', gas_std)

        # Set your thresholds based on these statistics and use them in your logic.