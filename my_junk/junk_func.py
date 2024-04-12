def cmd_str_to_sendable_bin_sequence(cmd_string):
    # cmd_hex_arr is only for debugging purposes
    #cmd_hex_arr = []
    hex_str= ''.join(format(ord(c), '02x') for c in cmd_string)
    #cmd_hex_arr.append(hex_string)
    #print(cmd_hex_arr)
    bin_sequence = bytes.fromhex(hex_str)
    return bin_sequence

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

