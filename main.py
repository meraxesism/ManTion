import cv2
from detector import Detector
from alarm import play_alarm
from utils import draw_detections, log_detection
from config import CAMERA_INDEX
import logging
import sys
import pygame

def main():
    logging.basicConfig(filename='detections.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s')
    cap = cv2.VideoCapture(CAMERA_INDEX)
    detector = Detector()
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
                log_detection(detections)
            else:
                cv2.putText(frame, "SAFE", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                alarm_triggered = False
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