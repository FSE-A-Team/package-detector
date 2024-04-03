#!/usr/bin/env python3
from modules import crypto, gpio, pressure, sms, SQL, steppers, animation,camera
import argparse
import time
import os

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
        #GPIO
        pins_dict = {"in":[], "out":steppers.PINS}
        gpio.setup(pins_dict)

        #SQL CREDENTIALS
        SQL.init()
        self.credentials = SQL.loadCredentials()
        self.credentials[0]["pk"] = 'raspberry'
        sms.set_credentials(self.credentials[0])
        print("Credentials loaded: ", self.credentials[0])
        

    def cleanup(self):
        # TODO: cleanup GPIO

        pass

    def run(self):
        try:
            item_found = camera.main()
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
            
            if item_found:
                print("found the package!")
                animation.play()
                steppers.step_motor(1000)
                print("SENDING SMS...")
                
                sms.send_sms_via_email('6025618306@tmomail.net', 'You have a package!')
                #sms.send_sms_via_email('holgate.mark1@gmail.com', 'You have a package!')
                
                
            while True:
                if item_found: 
                    self.cleanup()
                    break
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