# BLEDevice - Bluetooth Low Energy for Pico W

## Overview
This project implements a Bluetooth Low Energy (BLE) peripheral using a Raspberry Pi Pico W. The BLE device advertises itself, allows connections from a central device (such as a smartphone), and sends a simple payload periodically when connected. It also features an LED indicator to show connection status.

## Features
- BLE peripheral using MicroPython
- Advertises itself as `PicoW_Bluetooth`
- Supports read, write, and notify operations on a BLE characteristic
- Sends a payload (`55`) when connected
- Handles BLE connection and disconnection events
- Uses an onboard LED to indicate connection status
- Processes BLE events asynchronously

## Hardware Requirements
- Raspberry Pi Pico W
- MicroPython installed on the Pico W

## Setup and Usage
1. **Flash MicroPython** onto your Pico W if not already installed.
2. **Copy the script** to your Pico W.
3. **Run the script** using a MicroPython-compatible IDE (e.g., Thonny, RShell, or mpremote).
4. Use a **BLE scanner app** on your phone to find and connect to `PicoW_Bluetooth`.
5. Upon connection, the device will start sending the payload `55`.
6. The onboard LED will indicate the connection status:
   - Flashing: Advertising mode (not connected)
   - On: Connected and sending payload
   - Off: Script stopped

## Code Breakdown
### Initialization
- The BLE device is initialized and set up with a service and characteristic.
- The LED is assigned to indicate connection status.

### Advertising
- The device starts advertising itself with the name `PicoW_Bluetooth`.

### BLE Event Handling
- On connection, it stores the connection handle and turns on the LED.
- On disconnection, it restarts advertising and resets the connection status.

### Sending Data
- When connected, the device sends a payload (`55`) via BLE notifications.

## Dependencies
- MicroPython with Bluetooth support enabled

## Notes
- Ensure your BLE scanner app supports notifications to receive the `55` payload.
- Modify `SERVICE_UUID` and `CHARACTERISTIC_UUID` if you want to customize the BLE service.

## License
This project is open-source and free to use under the MIT License.

