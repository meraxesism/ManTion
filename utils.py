import cv2
import logging
from datetime import datetime
from config import LOG_PATH
import numpy as np

# Skeleton connections for COCO format (17 keypoints)
POSE_CONNECTIONS = [
    (0, 1), (0, 2), (1, 3), (2, 4),  # Head to ears
    (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),  # Arms
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16)  # Hips and legs
]

COLORS = {
    'skeleton': (0, 200, 255),
    'joint': (0, 255, 0),
    'bbox': (0, 0, 255),
    'text': (255, 255, 255)
}


def setup_logging():
    # Configure logging once
    if not logging.getLogger().handlers:
        logging.basicConfig(
            filename=LOG_PATH,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        # Also log to console
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(console)


def log_detection_event(label: str, confidence: float, bbox):
    try:
        logging.info(f"Detected {label} conf={confidence:.2f} bbox={bbox}")
    except Exception as e:
        logging.error(f"Logging error: {e}")


def draw_pose_results(frame, keypoints: np.ndarray, bboxes: np.ndarray, confidences: np.ndarray, class_names):
    # keypoints: (N, 17, 2 or 3), bboxes: (N, 4), confidences: (N,)
    num_instances = min(len(keypoints) if keypoints is not None else 0, len(bboxes) if bboxes is not None else 0)
    for i in range(num_instances):
        kp = keypoints[i]
        x1, y1, x2, y2 = map(int, bboxes[i])
        conf = float(confidences[i]) if confidences is not None and len(confidences) > i else 0.0

        # Draw bbox and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), COLORS['bbox'], 2)
        label = 'person'
        cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLORS['text'], 2, cv2.LINE_AA)

        # Draw joints and skeleton
        # Handle keypoints with (x,y) or (x,y,score)
        if kp.shape[1] == 2:
            pts = kp
            scores = np.ones((kp.shape[0],), dtype=np.float32)
        else:
            pts = kp[:, :2]
            scores = kp[:, 2]

        for (a, b) in POSE_CONNECTIONS:
            if a < len(pts) and b < len(pts) and scores[a] > 0.3 and scores[b] > 0.3:
                ax, ay = int(pts[a][0]), int(pts[a][1])
                bx, by = int(pts[b][0]), int(pts[b][1])
                cv2.line(frame, (ax, ay), (bx, by), COLORS['skeleton'], 2)

        for j, (px, py) in enumerate(pts):
            if scores[j] > 0.3:
                cv2.circle(frame, (int(px), int(py)), 4, COLORS['joint'], -1)

    return frame


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
        keypoints = det.get('keypoints')
        if keypoints is not None:
            frame = draw_skeleton(frame, keypoints)
        cv2.rectangle(frame, (x1, y1), (x2, y2), COLORS['bbox'], 2)
        cv2.putText(frame, f"Human {conf:.2f}", (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, COLORS['bbox'], 2)
    return frame