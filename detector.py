import cv2
from ultralytics import YOLO
from config import MODEL_PATH, DETECTION_THRESHOLD
import numpy as np
import logging

class Detector:
    def __init__(self):
        try:
            self.model = YOLO(MODEL_PATH)
        except Exception as e:
            logging.error(f"Model loading error: {e}")
            raise

    def detect(self, frame):
        try:
            results = self.model(frame, device='cpu')
            detections = []
            for r in results:
                for box, keypoints in zip(r.boxes, r.keypoints):
                    conf = float(box.conf[0])
                    if conf >= DETECTION_THRESHOLD:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        kps = keypoints.xy[0].cpu().numpy() if hasattr(keypoints.xy[0], 'cpu') else keypoints.xy[0]
                        detections.append({'conf': conf, 'bbox': (x1, y1, x2, y2), 'keypoints': kps})
            return detections
        except Exception as e:
            logging.error(f"Detection error: {e}")
            return []