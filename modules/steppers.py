try:
    from modules import gpio
except:
    import gpio
import time


# Define the GPIO signals to use that are connected to the stepper motor: IN1-IN4
PINS = [31, 33, 35, 37]

# Define the sequence of control signals for 4-step sequence
step_sequence = [
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1]
]

rev_sequence = [
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [0, 1, 1, 0],
    [1, 0, 1, 0]
]

old_step_sequence = [
    [1, 0, 0, 1],
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1]
]

old_rev_sequence2 = [
    [0, 0, 1, 1],
    [0, 1, 1, 0],
    [1, 1, 0, 0],
    [1, 0, 0, 1]
]

sleep_time = .0015

def initialize():
    gpio.setup({"in":[],"out":PINS})

    
# Function for stepping the motor
def step_motor(steps=50, direction=1):
    global sleep_time
    # Loop through the steps
    # Forward if direction = 1, Reverse if direction = -1
    #sleep_time += 0.001
    for i in range(steps):
        for fullstep in range(4):
            for pin in range(4):
                if (direction == 1):
                    gpio.write_pin(PINS[pin], step_sequence[(fullstep + direction) % 4][pin])
                else:
                    gpio.write_pin(PINS[pin], rev_sequence[(fullstep + direction) % 4][pin])
                #GPIO.output(control_pins[pin], step_sequence[(halfstep + direction) % 4][pin])
            time.sleep(sleep_time)

# TODO: Implement the following functions
# Function to open lid
def open_lid():
    step_motor(150, -1)

#function to close lid
def close_lid():
    step_motor(130, 1)

#function get status of motor
def get_status():
    #create global variable and set it when motor is running/idle
    pass

if __name__=="__main__":
    gpio.setup({"in":[],"out":PINS})
    
    while True:
      try:
        open_lid()
        time.sleep(.5)
        close_lid()
        time.sleep(2)
      except:
        gpio.cleanup()