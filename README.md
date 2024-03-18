# Package Detection System
Group: Mark Holgate, Lily Jones, Mudit Garg, James Lee

## Important Codes
Team locker code - 25_03_09

## Overview: 
We are building a system that detects packages for the sight-impaired. 
See System Diagram Here: https://miro.com/app/board/uXjVNnaeYi0=/

## Classes:
- Box Open and Close Detection - Detects if Box is open or closed
- Image Classifier - Using TensorFlow, we will train our model with labeled images of boxes and parcels.
- Weight Interpreter - Captures the weight data of object and stores as serialized data. 
- Final Classifier - From image and weight information, we categorize the output into different potential messages.
- Message Creator and Sender - Create message based on how the image and weights are classified and send SMS. 

## Tools and Libraries:
- Written in Python3
- Using Raspberry Pi v. 4
- TensorFlow for Image Classification


## TODOs:
- Build TensorFlow base image recognition model
- Train Model with Box Images
- Write Weight Interpreter Code
- Create Classes that incorporate all the codes
- Write SMS Script
- To recognize a package using the Raspberry Pi Camera Module v1.3, you'll need to use computer vision techniques to process the images captured by the camera. One popular library for computer vision in Python is OpenCV. 
## Work Done: 
- Stepper motor has been programmed.
- SMS sender has been programmed.
 

