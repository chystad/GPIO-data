"""
@Breief: 
    All custom functions needed to operate the GPIO-pins manually on a low level. 
    The functions in this library will make working with the gpio pins much easier, as it will handle all of the exporting/unexporting, and all bash commands. 
"""


import os
from time import sleep

# Array_container_format: [
#   Port_name, GPIO_pin_number, output/input, Physical_pin_number
# ]
JETSON_NX_SPI1_PIN_DEFS = [
   ('SPI1_MOSI', 482, 'out', 8),
   ('SPI1_MISO', 481, 'in', 9),
   ('SPI1_SCK', 480, 'out', 10),
   ('SPI1_CS0', 483, 'out', 11),
]

JETSON_NX_SPI0_PIN_DEFS = [
   ('SPI1_MOSI', 493, 'out', 2),
   ('SPI1_MISO', 492, 'in', 3),
   ('SPI1_SCK', 491, 'out', 4),
   ('SPI1_CS0', 494, 'out', 5),
]

# Brief: Exports a specified gpio pin and configure it to be an input/output pin
def export_and_set_mode(pin, mode):
   try:
       #os.system(f'echo {str(pin)} > /sys/class/gpio/export')
       sleep(0.05)
       #os.system(f'echo {mode} > /sys/class/gpio/gpio{str(pin)}/direction')
       print(f'Exported gpio pin {str(pin)} with direction {mode}')
   except:
       print(f'Something went wrong while exporting pin {str(pin)} or setting pin direction to {mode}')

# Brief: Sets the gpio pin to its default configuration before unexporting
def reset_and_unexport(pin):
   try:
       #os.system(f'echo in > /sys/class/gpio/gpio{str(pin)}/direction')
       sleep(0.05)
       #os.system(f'echo {str(pin)} > /sys/class/gpio/unexport')
       print(f'gpio pin {str(pin)} unexported')
   except:
       print(f'Something went wrong while unexporting pin {str(pin)}')

# Brief: Reads the logical value on a given gpio pin
def read(pin):
   if pin == 482: # 481
       os.system(f'cat /sys/class/gpio/gpio{str(pin)}/value')
       return 0
   else:
       print('Specified gpio pin is not an input-pin')
       return -1

# Brief: Writes a logical HIGH/LOW to given gpio pin
def write(pin, state):
    if state == 'HIGH' or state == 'High' or state == 'high' or state == 1:
        write_state = 1
    elif state == 'LOW' or state == 'Low' or state == 'low' or state == 0:
        write_state = 0
    else:
        print('Invalid write state. Cannot write logical value to pin.')
        return -1
    try:
        os.system(f'echo {str(write_state)} > /sys/class/gpio/gpio{str(pin)}/value')
    except:
        print('Failed to write ')

