import can
from can.bus import BusABC
#can.rc['interface'] = 'socketcan'
#can.rc['channel'] = 'can0'
#can.rc['bitrate'] = 500000
#from can.interface import Bus

#bus = Bus()

#with can.Bus() as bus:
#    for msg in bus:
#        print(msg.data)

msg = can.interface.Bus(channel="", bustype='socketcan').recv(timeout=20)
print(msg)