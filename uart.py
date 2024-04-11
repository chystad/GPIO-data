import serial
import threading
from time import sleep
from libdef_uart import uart_wakeup_cmd 
from libdef_uart import cmd_str_to_sendable_bin_sequence
from libdef_uart import UART_COMM_OPT

serial_port = '/dev/ttyUSB0'
baud_rate = UART_COMM_OPT[1]
wakeup_time = UART_COMM_OPT[5]
timeout = UART_COMM_OPT[4]

# Function to continuously listen for incoming data on the serial port
def listen_for_incoming_data(serial):
    while not exit_flag.is_set():  # Continue until told to stop
        if serial.in_waiting > 0:
            line = serial.readline(ser.in_waiting).decode('UTF-8').rstrip()
            print()
            print(line)

try:
    with serial.Serial(
        port=serial_port,
        baudrate=baud_rate,
        bytesize=serial.EIGHTBITS,  # Number of data bits (default is EIGHTBITS)
        parity=serial.PARITY_NONE,  # Set parity (default is PARITY_NONE)
        stopbits=serial.STOPBITS_ONE,  # Set the number of stop bits
        timeout=1
    ) as ser:
        
        print(f'Opened serial port {serial_port} with baud rate {str(baud_rate)}')

        # Create a thread-safe flag to signal when the program should exit
        exit_flag = threading.Event()

        # Start the listening thread
        listen_thread = threading.Thread(target=listen_for_incoming_data, args=(ser,))
        listen_thread.start()

        while True:
            print()
            cmd_to_send = input('Command to send to the magnetometer: ')
            if cmd_to_send.lower() == 'exit':
                exit_flag.set()  # Tell the listening thread to stop
                listen_thread.join()  # Wait for the listening thread to finish
                break
            ser.write(cmd_str_to_sendable_bin_sequence(cmd_to_send))


except serial.SerialException as e:
    print(f"Error opening serial port {serial_port}: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
except KeyboardInterrupt:
    exit_flag.set()  # Ensure the listening thread stops if CTRL+C is pressed
    listen_thread.join()  # Wait for the listening thread to finish
    print('Exiting...')





"""
This script works perfectly fine for sending commands, but fails to listen to data
while it waits for the user to provide a command input 

import serial
from time import sleep 
from libdef_uart import uart_wakeup_cmd
from libdef_uart import cmd_str_to_sendable_bin_sequence
from libdef_uart import format_character_to_send
from libdef_uart import send_cmd
from libdef_uart import format_cmd_and_send
from libdef_uart import UART_COMM_OPT

serial_port = '/dev/ttyUSB0'
baud_rate = UART_COMM_OPT[1]
wakeup_time = UART_COMM_OPT[5]
timeout = UART_COMM_OPT[4]

try:
    with serial.Serial(
        port=serial_port,
        baudrate=baud_rate, 
        bytesize=serial.EIGHTBITS,  # Number of data bits (default is EIGHTBITS)
        parity=serial.PARITY_NONE,  # Set parity (default is PARITY_NONE)
        stopbits=serial.STOPBITS_ONE,  # Set the number of stop bits
        timeout=1
    ) as ser:
        
        print(f'Opened serial port {serial_port} with baud rate {str(baud_rate)}')

        #uart_wakeup_cmd(ser, wakeup_time)

        while True:
            if ser.in_waiting > 0:
                #line = ser.readline().decode('utf-8').rstrip()
                line = ser.readline(ser.in_waiting).decode('UTF-8').rstrip()
                print(line)
            
            cmd_to_send = input('Command to send to the magnetometer: ')
            ser.write(cmd_str_to_sendable_bin_sequence(cmd_to_send))

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

