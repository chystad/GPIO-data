# This script will serve as a way to test if the start and stop bits are configured correctly 
# using a repeating signal and oscilloscope probing

# Fra Todo:
#   Skriv kode som gjentakende sender '11110000'. Da kan vi bruke oscilloskop
#   for å sjekke om det virkelig sendes en start-bit skaper en negativ flanke
#   på starten av datarammen, og en sluttbit som skaper en positiv flanke på slutten
#   av transmissjonen. Hvis dette er tilfellet -> slett 'format_cmd_and_send'

import serial
from libdef_uart import UART_COMM_OPT

serial_port = UART_COMM_OPT[0]
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

        hex_representations = [
            ('00000000', '0'),
            ('11110000', 'F0'),
            ('11111111', 'FF')
        ]
        hex_str = 'F0'
        bin_sequence = bytes.fromhex(hex_str)

        while True:
            ser.write(bin_sequence)

        


except serial.SerialException as e:
    print(f"Error opening serial port {serial_port}: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
except KeyboardInterrupt:
    print('Exiting...')
    





