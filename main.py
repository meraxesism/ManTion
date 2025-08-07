import cv2
import pyautogui
from detector import Detector
from hand_detector import HandDetector
from alarm import play_alarm
from utils import draw_detections, log_detection
from config import CAMERA_INDEX
import logging
import sys
import pygame
import os
from datetime import datetime

def save_detection_images(frame, count=3):
    now = datetime.now()
    date_folder = now.strftime("%Y-%m-%d")
    time_stamp = now.strftime("%H-%M-%S")

    folder_path = os.path.join("detections", date_folder)
    os.makedirs(folder_path, exist_ok=True)

    for i in range(count):
        filename = f"detection_{time_stamp}_{i+1}.jpg"
        file_path = os.path.join(folder_path, filename)
        cv2.imwrite(file_path, frame)

def main():
    logging.basicConfig(filename='detections.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s')

    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Get screen size for fullscreen display
    screen_width, screen_height = pyautogui.size()

    # Prepare fullscreen window
    cv2.namedWindow('Assembly Line Monitor', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Assembly Line Monitor', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    detector = Detector()
    hand_detector = HandDetector()
    alarm_triggered = False

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logging.error('Failed to read from camera.')
                break

            # --- Pose/Person Detection (YOLOv8) ---
            detections = detector.detect(frame)
            if detections:
                frame = draw_detections(frame, detections)
                cv2.putText(frame, "HUMAN DETECTED!", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                if not alarm_triggered:
                    play_alarm()
                    alarm_triggered = True
                    save_detection_images(frame, count=3)  # <-- Save 3 images
                log_detection(detections)
            else:
                cv2.putText(frame, "SAFE", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                alarm_triggered = False

            # --- Hand Detection (MediaPipe) ---
            frame, hand_landmarks = hand_detector.detect_hands(frame, draw=True)

            if hand_landmarks:
                logging.info(f"Detected {len(hand_landmarks)} hand(s) with landmarks.")

            # --- Resize frame to fullscreen ---
            frame = cv2.resize(frame, (screen_width, screen_height))

            # --- Display ---
            cv2.imshow('Assembly Line Monitor', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        logging.error(f"Fatal error: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.music.stop()
        logging.info('System shutdown.')

if __name__ == "__main__":
    main()
