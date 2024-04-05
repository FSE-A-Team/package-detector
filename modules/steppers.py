try:
    from modules import gpio
except:
    import gpio
import time


# Define the GPIO signals to use that are connected to the stepper motor: IN1-IN4
PINS = [31, 33, 35, 37]

# Define the sequence of control signals for 4-step sequence
step_sequence = [
    [1, 0, 0, 1],
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1]
]

rev_sequence = [
    [0, 0, 1, 1],
    [0, 1, 1, 0],
    [1, 1, 0, 0],
    [1, 0, 0, 1]
]

# Function for stepping the motor
def step_motor(steps=50, direction=1):
    # Loop through the steps
    # Forward if direction = 1, Reverse if direction = -1
    for i in range(steps):
        for fullstep in range(4):
            for pin in range(4):
                if (direction == 1):
                    gpio.write_pin(PINS[pin], step_sequence[(fullstep + direction) % 4][pin])
                else:
                    gpio.write_pin(PINS[pin], rev_sequence[(fullstep + direction) % 4][pin])
                #GPIO.output(control_pins[pin], step_sequence[(halfstep + direction) % 4][pin])
            time.sleep(0.002)

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

if __name__=="__main__":
    gpio.setup({"in":[],"out":PINS})
    step_motor()