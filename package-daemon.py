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

    def cleanup(self):
        pass

    def run(self):
        try:
            while True:
                pass #do something here
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.cleanup()
            print("Exiting Package Daemon")

# Run the daemon
if __name__ == "__main__":
    daemon = package_daemon( args )
    daemon.run()