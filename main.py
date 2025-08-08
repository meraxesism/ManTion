import cv2
import pyautogui
from detector import Detector
from hand_detector import HandDetector
from alarm import play_alarm
from utils import draw_detections
from config import CAMERA_INDEX
import logging
import sys
import pygame
import os
import sqlite3
from datetime import datetime
import time

# Clip recording duration (seconds)
CLIP_DURATION = 5
DB_FILE = "detections.db"

def init_db():
    """Initialize SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            detection_type TEXT,
            clip_path TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_detection_db(detection_type, clip_path):
    """Log detection in SQLite DB."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO detections (timestamp, detection_type, clip_path) VALUES (?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), detection_type, clip_path)
    )
    conn.commit()
    conn.close()

def save_detection_clip(cap, duration=CLIP_DURATION):
    """Records a short video clip from the camera."""
    now = datetime.now()
    date_folder = now.strftime("%Y-%m-%d")
    time_stamp = now.strftime("%H-%M-%S")

    folder_path = os.path.join("detections", date_folder)
    os.makedirs(folder_path, exist_ok=True)

    filename = f"detection_clip_{time_stamp}.mp4"
    file_path = os.path.join(folder_path, filename)

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(file_path, fourcc, fps, (width, height))

    start_time = time.time()
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    out.release()
    logging.info(f"Saved detection clip: {file_path}")
    return file_path

def main():
    logging.basicConfig(filename='detections.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s')

    init_db()

    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    screen_width, screen_height = pyautogui.size()
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

            detections = detector.detect(frame)
            if detections:
                frame = draw_detections(frame, detections)
                cv2.putText(frame, "HUMAN DETECTED!", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                if not alarm_triggered:
                    play_alarm()
                    alarm_triggered = True
                    clip_path = save_detection_clip(cap, CLIP_DURATION)
                    log_detection_db("human", clip_path)
            else:
                cv2.putText(frame, "SAFE", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                alarm_triggered = False

            frame, hand_landmarks = hand_detector.detect_hands(frame, draw=True)
            if hand_landmarks:
                logging.info(f"Detected {len(hand_landmarks)} hand(s) with landmarks.")

            frame = cv2.resize(frame, (screen_width, screen_height))
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
