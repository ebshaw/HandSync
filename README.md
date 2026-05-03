# HandSync
 Vision-controlled robotic hand using Python, MediaPipe, OpenCV, Arduino, and servo motors.

HandSync is a vision-controlled robotic hand that replicates real-time finger motion using a webcam.

## Tech Stack
- Python (OpenCV, MediaPipe)
- Arduino (C++)
- Serial USB Communication
- 5 Servo Motors

## Features
- Real-time hand tracking
- Independent control of 5 fingers
- Non-blocking servo control
- Tendon-driven actuation system

## How it Works
A webcam captures hand motion, Python processes the image using MediaPipe to detect finger positions, and sends commands via serial communication to an Arduino, which controls 5 servo motors to replicate the motion.

## Files
- Python script → hand tracking and signal generation
- Arduino code → servo control and actuation

## Demo Video
[Watch Demo]: https://drive.google.com/drive/folders/1ImXcnkaiK3UalOOUF89R0M4vEM9KCUiL?usp=sharing