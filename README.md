# MicroPython Playground for Raspberry Pi Pico W

This project is a collection of MicroPython examples and applications for the Raspberry Pi Pico W. It includes code for various sensors and communication protocols, with a focus on IoT and environmental sensing.

## Features

*   **Environmental Sensing:** Reads data from a BME688 sensor (temperature, humidity, pressure, gas).
*   **Motion Sensing:** Interfaces with an MPU6050 inertial measurement unit (IMU).
*   **Air Quality Sensing:** Reads data from an SGP40 VOC sensor.
*   **MQTT Communication:** Sends sensor data to an MQTT broker. Includes examples for both `umqtt.simple` and `mqtt_as`.
*   **BLE Peripheral:** An example of how to use the Raspberry Pi Pico W as a BLE peripheral.
*   **Over-the-Air (OTA) Updates:** An example of how to perform OTA updates using MQTT.
*   **Dependency Management:** Includes a `requirements.txt` file and a script to install the required packages using `mip`.

## Hardware

*   Raspberry Pi Pico W
*   BME688 Breakout Board
*   MPU6050 Breakout Board
*   SGP40 Breakout Board

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```

2.  **Configure your credentials:**
    Copy the `config_template.py` file to `config.py` and fill in your Wi-Fi and MQTT broker details.
    ```bash
    cp config_template.py config.py
    ```

3.  **Install dependencies:**
    Upload `requirements.txt` and `install_deps.py` to your MicroPython device. Then, connect to the device's REPL and run:
    ```python
    import install_deps
    ```
    This will install all the necessary libraries.

## Usage

The main application is `main.py`, which runs the environmental sensor and sends the data to an MQTT broker. You can run it from the REPL:

```python
import main
```

## Examples

The project includes several example files with the `ex_` prefix. These demonstrate how to use the different sensors and features individually. You can run them from the REPL to test your hardware and connections.
