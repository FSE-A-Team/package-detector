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

package_count = 0
original_value = 15

# Time interval to check the weight (1 second)
interval = 1
# Store the last time the package was counted
last_time_weight_changed = time.time()

# TODO - Implement buffer WHILE the weight changes
# buffer = 1

#Create a Loop that goes on as long as the script is running
while True:

    bus.write_byte(address, A0)

    current_value = bus.read_byte(address)

    # calibrate potentiometer to 12
  
    # Check if at least interval seconds have passed since last weight change
    if (time.time() - last_time_weight_changed) >= interval:
        if original_value < current_value:
            # New package added, increase count
            package_count += 1
            last_time_weight_changed = time.time()  # Reset the timer for weight change
        elif original_value > current_value and package_count > 0:
            # Package removed, decrease count
            
            package_count -= 1
            last_time_weight_changed = time.time()  # Reset the timer for weight change

        original_value = current_value  # Update the original value to the new value

        print(f"Current Value: {current_value}")
        print(f"Package Count: {package_count}")

   
    #Have a slight pause here, and avoid spamming the shell with data
    time.sleep(0.2)