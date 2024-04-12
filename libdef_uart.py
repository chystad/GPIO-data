import os
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
#   ------------------GJORT!------------------
#   Endre uart.py til å inkludere threading slik at scriptet kan høre etter data inputs 
#   mens den venter på den neste kommandoen fra brukeren.
#   ------------------------------------------




# ARRAY_FORMAT: [
#   serial_port,
#   baud_rate,
#   stop_bits,      Sjekk hva som er definert i pico-en
#   parity,         Sjekk hva som er definert i pico-en
#   timeout,
#   wakeup_time
# ]
UART_COMM_OPT = ['/dev/ttyTCU0', 9600, 1, 'none', 1, 0.1]


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

# Brief: Sends the command as a binary sequence with LSB first (standard)
def cmd_bin_sequence(cmd_string):
    # cmd_hex_arr is only for debugging purposes
    #cmd_hex_arr = []
    hex_str= ''.join(format(ord(c), '02x') for c in cmd_string)
    #cmd_hex_arr.append(hex_string)
    #print(cmd_hex_arr)
    bin_sequence = bytes.fromhex(hex_str)
    return bin_sequence

# Brief: Sends the command as a binary sequence with MSH first
def mirrored_cmd_bin_sequence(cmd_string):
    result_hex = []

    for char in cmd_string:
        # Convert character to its ASCII integer
        ascii_value = ord(char)
        
        # Convert the ASCII value to an 8-bit binary string
        bin_str = '{:08b}'.format(ascii_value)
        
        # Reverse the binary string
        reversed_bin_str = bin_str[::-1]
        
        # Convert the reversed binary string back to an integer
        reversed_num = int(reversed_bin_str, 2)
        
        # Convert the integer back to hexadecimal, removing the '0x' prefix
        reversed_hex = '{:02x}'.format(reversed_num)
        
        # Append the result to the list
        result_hex.append(reversed_hex)

    # Join all hexadecimal numbers into a single string
    hex_str = ''.join(result_hex)

    bin_sequence = bytes.fromhex(hex_str)
    return bin_sequence
