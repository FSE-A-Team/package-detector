import argparse
import sys
import time
import asyncio

import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

try:
    from modules.utils import visualize
except ModuleNotFoundError:
    from utils import visualize

from picamera2 import Picamera2

# Global variables to calculate FPS
ITEM_SEARCH=["kite","frisbee","tie","umbrella"]
MATCH_THRESHOLD = 0.5 #MINIMUM SCORE TO CONSIDER A MATCH
ITEM_SEARCH_SLICE = 1 #ALLOW FOR MORE CATEGORIES TO BE MATCHED OVER TIME
SECONDS_TILL_LOOSENING_SEARCH = 5
SEARCH_TIME = time.time()


COUNTER, FPS = 0, 0
START_TIME = time.time()
picam2 = Picamera2()
picam2.preview_configuration.main.size = (800,600)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

async def run(model: str, max_results: int, score_threshold: float, 
        camera_id: int, width: int, height: int) -> None:
  """Continuously run inference on images acquired from the camera.

  Args:
    model: Name of the TFLite object detection model.
    max_results: Max number of detection results.
    score_threshold: The score threshold of detection results.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
  """


  # Define the window size
  window_name = 'FSE 100 Package Detector'
  window_width = 800  # Set the width to 800 pixels
  window_height = 600  # Set the height to 600 pixels

  # Create a named window
  cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)  # Create a resizable window
  cv2.resizeWindow(window_name, window_width, window_height)  # Resize the window

  # Position the window to the left edge of the screen
  x_position = 0  # Leftmost edge
  y_position = 100  # Top of the screen
  cv2.moveWindow(window_name, x_position, y_position)

  # Visualization parameters
  row_size = 50  # pixels
  left_margin = 24  # pixels
  text_color = (0, 0, 0)  # black
  font_size = 1
  font_thickness = 1
  fps_avg_frame_count = 10

  detection_frame = None
  detection_result_list = []

  def save_result(result: vision.ObjectDetectorResult, unused_output_image: mp.Image, timestamp_ms: int):
      global FPS, COUNTER, START_TIME
      

      # Calculate the FPS
      if COUNTER % fps_avg_frame_count == 0:
          FPS = fps_avg_frame_count / (time.time() - START_TIME)
          START_TIME = time.time()
      #print(result)
      detection_result_list.append(result)
      COUNTER += 1

  # Initialize the object detection model
  base_options = python.BaseOptions(model_asset_path=model)
  options = vision.ObjectDetectorOptions(base_options=base_options,
                                         running_mode=vision.RunningMode.LIVE_STREAM,
                                         max_results=max_results, score_threshold=score_threshold,
                                         result_callback=save_result)
  detector = vision.ObjectDetector.create_from_options(options)

  global SEARCH_TIME, ITEM_SEARCH_SLICE, ITEM_SEARCH, MATCH_THRESHOLD

  SEARCH_TIME = time.time()
  ITEM_SEARCH_SLICE = 1

  # Continuously capture images from the camera and run inference
  while True:

    # Allow for more categories to be matched over time
    if time.time() - SEARCH_TIME > SECONDS_TILL_LOOSENING_SEARCH:
        if ITEM_SEARCH_SLICE < len(ITEM_SEARCH):
            ITEM_SEARCH_SLICE += 1
            SEARCH_TIME = time.time()
        else: # If all categories have been searched, lower the threshold
            MATCH_THRESHOLD -= 0.05

    im= picam2.capture_array()  
#    success, image = cap.read()
    image=cv2.resize(im,(640,480))
    #image = cv2.flip(image, -1)

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

    # Run object detection using the model.
    detector.detect_async(mp_image, time.time_ns() // 1_000_000)

    # Show the FPS
    #fps_text = 'FPS = {:.1f}'.format(FPS)
    #text_location = (left_margin, row_size)
    current_frame = image
    #cv2.putText(current_frame, fps_text, text_location, cv2.FONT_HERSHEY_DUPLEX,
    #            font_size, text_color, font_thickness, cv2.LINE_AA)

    await asyncio.sleep(0.5)
    if detection_result_list:
        for detection in detection_result_list[0].detections:
            category = detection.categories[0]
            category_name = category.category_name
            category_score = category.score
            #print("Category Name: " + category_name)
            if category_name in ITEM_SEARCH[0:ITEM_SEARCH_SLICE] and category_score > MATCH_THRESHOLD:
               await asyncio.sleep(3)
               await cleanup(detector)
               print("I see a package!")
               return category_name
        current_frame = visualize(current_frame, detection_result_list[0], ITEM_SEARCH)
        detection_frame = current_frame
        detection_result_list.clear()

    if detection_frame is not None:
        cv2.imshow(window_name, detection_frame)

    # Stop the program if the ESC key is pressed.
    if cv2.waitKey(1) == 27:
      break

  await cleanup(detector)

async def cleanup(detector):
   detector.close()
   #cap.release()
   cv2.destroyAllWindows()

async def main(args):

  return await run(args.model, int(args.maxResults),
      args.scoreThreshold, int(args.cameraId), args.frameWidth, args.frameHeight)


if __name__ == '__main__':
  main()