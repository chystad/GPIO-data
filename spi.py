# Krav for å få SPI til å fungere
#   (OPPFYLT) Power up: "If a high logic level is detected on the UART-RX pin (MOSI), the UART will be activated. Otherwise, the SPI port will be the active serial interface"
#
#   (OPPFYLT) Wake up cmd: "Falling edge signal on the SPI-CS pin" + info: "A single "wake up" character will be discarded by the microprocessor"
#   Denne vil bli oppfylt bare av å sende et hvilket som helst signal ettersom CS går fra høy til lav under en transmisjon. 
#
#   (OPPFYLT) MSB overføres først (Sjekket med signalet '10000011' og det stemmer)
#
#   (OPPFYLT) Anbefalte innstillinger: 200kHz bus, minst 200 mikro sek mellom rammene 
#
#   (OPPFYLT) "The CS has to be set and released for every 16-bit frame"

# Idle pin levels:
#   MOSI: LOW
#   MISO: LOW (ser litt ustabil ut? flyt?)
#   SCK:  LOW
#   CS:   HIGH


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

   # mosi_low(mosi_pin, mosi_mode)

   # Configure spi communication 
   spi = spidev.SpiDev()
   spi.open(spidev_bus, spidev_dev) 

   spi.max_speed_hz = max_speed_hz
   spi.mode = mode

   sleep(1)

   try:
       spi_wakeup(spi, mag_wakeup_time)
       sleep(1)

       n = 0
       while True:
           if n == 0:
               frame_to_send = [0x49, 0xA5]
           if n == 1:
               frame_to_send = [0x0D, 0xFF]
           else:
               frame_to_send = [0xFF, 0xFF]

           response = spi.xfer2(frame_to_send)

           data_byte, control_byte = response
           
           if True:
               print(f'Received data byte: {data_byte}, Control byte: {control_byte}')

           sleep(0.00001)
           n = n + 1

           """
           if (n % 2) == 0:
               frame_to_send = [0x83, 0xA5]
           else:
               frame_to_send = [0x83, 0xA5]

           response = spi.xfer2(frame_to_send)
           
           # With this delay, the time in between each frame is measured to be around 250us (over 200us is recommended)
           sleep(0.00001)
           """
           """
           # Construct a frame to send consisting of a data byte and control byte respectivly
           # I = 0x49
           if (n+1) % 30000 == 0:
               msg = "I".encode()
               print(msg)
               frame_to_send = [0X49, 0xA5]
           elif False:
               frame_to_send = [0x0D, 0xA5]
           else:
               frame_to_send = [0xFF, 0xFF]
           
           # print(f'sending: {frame_to_send}')

           # Send frame and read response
           response = spi.xfer2(frame_to_send)
           

           if len(response) == frame_length:
               data_byte, control_byte = response
               if control_byte != 255:
                   print(f'Received data byte: {data_byte}, Control byte: {control_byte}')
           else:
               print('Unexpected response length')

           if (n > (10 * max_speed_hz)):
               break
               #and (control_byte == 0xFF)
           """
           
           sleep(0.00001)
           n = n + 1
       
       print(f'Exit condition met. Closing spi communication...')
       #print(f'Control_byte in response indicate end of transmission. Closing spi communication...')
       spi.close()



   except KeyboardInterrupt:
       print('Closing spi communication...')
       spi.close()


main()