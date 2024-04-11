import os
import serial
from time import sleep


# Todo:
#   Sjekk at følgende parametre er konfigurert som ønsket på pico-en:
#   baudrate: man kan ikke se den i "I", men settes til 9600 med 'SB9600'
#   Stop-bits og parity: Sjekk status med å sende 'S97ux<CR><SOH>. I strengen som
#   returneres er det byte 30 og 31 som er av relevans. Disse kan kun endres ved å
#   oppgi et passord, så jeg antar foreløpig at picoen er konfigurert med de anbefalte
#   valgene for UART (parity: none, stop bits: 1)
#
#   ------------------GJORT!------------------
#   Skriv kode som gjentakende sender '11110000'. Da kan vi bruke oscilloskop
#   for å sjekke om det virkelig sendes en start-bit skaper en negativ flanke
#   på starten av datarammen, og en sluttbit som skaper en positiv flanke på slutten
#   av transmissjonen. Hvis dette er tilfellet -> slett 'format_cmd_and_send'
#   -------------------------------------------
#
#   Endre funksjonen uart_wakeup_cmd() til å sende signal fra RX-pinnen 
#   (Dette må endres for å sende korrekt wakeup signal til magnetometeret)
#
#   Endre uart.py til å inkludere threading slik at scriptet kan høre etter data inputs 
#   mens den venter på den neste kommandoen fra brukeren.




# ARRAY_FORMAT: [
#   serial_port,
#   baud_rate,
#   stop_bits,      Sjekk hva som er definert i pico-en
#   parity,         Sjekk hva som er definert i pico-en
#   timeout,
#   wakeup_time
# ]
UART_COMM_OPT = ['TCU0', 9600, 1, 'none', 1, 0.1]


# Brief: No argument: Lists all available ports. Argument: Check if specified port is available
def check_available_ports(*port):
    if not port:
        print('No specific port specified, listing all available ports...')
        try:
            os.system('python3 -m serial.tools.list_ports')
        except:
            print('Error while listing available serial ports')
    else:
        print(f'Checking individual ports is not yet implemented')
        print('Try calling the function without any argument to fetch a complete list over all available ports')
        # Todo...

# Brief: Send a rising edge signal from TX pin which triggers a wakeup sequence in the magnetometer
def uart_wakeup_cmd(serial, wakeup_time):
    # Assuming that the serial connection has already been established

    # The bit representation of '@' is 01000000, which is interpreted as a wakeup signal for the magnetometer
    # A signal like 00001000 would also be interpretes as a wakeup signal for the magnetometer, but '@' is the 
    # first readable ASCII character with a single 1 in its 8-bit representation
    
    #cmd_hex_str = '6162' #'ab'
    #binary_sequence = bytes.fromhex(cmd_hex_str)
    #print(binary_sequence)
    try:
        serial.write(b'@')
        print('Wakeup signal sent. Waiting for the magnetometer to wake up...')
    except:
        print('Failed to send wakeup signal to the magnetometer ')
        return -1
    sleep(wakeup_time)
    print('The magnetometer has woken up')

def cmd_str_to_sendable_bin_sequence(cmd_string):
    # cmd_hex_arr is only for debugging purposes
    #cmd_hex_arr = []
    hex_str= ''.join(format(ord(c), '02x') for c in cmd_string)
    #cmd_hex_arr.append(hex_string)
    #print(cmd_hex_arr)
    bin_sequence = bytes.fromhex(hex_str)
    return bin_sequence

# Brief: Converts an input character string into the corresponsing 8-bit ASCII representation, and returns a 
# 10-bit value with the correct start and stop bit to enable communication with the magnetometer
def format_character_to_send(character_string):
    bin_representation = format(ord(character_string), '08b')
    # Add a 0 at the beginning and a 1 at the end (start and stop bit)
    custom_bin = '0' + bin_representation + '1'
    return custom_bin

# Brief: Sends a command string in 10-bit packets over serial. 
def send_cmd(serial, cmd_string):
    cmd_string_arr = list(cmd_string)
    for i in range(0, len(cmd_string_arr)):
        bit_string_to_send = format_character_to_send(cmd_string_arr[i])
        print(bit_string_to_send)
        try:
            serial.write(bit_string_to_send)
        except:
            print(f'Failed to send bit string {bit_string_to_send}')
            print('INFO: Aborting command transmission')
            break
    print(f'Command {cmd_string} successfully transmitted')
    return 0

# Brief: Converts a cmd string into a hexadecimal string that accounts for
# the neccessary start and stop bit. Then the command is sent to the magnetometer
def format_cmd_and_send(serial, cmd_string):
    cmd_bit_arr = []
    
    # Converts each character into its 8-bit ascii value, and adds the appropriate 
    # start and stop bit to enable communication with the magnetometer
    for char in cmd_string:
        binary_string = format(ord(char), '08b')
        modified_bits = [0] + [int(bit) for bit in binary_string] + [1]
        # Append modified bits to the bit array
        cmd_bit_arr.extend(modified_bits)

    # Extend the bit array with 1's if its length is not divisible by 8
    while len(cmd_bit_arr) % 8 != 0:
        cmd_bit_arr.append(1)
    
    # Convert each group of 8 bits to a hexadecimal character
    cmd_hex_arr = []
    for i in range(0, len(cmd_bit_arr), 8):
        # Join 8 bits to form a binary string, then convert to an integer, and finally to a hexadecimal string
        hex_char = format(int(''.join(str(bit) for bit in cmd_bit_arr[i:i+8]), 2), '02x')
        cmd_hex_arr.append(hex_char)
    print(cmd_hex_arr)

    # NB! TRENGER BARE EN AV DE TO METODENE UNDER. BESTEM ÈN
    """
    cmd_byte_sequence = ''.join(['\\x' + hex_byte for hex_byte in cmd_hex_arr])
    print(cmd_byte_sequence)
    """
    cmd_hex_str = ''.join(cmd_hex_arr)
    print(cmd_hex_str)
    binary_sequence = bytes.fromhex(cmd_hex_str)
    print(binary_sequence)


    try:
        # Will give an error if the binary sequence contains a hex number > 7F
        serial.write(binary_sequence)
    except:
        print(f'Failed to send bit string {binary_sequence}')
        print('INFO: Aborting command transmission')
    print(f'Command {cmd_string} successfully transmitted')

