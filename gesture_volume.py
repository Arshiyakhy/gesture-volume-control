import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_angle = None

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
                    print(delta)
                prev_angle = angle

    cv2.imshow("Gesture Volume", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
