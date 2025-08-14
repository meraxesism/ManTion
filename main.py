import cv2
import logging
import platform
import time
from alarm import Alarm
from config import CAMERA_INDEX
from utils import setup_logging
from line_control import LineController
from detector import Detector  # YOLOv8 + YOLOv8-Pose
from hand_detector import HandDetector  # Use user's proven hand detector

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

INDICATOR_POS = (20, 80)


def draw_line_status(frame, running: bool):
    color = (0, 255, 0) if running else (0, 0, 255)
    text = 'LINE: RUNNING' if running else 'LINE: STOPPED'
    cv2.rectangle(frame, (15, 20), (360, 110), (0, 0, 0), -1)
    cv2.putText(frame, text, INDICATOR_POS, cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2, cv2.LINE_AA)
    return frame


def open_capture(index: int) -> cv2.VideoCapture:
    is_windows = platform.system().lower() == 'windows'
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW) if is_windows else cv2.VideoCapture(index)
    if not cap.isOpened() and is_windows:
        cap = cv2.VideoCapture(index)
    if cap and cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
    return cap


# ----- Hand gesture helpers (MediaPipe Hands landmarks) -----
TIPS = [4, 8, 12, 16, 20]
PIPS = [3, 6, 10, 14, 18]

def classify_hand_state(hand_landmarks):
    """Classify 'open' vs 'fist' using simple fingertip-vs-PIP y heuristic (image origin top-left).
    Returns ('open'|'fist'|'none')."""
    if not hand_landmarks or len(hand_landmarks) < 21:
        return 'none'
    extended = 0
    for tip, pip in zip(TIPS[1:], PIPS[1:]):  # ignore thumb for robustness
        if hand_landmarks[tip][1] < hand_landmarks[pip][1]:
            extended += 1
    # Thumb horizontal distance as proxy for openness
    thumb_open = abs(hand_landmarks[4][0] - hand_landmarks[3][0]) > 10
    if extended >= 3 and thumb_open:
        return 'open'
    if extended <= 1:
        return 'fist'
    return 'none'


def main():
    alarm = Alarm()
    line = LineController()

    # Initialize detectors
    detector = Detector()  # YOLO general + YOLO pose overlay
    hand = HandDetector(max_hands=2, detection_conf=0.7, tracking_conf=0.7)

    # Debounce state for gestures
    last_state = 'none'
    last_change_ms = 0
    debounce_ms = 400

    cap = None
    try:
        for idx in [CAMERA_INDEX, 0, 1, 2]:
            cap = open_capture(idx)
            if cap.isOpened():
                current_index = idx
                logger.info(f"Camera opened on index {current_index}")
                break
        if cap is None or not cap.isOpened():
            raise IOError("Unable to open any camera.")

        cv2.namedWindow('Assembly Line Monitor', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Assembly Line Monitor', 1280, 720)

        failed_reads = 0
        max_failed_reads = 60

        while True:
            ret, frame = cap.read()
            if not ret:
                failed_reads += 1
                if failed_reads >= max_failed_reads:
                    cap.release()
                    cap = open_capture(current_index)
                    failed_reads = 0
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                continue
            failed_reads = 0

            # 1) YOLO general detection + YOLO-Pose overlay
            processed, human_detected, detections = detector.detect(frame)

            # 2) Hand detection (user's module)
            processed, hands = hand.detect_hands(processed, draw=True)

            # 3) Gesture classification with debounce
            state_text = ""
            current_state = 'none'
            if hands:
                # choose first hand (or refine to pick the larger hand bbox if needed)
                current_state = classify_hand_state(hands[0])
            now_ms = int(time.time() * 1000)
            if current_state != last_state and now_ms - last_change_ms > debounce_ms:
                last_state = current_state
                last_change_ms = now_ms
                if last_state == 'fist':
                    line.stop_line()
                    alarm.trigger()
                elif last_state == 'open':
                    line.start_line()
                    alarm.stop()
            if current_state in ('fist', 'open'):
                state_text = f"Gesture: {current_state}"
            else:
                state_text = "Keys: S=Stop (fist), G=Start (open), Q=Quit"

            # 4) Status overlays
            processed = draw_line_status(processed, line.is_running())
            if human_detected:
                cv2.putText(processed, "HUMAN DETECTED!", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)
            if state_text:
                cv2.putText(processed, state_text, (20, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 50), 2, cv2.LINE_AA)

            cv2.imshow('Assembly Line Monitor', processed)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            # Keyboard fallback
            if key == ord('s'):
                line.stop_line()
                alarm.trigger()
            elif key == ord('g'):
                line.start_line()
                alarm.stop()

    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
    finally:
        if cap is not None and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        alarm.stop()
        # hand detector cleanup
        try:
            hand.release()
        except Exception:
            pass


if __name__ == "__main__":
    main()
