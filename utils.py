import cv2
import logging
from config import LOG_PATH
import numpy as np

# Skeleton connections for COCO format (17 keypoints)
POSE_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),      # Nose -> LEye -> REye -> LEar -> REar
    (0, 5), (5, 7), (7, 9),              # Nose -> LShoulder -> LElbow -> LWrist
    (0, 6), (6, 8), (8, 10),             # Nose -> RShoulder -> RElbow -> RWrist
    (5, 6), (5, 11), (6, 12),            # LShoulder <-> RShoulder, LShoulder -> LHip, RShoulder -> RHip
    (11, 12), (11, 13), (13, 15),        # LHip <-> RHip, LHip -> LKnee -> LAnkle
    (12, 14), (14, 16)                   # RHip -> RKnee -> RAnkle
]

COLORS = {
    'skeleton': (0, 255, 255),
    'joint': (0, 128, 255),
    'bbox': (0, 0, 255)
}

def draw_skeleton(frame, keypoints):
    keypoints = np.array(keypoints, dtype=np.int32)
    # Draw skeleton lines
    for i, j in POSE_CONNECTIONS:
        if i < len(keypoints) and j < len(keypoints):
            pt1, pt2 = tuple(keypoints[i]), tuple(keypoints[j])
            cv2.line(frame, pt1, pt2, COLORS['skeleton'], 2)
    # Draw joints
    for x, y in keypoints:
        cv2.circle(frame, (x, y), 4, COLORS['joint'], -1)
    return frame

def draw_detections(frame, detections):
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        conf = det['conf']
        keypoints = det['keypoints']
        frame = draw_skeleton(frame, keypoints)
        cv2.rectangle(frame, (x1, y1), (x2, y2), COLORS['bbox'], 2)
        cv2.putText(frame, f"Human {conf:.2f}", (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, COLORS['bbox'], 2)
    return frame

def log_detection(detections):
    try:
        logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                            format='%(asctime)s %(message)s')
        for det in detections:
            logging.info(f"Detected human with confidence {det['conf']:.2f} at {det['bbox']}")
    except Exception as e:
        logging.error(f"Logging error: {e}")