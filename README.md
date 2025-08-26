# MicroPython Playground for Raspberry Pi Pico W

This project contains the code for a Wi-Fi enabled environmental sensor that sends data to an MQTT broker. It is designed for a Raspberry Pi Pico W with a BME688 sensor.

The repository is structured for a production deployment, but also contains a folder with examples for learning and testing purposes.

## Production Deployment

This guide explains how to deploy the main environmental sensor application to your Raspberry Pi Pico W.

### 1. Configure Your Credentials

Copy the `config_template.py` file to `config.py` and fill in your Wi-Fi and MQTT broker details.

### 2. Deploy to the Device

Copy the following files and directories to the root of your MicroPython device:

*   `main.py`
*   `src/`
*   `lib/`
*   `config.py`
*   `requirements.txt`
*   `install_deps.py`

You can use tools like Thonny or `mpremote` to copy the files. For example, with `mpremote`:
```bash
mpremote cp main.py src lib config.py requirements.txt install_deps.py /
```

### 3. Install Dependencies

Connect to the device's REPL and run the installation script:
```python
import install_deps
```

### 4. Run the Application

The application will now run automatically every time the device boots up. You can monitor the output by connecting to the REPL.

## Examples and Learning

This repository also contains a number of examples in the `examples/` directory. These are not required for the main application to run.

If you wish to run them, you will need to install their dependencies, which are listed in `examples/requirements.txt`. You can copy this file to your device and use the `install_deps.py` script to install them.