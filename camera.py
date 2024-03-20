import cv2
import picamera2
import time
import pyzbar.pyzbar as pyzbar

# Initialize the camera
camera = picamera2.Picamera2()

# Set the resolution of the image
camera.resolution = (1024, 1024)

# Start the camera preview
camera.start()

# Wait for a short period to allow the camera to adjust its settings
time.sleep(2)

# Take a picture
camera.start_and_capture_file('image.jpg')

# Stop the camera preview
camera.stop()

# Convert the captured image to RGB
image = cv2.imread('image.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Decode the barcode in the image
barcodes = pyzbar.decode(image)

# Initialize a variable to store the barcode data
barcode_data = None

# Loop through the barcodes and find the first one
for barcode in barcodes:
    barcode_data = barcode.data.decode('utf-8')
    break

# Check if a barcode was found
if barcode_data is not None:
    # Print the barcode data
    print("Barcode data: {}".format(barcode_data))
else:
    print("No barcode detected in the image.")


