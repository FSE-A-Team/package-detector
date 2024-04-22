#!/usr/bin/env python3
import argparse
# Command line arguments
parser = argparse.ArgumentParser(description='Package Daemon',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--test', 
                    action='store_true',
                    help='Run in test mode')

parser.add_argument('--email',
                    metavar = 'email', 
                    default = 'eelksemaj@gmail.com', 
                    type = str,
                    help='Email to send SMS alerts')

# args for camera
parser.add_argument('--model',
                    help='Path of the object detection model.',
                    required=False,
                    default='efficientdet_lite0.tflite')
                    #default='best.tflite')

parser.add_argument('--maxResults',
                    help='Max number of detection results.',
                    required=False,
                    default=3)

parser.add_argument('--scoreThreshold',
                    help='The score threshold of detection results.',
                    required=False,
                    type=float,
                    default=0.25)
# Finding the camera ID can be very reliant on platform-dependent methods. 
# One common approach is to use the fact that camera IDs are usually indexed sequentially by the OS, starting from 0. 
# Here, we use OpenCV and create a VideoCapture object for each potential ID with 'cap = cv2.VideoCapture(i)'.
# If 'cap' is None or not 'cap.isOpened()', it indicates the camera ID is not available.
parser.add_argument('--cameraId', 
                    help='Id of camera.', 
                    required=False, 
                    type=int, 
                    default=0)

parser.add_argument('--frameWidth',
                    help='Width of frame to capture from camera.',
                    required=False,
                    type=int,
                    default=640)

parser.add_argument('--frameHeight',
                    help='Height of frame to capture from camera.',
                    required=False,
                    type=int,
                    default=480)

args = parser.parse_args()

if args.test:
    from modules import crypto
    from modules import pressure
    from modules import camera
    from modules import gpio, steppers
    from modules import SQL
    from modules import sms
else:
    from modules import crypto, gpio, pressure, sms, SQL, steppers, camera#, animation

import time
import asyncio, threading
import os



# Package Daemon
class package_daemon:
    def __init__(self, args):
        # Command line arguments
        self.args = args

        # Stepper motors
        steppers.initialize()
        
        #SQL database
        SQL.init()
        self.credentials = SQL.loadCredentials()
        if self.credentials is None:
            print("No credentials found!")
        else:
            self.credentials[0]["pk"] = 'raspberry'
            sms.set_credentials(self.credentials[0])
            sms.set_recipient(self.args.email)
            

        # Pressure sensor
        self.pSensor = pressure.Sensor(sms, test=args.test)

       
    def cleanup(self):
        steppers.cleanup()
        self.pressure_task.cancel()

    async def main(self):
        # create asynchronous task for pressure sensor
        self.pressure_task = asyncio.create_task(self.pSensor.run())
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
        while(True):
            try:

                item_found = await camera.main(self.args)
                
                
                if item_found:
                    print("Dropping Package...")
                    await self.pSensor.set_added_new_box()
                    await asyncio.sleep(0.1)
                    
                    steppers.open_lid()
                    await asyncio.sleep(3)
                    print("Looking for pressure change...")
                    print()
                    steppers.close_lid()
                    #animation.play()
                    item_found = None
                await asyncio.sleep(1)  # Use asyncio.sleep instead of time.sleep
                    
            except KeyboardInterrupt:
                self.cleanup()
                print("Kaaaaaahhhnnnnn!!!")

# Run the daemon
if __name__ == "__main__":
    daemon = package_daemon( args )
    asyncio.run(daemon.main())