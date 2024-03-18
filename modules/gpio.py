import RPi.GPIO as GPIO

# Setup GPIO pins and initial states
def setup(pins_dict):
    #pins_dict -> {"in": [11, 13, 15, 19], "out": [12, 16, 18, 22]}
    global setup_called
    GPIO.setmode(GPIO.BOARD)  # or GPIO.BCM, depending on your pin numbering system
    # Set up each pin you plan to use
    # For example:
    for pin in pins_dict["in"]:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    for pin in pins_dict["out"]:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    setup_called = True

def check_setup():
    # Check if the setup function has been called
    global setup_called
    return setup_called

# Write to a pin
def write_pin(pin, state):
    GPIO.output(pin, state)

# Read from a pin
def read_pin(pin):
    return GPIO.input(pin)

# Clean up at the end of our program
def cleanup():
    GPIO.cleanup()
