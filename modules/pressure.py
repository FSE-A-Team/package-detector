import smbus
import time

def getValue():
    address = 0x48
    A0 = 0x40
    bus = smbus.SMBus(1)
    bus.write_byte(address,A0)
    value = bus.read_byte(address)
    #print(value)
    return value

if __name__=="__main__":
    while True:
        getValue()