#!/usr/bin/env python3
import modules
import argparse
import time

# Command line arguments
parser = argparse.ArgumentParser(description='Package Daemon')

parser.add_argument('--example', 
							metavar = '50', default = 50.0, type = float,
							help='Time in milliseconds to wait for combo buttons')

args = parser.parse_args()

# Package Daemon
class package_daemon:
    def __init__(self, args):
        self.args = args
        # TODO: get pins from modules pins_dict = {"in": [3,5,7], "out": [12, 16, 18, 22]}
        # TODO: initialize GPIO with pins_dict

    def cleanup(self):
        # TODO: cleanup GPIO

        pass

    def run(self):
        try:
            while True:
                # TODO: get data from camera
                # TODO: Do something with the data
                # TODO: text someone!
                pass
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.cleanup()
            print("Kaaaaaahhhnnnnn!!!")

# Run the daemon
if __name__ == "__main__":
    daemon = package_daemon( args )
    daemon.run()