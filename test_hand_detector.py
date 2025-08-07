# test_hand_detector.py

import cv2
from hand_detector import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector()

while True:
    success, frame = cap.read()
    if not success:
        break

    frame, landmarks = detector.detect_hands(frame, draw=True)

    cv2.imshow("Hand Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
