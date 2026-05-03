# ------------------------------------------------------
# IMPORT LIBRARIES
# ------------------------------------------------------

import cv2                 # OpenCV for webcam and image processing
import mediapipe as mp     # MediaPipe for hand tracking
import serial              # Serial communication with Arduino
import time                # Used for delay after opening serial


# ------------------------------------------------------
# SERIAL SETUP
# ------------------------------------------------------

PORT = "COM3"              # Change this to your Arduino COM port
BAUD_RATE = 9600           # Must match Arduino Serial.begin(9600)

arduino = serial.Serial(PORT, BAUD_RATE)   # Open serial connection
time.sleep(2)                               # Wait for Arduino to reset


# ------------------------------------------------------
# MEDIAPIPE SETUP
# ------------------------------------------------------

mp_hands = mp.solutions.hands               # Access hand tracking module
mp_draw = mp.solutions.drawing_utils        # Drawing utilities

hands = mp_hands.Hands(
    max_num_hands=1,                        # ONLY track one hand
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# ------------------------------------------------------
# WEBCAM SETUP (UPDATED)
# ------------------------------------------------------

cap = cv2.VideoCapture(0)   # Open default webcam

# I increase the camera resolution so the image is sharper and larger.
# Not all webcams support high resolution, but 1280x720 usually works.
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# I create a resizable window instead of the default fixed small one.
cv2.namedWindow("Robot Hand Control", cv2.WINDOW_NORMAL)

# I manually make the window bigger so it's easier to see.
# I can change these numbers if I want it even bigger.
cv2.resizeWindow("Robot Hand Control", 1000, 800)


# ------------------------------------------------------
# STORE LAST STATES (to avoid spamming Arduino)
# ------------------------------------------------------

last_states = {
    "THUMB": None,
    "POINTER": None,
    "MIDDLE": None,
    "RING": None,
    "PINKY": None
}


# ------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------

while True:

    success, frame = cap.read()       # Capture frame
    if not success:
        break

    frame = cv2.flip(frame, 1)        # Mirror image
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB

    result = hands.process(rgb)       # Run hand detection


    # Default states (all fingers up)
    states = {
        "THUMB": "UP",
        "POINTER": "UP",
        "MIDDLE": "UP",
        "RING": "UP",
        "PINKY": "UP"
    }


    # --------------------------------------------------
    # IF HAND DETECTED
    # --------------------------------------------------

    if result.multi_hand_landmarks:

        hand = result.multi_hand_landmarks[0]   # Get the hand

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        landmarks = []

        for lm in hand.landmark:
            h, w, _ = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            landmarks.append((cx, cy))


        # --------------------------------------------------
        # FINGER DETECTION
        # --------------------------------------------------

        # THUMB (uses X direction)
        if landmarks[4][0] < landmarks[3][0]:
            states["THUMB"] = "DOWN"

        # POINTER
        if landmarks[8][1] > landmarks[6][1]:
            states["POINTER"] = "DOWN"

        # MIDDLE
        if landmarks[12][1] > landmarks[10][1]:
            states["MIDDLE"] = "DOWN"

        # RING
        if landmarks[16][1] > landmarks[14][1]:
            states["RING"] = "DOWN"

        # PINKY
        if landmarks[20][1] > landmarks[18][1]:
            states["PINKY"] = "DOWN"


    # --------------------------------------------------
    # SEND SERIAL COMMANDS (ONLY WHEN CHANGED)
    # --------------------------------------------------

    for finger in states:

        command = f"{finger}_{states[finger]}"   # Example: POINTER_DOWN

        if last_states[finger] != command:
            arduino.write((command + "\n").encode())   # Send to Arduino
            print("Sent:", command)
            last_states[finger] = command


    # ------------------------------------------------------
    # DRAW STATUS TEXT ON SCREEN
    # ------------------------------------------------------

    cv2.putText(frame, f"Thumb:   {states['THUMB']}",   (20, 40),  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Pointer: {states['POINTER']}", (20, 70),  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Middle:  {states['MIDDLE']}",  (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Ring:    {states['RING']}",    (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Pinky:   {states['PINKY']}",   (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


    # I display the frame in the bigger window I created earlier.
    cv2.imshow("Robot Hand Control", frame)


    # I press q to quit the program.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# ------------------------------------------------------
# CLEANUP
# ------------------------------------------------------

cap.release()            # Release webcam
cv2.destroyAllWindows()  # Close window
arduino.close()          # Close serial connection