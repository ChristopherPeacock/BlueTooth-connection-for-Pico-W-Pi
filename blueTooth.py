import bluetooth
import time
from machine import Pin
from utime import sleep

connectionFlag = False

# Create BLE object
ble = bluetooth.BLE()

# Function to create advertising payload
def create_advertising_payload(name):
    payload = bytearray()
    payload.extend(bytes([len(name) + 1, 0x09]))  # Length and type for Complete Local Name
    payload.extend(name.encode('utf-8'))
    return payload

# Function to start BLE advertising
def start_advertising(name="PicoW_Bluetooth", interval=1000):
    print("Starting advertising...")
    payload = create_advertising_payload(name)
    ble.gap_advertise(interval, payload, connectable=True)

def on_connect(event, data):
    global connectionFlag
    pin.on()
    conn_handle, addr_type, addr = data
    print(f"Connected to device: {addr}")
    connectionFlag = True
    # Stop advertising once connected
    
def on_disconnect(event, data):
    global connectionFlag
    reason = data
    print("Disconnected, reason:", reason)
    connectionFlag = False
    # Restart advertising after disconnection
    start_advertising()
    # Restart advertising after disconnection
    start_advertising()

# Initialize LED
pin = Pin(16, Pin.OUT)

# Start advertising the BLE device
ble.active(True)  # Turn on the BLE module
start_advertising()  # Start advertising

# Register the callback functions
def ble_irq(event, data):
    if event == 1:  # Central connected
        on_connect(event, data)
    elif event == 2:  # Central disconnected
        on_disconnect(event, data)

ble.irq(ble_irq)

print("Advertising started. Look for 'PicoW_Bluetooth' on your phone.")
print("LED starts flashing...")

# Keep the Pico W running and advertising with flashing LED
try:
    while connectionFlag == False:
        pin.toggle()
        sleep(1)  # sleep 1 sec
    if connectionFlag == True:
        while True:
            pin.on()
except KeyboardInterrupt:
    pin.off()
    print("Finished.")