import os
from time import sleep
from libdef_gpio import export_and_set_mode
from libdef_gpio import reset_and_unexport

# ARRAY_FORMAT: [
#   spidev_bus, 
#   spidev_device,
#   frame_length, 
#   max_speed_hz, 
#   spi_mode, 
#   wakeup_time
# ]
SPI_COMM_SPECS = [0, 0, 2, 200000, 0, 0.1]


# Brief: Loads all spidev modules if it hasn't been loaded yet
def initialize_spidev_modules():
   if not os.path.exists(f'/dev/spidev0.0'):
       print('importing spi modules...')
       try:
           os.system('sudo modprobe spidev')
           print('Loading spidev modules...')
           sleep(5)
       except:
           print('failed to import spi modules')
   else:
       print('spi modules already imported')


# Brief: Holds mosi LOW until the magnetometer has booted. Necessary for ensuring that 
# the chipset on the connector-stip selects SPI communication protocol
def mosi_low(mosi_pin, mosi_mode):
   print('Exporting MOSI pin...')
  
   if not os.path.exists(f'/sys/class/gpio/gpio{str(mosi_pin)}'):
       export_and_set_mode(mosi_pin, mosi_mode)

   sleep(0.05)
   print('Setting MOSI to LOW. You can now connect the magnetometer')
   os.system(f'echo 0 > /sys/class/gpio/gpio{str(mosi_pin)}/value')

   while True:
       try:
           txt_in = input('Do you wish to proceed to SPI communication? (y/n)')
           if txt_in == 'y':
               break
       except KeyboardInterrupt:
           break
      
   print('Program exited, unexporting MOSI pin...')
   reset_and_unexport(mosi_pin)
   sleep(0.05)

# Brief: Creates a falling edge on the CS-pin. This is used as a wakeup-signal to the magnetometer 
# which will make it enter its "operational mode"
def spi_wakeup(spi, spi_init_time):
   frame_to_send = [0x0D, 0xA5] # It does not matter what signal is sent beacuse CS will go HIGH->Low during a transmission anyway
   response = spi.xfer2(frame_to_send)
   print(response)
   print('spi awakened (Hopefully)')
   sleep(spi_init_time)