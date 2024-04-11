import serial
import time

# The serial port name will depend on your operating system and how the device is connected.
# On Windows, it might be 'COM#' (e.g., 'COM3').
# On Linux or macOS, it will be something like '/dev/ttyUSB0' or '/dev/ttyACM0'.
serial_port = '/dev/ttyUSB0'
baud_rate = 9600  # Set this to match the baud rate used by your device.

try:
    # Attempt to open the serial port
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
        print(f"Opened serial port {serial_port}")

        # Write the character 'I' to the device
        ser.write(b'I')  # b'I' is the byte literal for "I"
        print("Wrote 'I' to the device")

        # Optionally, read response from the device
        response = ser.readline()
        print(f"Received response: {response}")

        # Wait a bit for the data to be sent and received
        time.sleep(1)

except serial.SerialException as e:
    print(f"Error opening serial port {serial_port}: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")