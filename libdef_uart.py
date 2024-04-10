import os
import serial

# Brief: No argument: Lists all available ports. Argument: Check if specified port is available
def check_available_ports(*port):
    if not port:
        print('No specific port specified, listing all available ports...')
        try:
            os.system('python3 -m serial.tools.list_ports')
        except:
            print('Error while listing available serial ports')
    else:
        print(f'Checking if port {port} is available')
        # Todo...


check_available_ports()