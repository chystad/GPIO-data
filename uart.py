import serial
import threading
from time import sleep 
from libdef_uart import uart_wakeup_cmd
from libdef_uart import format_character_to_send
from libdef_uart import send_cmd
from libdef_uart import format_cmd_and_send
from libdef_uart import UART_COMM_SPECS

serial_port = '/dev/ttyUSB0'
baud_rate = UART_COMM_SPECS[1]
wakeup_time = UART_COMM_SPECS[2]

try:
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
        print(f'Opened serial port {serial_port} with baud rate {str(baud_rate)}')

        #uart_wakeup_cmd(ser, wakeup_time)
        format_cmd_and_send(ser, 'S82I@')


        while True:
            if ser.in_waiting > 0:
                #line = ser.readline().decode('utf-8').rstrip()
                line = ser.read(ser.in_waiting).decode('utf-8')
                print(line)
            
            #cmd_to_send = input('Command to send to the magnetometer: ')

            # Todo: Some cmd verification

            #send_cmd(ser, cmd_to_send)

            # if cmd_is_expecting_response:
            #     listen_for_response...

        


except serial.SerialException as e:
    print(f"Error opening serial port {serial_port}: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
except KeyboardInterrupt:
    print('Exiting...')
    






"""

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
        sleep(1)

except serial.SerialException as e:
    print(f"Error opening serial port {serial_port}: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
except KeyboardInterrupt:
    print('Exiting')
    ser.close()


"""