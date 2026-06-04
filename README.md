# Gesture Volume Control 🖐️

Control your Windows system volume by rotating your index finger in the air — inspired by BMW iDrive's gesture control system.

## How it works
The app uses your webcam to detect your hand in real time. Point your index finger up and rotate your wrist like a dial to change the volume.

- Rotate clockwise → volume down
- Rotate counter-clockwise → volume up

## Setup

1. Clone the repo
2. Create a virtual environment and activate it
```bash
   python -m venv venv
   .\venv\Scripts\activate
```
3. Install dependencies
```bash
   python -m pip install opencv-python mediapipe pycaw comtypes numpy pyautogui
```
4. Run it
```bash
   python gesture_volume.py
```

## Requirements
- Windows 10/11
- Python 3.10+
- A webcam
