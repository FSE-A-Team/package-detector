#import RPi.GPIO as GPIO
from modules import gpio
import time


# Define the GPIO signals to use that are connected to the stepper motor: IN1-IN4
PINS = [11, 13, 15, 19]

# Define the sequence of control signals for 4-step sequence
step_sequence = [
    [1, 0, 0, 1],
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1]
]

# Function for stepping the motor
def step_motor(steps=50, direction=1):
    # Loop through the steps
    # Forward if direction = 1, Reverse if direction = -1
    for i in range(steps):
        for fullstep in range(4):
            for pin in range(4):
                gpio.write_pin(PINS[pin], step_sequence[(fullstep + direction) % 4][pin])
                #GPIO.output(control_pins[pin], step_sequence[(halfstep + direction) % 4][pin])
            time.sleep(0.01)

# TODO: Implement the following functions
# Function to open lid
def open_lid():
    pass

#function to close lid
def close_lid():
    pass

#function get status of motor
def get_status():
    #create global variable and set it when motor is running/idle
    pass

