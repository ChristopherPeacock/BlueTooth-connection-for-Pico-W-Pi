import bluetooth
import time
from machine import Pin
from utime import sleep

class BLEDevice:
    def __init__(self, name="PicoW_Bluetooth"):
        self.name = name
        self.connectionFlag = False
        self.ble = bluetooth.BLE()
        self.pin = Pin(16, Pin.OUT)
        self.ble.active(True)
        self.ble.irq(self.ble_irq)
        self.start_advertising()

    def create_advertising_payload(self):
        payload = bytearray()
        payload.extend(bytes([len(self.name) + 1, 0x09]))  # Length and type for Complete Local Name
        payload.extend(self.name.encode('utf-8'))
        return payload

    def start_advertising(self, interval=1000):
        print("Starting advertising...")
        payload = self.create_advertising_payload()
        self.ble.gap_advertise(interval, payload, connectable=True)

    def on_connect(self, event, data):
        self.pin.on()
        conn_handle, addr_type, addr = data
        print(f"Connected to device: {addr}")
        self.connectionFlag = True
        # Stop advertising once connected
        self.ble.gap_advertise(None)

    def on_disconnect(self, event, data):
        reason = data
        print("Disconnected, reason:", reason)
        self.connectionFlag = False
        # Restart advertising after disconnection
        self.start_advertising()

    def ble_irq(self, event, data):
        if event == 1:  # Central connected
            self.on_connect(event, data)
        elif event == 2:  # Central disconnected
            self.on_disconnect(event, data)

    def run(self):
        print("Advertising started. Look for 'PicoW_Bluetooth' on your phone.")
        print("LED starts flashing...")
        try:
            while True:
                if not self.connectionFlag:
                    self.pin.toggle()
                    sleep(1)  # sleep 1 sec
                else:
                    self.pin.on()
                    sleep(1)  # sleep 1 sec to avoid busy-waiting
        except KeyboardInterrupt:
            self.pin.off()
            print("Finished.")

# Create and run the BLE device
ble_device = BLEDevice()
ble_device.run()