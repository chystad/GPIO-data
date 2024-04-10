import spidev
from time import sleep
from libdef_spi import initialize_spidev_modules
from libdef_spi import mosi_low
from libdef_spi import spi_wakeup
from libdef_spi import SPI_COMM_SPECS
from libdef_gpio import JETSON_NX_SPI0_PIN_DEFS

# Note to self:
# Hvis magnetometeret merker HØY på RX/MOSI pinnen ved boot velger den UART kommunikasjon!
# Derfor er det fiktig at MOSI er lav mens magnetometeret booter

spidev_bus = SPI_COMM_SPECS[0]
spidev_dev = SPI_COMM_SPECS[1]
frame_length = SPI_COMM_SPECS[2]
max_speed_hz = SPI_COMM_SPECS[3]           
mode = SPI_COMM_SPECS[4]
mag_wakeup_time = SPI_COMM_SPECS[5]         

mosi_pin = JETSON_NX_SPI0_PIN_DEFS[0][1]
mosi_mode = JETSON_NX_SPI0_PIN_DEFS[0][2]
cs_pin = JETSON_NX_SPI0_PIN_DEFS[3][1]
cs_mode = JETSON_NX_SPI0_PIN_DEFS[3][2]


def main():
   initialize_spidev_modules()

   mosi_low(mosi_pin, mosi_mode)

   spi_wakeup(cs_pin, cs_mode, mag_wakeup_time)

   # Configure spi communication 
   spi = spidev.SpiDev()
   spi.open(spidev_bus, spidev_dev) 

   spi.max_speed_hz = max_speed_hz
   spi.mode = mode

   sleep(1)

   try:
       n = 0
       while True:
           # Construct a frame to send consisting of a data byte and control byte respectivly
           # I = 0x49
           if n % 30000 == 0:
               msg = "I".encode()
               print(msg)
               frame_to_send = [0X49, 0xA5]
           else:
               frame_to_send = [0xFF, 0xFF]
           
           # print(f'sending: {frame_to_send}')

           # Send frame and read response
           response = spi.xfer3(frame_to_send)
         

           if len(response) == frame_length:
               data_byte, control_byte = response
               if control_byte != 255:
                   print(f'Received data byte: {data_byte}, Control byte: {control_byte}')
           else:
               print('Unexpected response length')

           if (n > (10 * max_speed_hz)):
               break
               #and (control_byte == 0xFF)
           n = n + 1
       
       print(f'Exit condition met. Closing spi communication...')
       #print(f'Control_byte in response indicate end of transmission. Closing spi communication...')
       spi.close()



   except KeyboardInterrupt:
       print('Closing spi communication...')
       spi.close()


main()