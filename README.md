# MicroPython Playground for Raspberry Pi Pico W

This project contains the code for a Wi-Fi enabled environmental sensor that sends data to an MQTT broker. It is designed for a Raspberry Pi Pico W with a BME688 sensor.

The repository is structured for a production deployment, but also contains a folder with examples for learning and testing purposes.

## Production Deployment

This guide explains how to deploy the main environmental sensor application to your Raspberry Pi Pico W.

### 1. Configure Your Credentials

Copy the `config_template.py` file to `config.py` and fill in your Wi-Fi and MQTT broker details.

### 2. Deploy to the Device

Copy the following files and directories to the root of your MicroPython device:

*   `src/*.py`
*   `src/requirements.txt`
*   `install_deps.py`
*   `config.py`

You can use tools like Thonny or `mpremote` to copy the files. Example (PowerShell) — copy several files in one command (replace `COM_PORT` with your port, e.g. `COM3`):

```powershell
mpremote -p COM_PORT fs cp src\main.py src\logger.py src\wifi.py :/
```

### 3. Install Dependencies

Dependencies are installed automatically on the device the first time it boots with an internet connection. The installer writes a small marker file after a successful run and will skip installation on subsequent boots.

To run the installer manually from the REPL (interactive):

```python
import dependency_manager
dependency_manager.install()
```

Notes:
- The module also exposes helper functions for programmatic use: `check_missing_packages()` and `install_packages()`.
- Example (from REPL):

```python
from dependency_manager import check_missing_packages, install_packages
missing = check_missing_packages()
if missing:
	install_packages(packages=missing)
```

To force re-run of the installer on the device, delete the `installed_once.flag` file from the device filesystem and reboot.

### 4. Run the Application

The application will now run automatically every time the device boots up. You can monitor the output by connecting to the REPL.

## Examples and Learning

This repository also contains a number of examples in the `examples/` directory. These are not required for the main application to run.

If you wish to run them, you will need to install their dependencies, which are listed in `examples/requirements.txt`. You can copy this file to your device and use the `install_deps.py` script to install them.