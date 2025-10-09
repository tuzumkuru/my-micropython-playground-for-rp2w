import network
import uasyncio as asyncio
import time
from logger import log

class WiFi:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self, ssid, password, timeout=20, retries=3, backoff_factor=2):
        """Connect synchronously with timeout and retries.

        Args:
            ssid (str): network SSID
            password (str): network password
            timeout (int): seconds to wait for each attempt
            retries (int): number of attempts (including first)
            backoff_factor (float): multiplier for sleep between retries
        Returns:
            bool: True if connected, False otherwise
        """
        log(f"Connecting to {ssid}")
        self.wlan.active(True)  # Activate the interface

        attempt = 0
        wait = 1
        while attempt < retries:
            attempt += 1
            try:
                if self.is_connected():
                    log("Already connected")
                    return True

                log(f"Attempt {attempt}/{retries}: connecting to {ssid}")
                # start connect
                try:
                    self.wlan.connect(ssid, password)
                except Exception as e:
                    # Some ports raise if already connecting; ignore and proceed to wait
                    log(f"connect() raised: {e}")

                start = time.time()
                while time.time() - start < timeout:
                    if self.wlan.isconnected():
                        log(f"Wi-Fi connected: {self.wlan.ifconfig()}")
                        return True
                    # log occasional status
                    log(f"Waiting for connection... status={self.wlan.status()}")
                    time.sleep(1)

                log(f"Attempt {attempt} timed out after {timeout}s")
            except Exception as e:
                log(f"Error occurred while connecting: {e}")

            # failed this attempt; disconnect and backoff before retrying
            try:
                self.wlan.disconnect()
            except Exception:
                pass

            if attempt < retries:
                sleep_for = wait
                log(f"Retrying in {sleep_for}s...")
                time.sleep(sleep_for)
                wait = min(wait * backoff_factor, 60)

        log("Failed to connect after retries")
        return False

    async def connect_async(self, ssid, password):
        """Async connect with timeout, retries and optional backoff.

        This function is non-blocking and returns True on success, False on failure.
        """
        return await self.connect_async_with_options(ssid, password)

    async def connect_async_with_options(self, ssid, password, timeout=20, retries=3, backoff_factor=2):
        log(f"Connecting to {ssid} (async)")
        self.wlan.active(True)
        await asyncio.sleep(0)  # allow event loop to run

        attempt = 0
        wait = 1
        while attempt < retries:
            attempt += 1
            try:
                if self.is_connected():
                    log("Already connected")
                    return True

                log(f"Async attempt {attempt}/{retries}: connecting to {ssid}")
                try:
                    self.wlan.connect(ssid, password)
                except Exception as e:
                    log(f"connect() raised: {e}")

                start = time.time()
                while time.time() - start < timeout:
                    if self.wlan.isconnected():
                        log(f"Wi-Fi connected: {self.wlan.ifconfig()}")
                        return True
                    log(f"Waiting for connection... status={self.wlan.status()}")
                    await asyncio.sleep(1)

                log(f"Async attempt {attempt} timed out after {timeout}s")
            except Exception as e:
                log(f"Error occurred while connecting asynchronously: {e}")

            try:
                self.wlan.disconnect()
            except Exception:
                pass

            if attempt < retries:
                sleep_for = wait
                log(f"Async retrying in {sleep_for}s...")
                await asyncio.sleep(sleep_for)
                wait = min(wait * backoff_factor, 60)

        log("Failed to connect after async retries")
        return False

    def is_connected(self):
        return self.wlan.isconnected()

    def disconnect(self):
        try:
            self.wlan.disconnect()
        except Exception as e:
            log(f"Error occurred while disconnecting: {e}")

    def scan(self):
        try:
            return self.wlan.scan()
        except Exception as e:
            log(f"Error occurred while scanning: {e}")
            return []

    def get_ip(self):
        try:
            return self.wlan.ifconfig()[0]
        except Exception as e:
            log(f"Error occurred while getting IP address: {e}")
            return None
