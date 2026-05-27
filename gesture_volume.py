import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.utils import AudioUtilities
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_angle = None
current_vol = 0.5
devices = AudioUtilities.GetSpeakers()
volume_ctrl = devices.EndpointVolume

while True:
    ret, frame = cap.read()
    h, w, c = frame.shape
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks,
                                   mp_hands.HAND_CONNECTIONS)
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)
            # print(x)
            # print(y)
            cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)
            if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:
                print("pointing!")
                angle = math.atan2(
                    hand_landmarks.landmark[8].y -
                    hand_landmarks.landmark[5].y,
                    hand_landmarks.landmark[8].x - hand_landmarks.landmark[5].x
                )
                if prev_angle is not None:
                    delta = angle - prev_angle
                    if delta > math.pi:
                        delta -= 2 * math.pi
                    if delta < -math.pi:
                        delta += 2 * math.pi
                    if abs(delta) < 0.3:
                        if delta < 0:
                            pyautogui.press('volumeup')
                        elif delta > 0:
                            pyautogui.press('volumedown')
                        print(f"vol: {current_vol:.2f} delta: {delta:.3f}")
                        volume_ctrl.SetMasterVolumeLevelScalar(
                            current_vol, None)
                prev_angle = angle
    cv2.imshow("Gesture Volume", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
