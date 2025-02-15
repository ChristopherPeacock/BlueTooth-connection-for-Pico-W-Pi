import bluetooth
import time
from machine import Pin
from micropython import const

# BLE Constants
_IRQ_CENTRAL_CONNECT = const(1)  # Event for when a central device connects
_IRQ_CENTRAL_DISCONNECT = const(2)  # Event for when a central device disconnects

_FLAG_READ = const(0x02)  # Flag to indicate that the characteristic can be read
_FLAG_WRITE = const(0x08)  # Flag to indicate that the characteristic can be written
_FLAG_NOTIFY = const(0x10)  # Flag to indicate that the characteristic can notify

# Use proper 128-bit UUIDs for BLE compatibility
SERVICE_UUID = bluetooth.UUID("0000A000-0000-1000-8000-00805F9B34FB")  # UUID for the service
CHARACTERISTIC_UUID = bluetooth.UUID("0000A001-0000-1000-8000-00805F9B34FB")  # UUID for the characteristic

class BLEDevice:
    def __init__(self, name="PicoW_Bluetooth"):
        self.name = name
        self.connected = False
        self.conn_handle = None
        self.ble = bluetooth.BLE()  # Initialize the BLE object
        self.ble.active(True)  # Activate BLE
        self.ble.irq(self.ble_irq)  # Set the IRQ handler for BLE events
        self.pin = Pin(16, Pin.OUT)  # Initialize the pin for the LED

        # Define GATT service with correct structure
        self.service = (
            SERVICE_UUID,
            [
                (CHARACTERISTIC_UUID, _FLAG_READ | _FLAG_NOTIFY | _FLAG_WRITE),
            ],
        )

        # Register the service
        ((self.characteristic_handle,),) = self.ble.gatts_register_services([self.service])
        
        self.start_advertising()
  
    def start_advertising(self, interval=100):
        """Start advertising BLE service"""
        print("Starting advertising...")
        payload = self.create_advertising_payload()
        self.ble.gap_advertise(interval, adv_data=payload)

    def create_advertising_payload(self):
        """Create a proper advertising packet"""
        payload = bytearray()
        payload.extend(bytes([len(self.name) + 1, 0x09]))  # Length and type for Complete Local Name
        payload.extend(self.name.encode('utf-8'))
        return payload

    def send_payload(self):
        """Send payload 55 to the connected device"""
        payload = bytearray('55', 'utf-8')
        print(f"Sending payload: {payload} to handle: {self.characteristic_handle}")
        try:
            if self.conn_handle is not None and self.characteristic_handle is not None:
                self.ble.gatts_write(self.characteristic_handle, payload)  # Write the payload to the characteristic
                self.ble.gatts_notify(self.conn_handle, self.characteristic_handle, payload)  # Send notification
                print("Sent Payload: 55")
            else:
                print("Connection handle or characteristic handle is None")
        except OSError as e:
            print(f"Error sending payload: {e}")

    def on_connect(self, conn_handle, addr_type, addr):
        """Handle BLE connection"""
        print(f"Connected to {addr}")
        self.conn_handle = conn_handle  # Store connection handle
        print(f"Connection handle: {self.conn_handle}")
        self.connected = True
        
        
    def on_disconnect(self, conn_handle, reason):
        """Handle BLE disconnection"""
        print(f"Disconnected. Reason: {reason} {conn_handle}")
        self.connected = False
        self.conn_handle = None  # Clear connection handle
        self.start_advertising()

    def ble_irq(self, event, data):
        """Handle BLE events"""
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, addr_type, addr = data
            self.on_connect(conn_handle, addr_type, addr)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            print("Disconnected")
            conn_handle, reason = data
            self.on_disconnect(conn_handle, reason)

    def run(self):
        print("Advertising started. Look for 'PicoW_Bluetooth' on your phone.")
        print("LED starts flashing...")
        try:
            while True:
                if self.connected:
                    self.send_payload()
                    
                if not self.connected:
                    self.pin.toggle()
                    time.sleep(1)  # sleep 1 sec
                else:
                    self.pin.on()
                    time.sleep(1)  # sleep 1 sec to avoid busy-waiting
        except KeyboardInterrupt:
            self.pin.off()
            print("Finished.")

# Create and run the BLE device
ble_device = BLEDevice()
ble_device.run()
