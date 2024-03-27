#Start by importing all necessary libraries and packages 
import RPi.GPIO as GPIO
import time
import smbus

address = 0x48
A0 = 0x40

bus = smbus.SMBus(1)

#Set the GPIO to BCM Mode
# GPIO.setmode(GPIO.BCM)

#Set Pin 4 to be our Sniffer Pin, We want this to be an Input so we set it as such
# GPIO.setup(4,GPIO.IN)

#This variable will be used to determine if pressure is being applied or not
prev_input = 0

#Create a Loop that goes on as long as the script is running
while True:

    bus.write_byte(address, A0)

    current_value = bus.read_byte(address)

    # calibrate potentiometer to 49
    original_value = 49
    package_count = 0

    while (current_value > original_value):
        if current_value > original_value:
            package_count += 1
            original_value = current_value

    

    print(f"Current Value: {current_value}")
    print(f"Package Count: {package_count}")

    #Have a slight pause here, also to avoid spamming the shell with data
    time.sleep(0.10)