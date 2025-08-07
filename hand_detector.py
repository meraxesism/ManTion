# hand_detector.py

import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_hands=2, detection_conf=0.7, tracking_conf=0.7):
        self.max_hands = max_hands
        self.detection_conf = detection_conf
        self.tracking_conf = tracking_conf

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect_hands(self, frame, draw=True):
        """Returns processed frame and list of hand landmarks per hand."""
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        landmarks_list = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand_points = []
                for lm in hand_landmarks.landmark:
                    h, w, _ = frame.shape
                    x, y = int(lm.x * w), int(lm.y * h)
                    hand_points.append((x, y))
                landmarks_list.append(hand_points)

                if draw:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return frame, landmarks_list

    def release(self):
        self.hands.close()
