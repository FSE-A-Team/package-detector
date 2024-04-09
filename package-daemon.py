#!/usr/bin/env python3
from modules import crypto, gpio, pressure, sms, SQL, steppers, camera#, animation
import argparse
import time
import asyncio, threading
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


        # Pressure sensor
        self.pSensor = pressure.Sensor()
        
        steppers.initialize()
        
        #SQL database
        SQL.init()
        self.credentials = SQL.loadCredentials()
        if self.credentials is None:
            print("No credentials found!")
        else:
            self.credentials[0]["pk"] = 'raspberry'
            sms.set_credentials(self.credentials[0])
            print("Credentials loaded: ", self.credentials[0])

       

    def cleanup(self):
        # TODO: cleanup GPIO
        self.pressure_task.cancel()
        pass

    async def main(self):
        self.pressure_task = asyncio.create_task(self.pSensor.run())
        while(True):
            try:
                initial_package_count = 0
                item_found = camera.main()
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear console

                if item_found:
                    print("looking for pressure change...")

                    steppers.open_lid()
                    await asyncio.sleep(3)
                    steppers.close_lid()

                    package_count, package_list = await self.pSensor.get_package_count()
                    while package_count < initial_package_count:
                        package_count, package_list = await self.pSensor.get_package_count()
                        await asyncio.sleep(1)  # Use asyncio.sleep instead of time.sleep
                    print("found the package! " + item_found)
                    #animation.play()
                   
                    print("SENDING SMS...")
                    sms.send_sms_via_email('eelksemaj@gmail.com', 'A ' + item_found + ' is in your box!!!')
                    
                    #sms.send_sms_via_email('6025618306@tmomail.net', 'You have a package!')
                    #sms.send_sms_via_email('holgate.mark1@gmail.com', 'You have a package!')
                print("packages: " + str(await self.pSensor.get_package_count()))
                
                await asyncio.sleep(1)  # Use asyncio.sleep instead of time.sleep
                    
            except KeyboardInterrupt:
                self.cleanup()
                print("Kaaaaaahhhnnnnn!!!")

# Run the daemon
if __name__ == "__main__":
    daemon = package_daemon( args )
    asyncio.run(daemon.main())