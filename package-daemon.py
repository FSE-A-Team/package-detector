#!/usr/bin/env python3
from modules import camera, crypto, gpio, pressure, sms, SQL, steppers
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
        SQL.init()
        self.credentials = SQL.loadCredentials()
        self.credentials[0]["pk"] = 'raspberry'
        sms.set_credentials(self.credentials[0])
        print("Credentials loaded: ", self.credentials[0])
        sms.send_sms_via_email('6025618306@tmomail.net', 'Hello, World! This is a test message!')

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