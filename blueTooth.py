import bluetooth
import time
import machine
from machine import Pin
from utime import sleep

# Create BLE object
ble = bluetooth.BLE()

# Function to create advertising payload
def create_advertising_payload(name):
    payload = bytearray()
    payload.extend(bytes([len(name) + 1, 0x09]))  # Length and type for Complete Local Name
    payload.extend(name.encode('utf-8'))
    return payload

# Function to start BLE advertising
def start_advertising(name="PicoW_Bluetooth", interval=100):
    print("Starting advertising...")
    payload = create_advertising_payload(name)
    ble.gap_advertise(interval, payload)

# Initialize LED
pin = Pin(16, Pin.OUT)

# Start advertising the BLE device
ble.active(True)  # Turn on the BLE module
start_advertising()  # Start advertising

print("Advertising started. Look for 'PicoW_Bluetooth' on your phone.")
print("LED starts flashing...")

# Keep the Pico W running and advertising with flashing LED
try:
    while True:
        pin.toggle()
        sleep(1)  # sleep 1 sec
        start_advertising()  # Start advertising
except KeyboardInterrupt:
    pin.off()
    print("Finished.")