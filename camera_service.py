import cv2
import logging
import threading
import time
import platform
import os
import numpy as np
import asyncio
from alarm import Alarm
from line_control import LineController
from detector import Detector
from hand_detector import HandDetector
from config import CAMERA_INDEX

logger = logging.getLogger(__name__)

class CameraService:
    def __init__(self):
        self.is_running = False
        self.thread = None
        self.cap = None
        self.alarm = None
        self.line = None
        self.detector = None
        self.hand = None
        self.status = {
            'active': False,
            'human_detected': False,
            'gesture_state': 'none',
            'line_running': True,
            'camera_connected': False,
            'last_update': None
        }
        
        # Gesture debouncing
        self.last_state = 'none'
        self.last_change_ms = 0
        self.debounce_ms = int(os.environ.get('GESTURE_DEBOUNCE_MS', 400))
        
    def start(self):
        if self.is_running:
            logger.warning("Camera service already running")
            return False
            
        try:
            self.is_running = True
            self.thread = threading.Thread(target=self._run_detection, daemon=True)
            self.thread.start()
            logger.info("Camera service started")
            return True
        except Exception as e:
            logger.error(f"Failed to start camera service: {e}")
            self.is_running = False
            return False
    
    def stop(self):
        if not self.is_running:
            return
            
        self.is_running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
        
        if self.cap and self.cap.isOpened():
            self.cap.release()
        
        if self.alarm:
            self.alarm.stop()
            
        if self.hand:
            try:
                self.hand.release()
            except:
                pass
                
        logger.info("Camera service stopped")
    
    def get_status(self):
        self.status['last_update'] = datetime.now().isoformat()
        return self.status.copy()
    
    def _open_capture(self, index: int) -> cv2.VideoCapture:
        is_windows = platform.system().lower() == 'windows'
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW) if is_windows else cv2.VideoCapture(index)
        if not cap.isOpened() and is_windows:
            cap = cv2.VideoCapture(index)
        if cap and cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            cap.set(cv2.CAP_PROP_FPS, 30)
        return cap
    
    def _classify_hand_state(self, hand_landmarks):
        """Classify 'open' vs 'fist' using simple fingertip-vs-PIP y heuristic (image origin top-left).
        Returns ('open'|'fist'|'none')."""
        if not hand_landmarks or len(hand_landmarks) < 21:
            return 'none'
        extended = 0
        TIPS = [4, 8, 12, 16, 20]
        PIPS = [3, 6, 10, 14, 18]
        
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
    
    def _draw_line_status(self, frame, running):
        """Draw assembly line status on frame"""
        color = (0, 255, 0) if running else (0, 0, 255)
        text = 'LINE: RUNNING' if running else 'LINE: STOPPED'
        cv2.rectangle(frame, (15, 20), (360, 110), (0, 0, 0), -1)
        cv2.putText(frame, text, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2, cv2.LINE_AA)
        return frame
    
    def _run_detection(self):
        # Ensure we're running in a proper event loop context
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                asyncio.set_event_loop(asyncio.new_event_loop())
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())
        
        try:
            # Initialize components
            self.alarm = Alarm()
            self.line = LineController()
            self.detector = Detector()
            self.hand = HandDetector(max_hands=2, detection_conf=0.7, tracking_conf=0.7)
            
            # Try to open camera
            for idx in [CAMERA_INDEX, 0, 1, 2]:
                self.cap = self._open_capture(idx)
                if self.cap.isOpened():
                    current_index = idx
                    logger.info(f"Camera opened on index {current_index}")
                    self.status['camera_connected'] = True
                    break
            
            if not self.cap or not self.cap.isOpened():
                logger.error("Unable to open any camera")
                self.status['camera_connected'] = False
                return
            
            # Create OpenCV window
            cv2.namedWindow('Assembly Line Monitor', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Assembly Line Monitor', 1280, 720)
            
            failed_reads = 0
            max_failed_reads = 60
            
            while self.is_running:
                ret, frame = self.cap.read()
                if not ret:
                    failed_reads += 1
                    if failed_reads >= max_failed_reads:
                        if self.cap is not None:
                            self.cap.release()
                        self.cap = self._open_capture(current_index)
                        failed_reads = 0
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    continue
                
                failed_reads = 0
                
                # 1) YOLO general detection + YOLO-Pose overlay
                processed, human_detected, detections = self.detector.detect(frame)
                self.status['human_detected'] = human_detected
                
                # 2) Hand detection
                processed, hands = self.hand.detect_hands(processed, draw=True)
                
                # 3) Gesture classification with debounce
                state_text = ""
                current_state = 'none'
                if hands:
                    # choose first hand (or refine to pick the larger hand bbox if needed)
                    current_state = self._classify_hand_state(hands[0])
                
                now_ms = int(time.time() * 1000)
                if current_state != self.last_state and now_ms - self.last_change_ms > self.debounce_ms:
                    self.last_state = current_state
                    self.last_change_ms = now_ms
                    if self.last_state == 'fist':
                        self.line.stop_line()
                        self.alarm.trigger()
                        logger.info("Emergency stop triggered by fist gesture")
                    elif self.last_state == 'open':
                        self.line.start_line()
                        self.alarm.stop()
                        logger.info("System started by open palm gesture")
                
                if current_state in ('fist', 'open'):
                    state_text = f"Gesture: {current_state}"
                else:
                    state_text = "Keys: S=Stop (fist), G=Start (open), Q=Quit"
                
                # 4) Status overlays
                processed = self._draw_line_status(processed, self.line.is_running())
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
                    self.line.stop_line()
                    self.alarm.trigger()
                elif key == ord('g'):
                    self.line.start_line()
                    self.alarm.stop()
                
                # Update status
                self.status['active'] = True
                self.status['gesture_state'] = current_state
                self.status['line_running'] = self.line.is_running()
                
        except Exception as e:
            logger.error(f"Error in camera detection loop: {e}", exc_info=True)
            # User-facing error notification
            try:
                cv2.namedWindow('Error', cv2.WINDOW_NORMAL)
                error_img = np.zeros((200, 600, 3), dtype=np.uint8)
                cv2.putText(
                    error_img,
                    f"Fatal error: {e}",
                    (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA
                )
                cv2.imshow('Error', error_img)
                cv2.waitKey(3000)
                cv2.destroyWindow('Error')
            except Exception:
                pass
        finally:
            if self.cap is not None and hasattr(self.cap, 'isOpened') and self.cap.isOpened():
                self.cap.release()
            cv2.destroyAllWindows()
            if self.alarm is not None:
                self.alarm.stop()
            # hand detector cleanup
            try:
                if self.hand is not None:
                    self.hand.release()
            except Exception:
                pass
            self.status['active'] = False
            self.status['camera_connected'] = False
            logger.info("Camera service stopped")

# Global camera service instance
camera_service = CameraService()
