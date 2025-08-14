import cv2
from ultralytics import YOLO
from config import YOLO_MODEL_PATH, YOLO_POSE_MODEL_PATH, DETECTION_THRESHOLD
import numpy as np
import logging
from utils import draw_pose_results, log_detection_event

logger = logging.getLogger(__name__)

BOX_COLOR = (0, 0, 255)
TEXT_COLOR = (255, 255, 255)

class Detector:
    def __init__(self):
        try:
            self.det_model = YOLO(YOLO_MODEL_PATH)
            self.pose_model = YOLO(YOLO_POSE_MODEL_PATH)
            logger.info(f"YOLO models loaded: det={YOLO_MODEL_PATH}, pose={YOLO_POSE_MODEL_PATH}")
        except Exception as e:
            logger.error(f"Model loading error: {e}")
            raise

    def detect(self, frame):
        processed_frame = frame.copy()
        human_detected = False
        detections_info = []
        try:
            # 1) General detection (person, etc.)
            det_results = self.det_model(frame, device='cpu', conf=DETECTION_THRESHOLD)
            for r in det_results:
                if getattr(r, 'boxes', None) is not None and len(r.boxes) > 0:
                    b_xyxy = r.boxes.xyxy
                    b_conf = r.boxes.conf
                    b_cls = r.boxes.cls
                    names = self.det_model.names
                    for i in range(len(b_xyxy)):
                        conf = float(b_conf[i])
                        cls_id = int(b_cls[i]) if b_cls is not None else -1
                        label = names.get(cls_id, str(cls_id)) if isinstance(names, dict) else names[cls_id]
                        x1, y1, x2, y2 = map(int, b_xyxy[i])
                        if conf >= DETECTION_THRESHOLD:
                            if label == 'person':
                                human_detected = True
                            detections_info.append({'label': label, 'conf': conf, 'bbox': (x1, y1, x2, y2)})
                            log_detection_event(label, conf, (x1, y1, x2, y2))
                            cv2.rectangle(processed_frame, (x1, y1), (x2, y2), BOX_COLOR, 2)
                            cv2.putText(processed_frame, f"{label} {conf:.2f}", (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, TEXT_COLOR, 2, cv2.LINE_AA)

            # 2) YOLOv8-Pose for skeleton overlay (humans only)
            pose_results = self.pose_model(frame, device='cpu', conf=DETECTION_THRESHOLD)
            for r in pose_results:
                if getattr(r, 'keypoints', None) is not None and r.keypoints is not None:
                    try:
                        kps = r.keypoints.xy
                        bxs = r.boxes.xyxy if getattr(r, 'boxes', None) is not None else np.zeros((0, 4))
                        confs = r.boxes.conf if getattr(r, 'boxes', None) is not None else np.zeros((0,))
                        kps = kps.cpu().numpy() if hasattr(kps, 'cpu') else np.asarray(kps)
                        bxs = bxs.cpu().numpy() if hasattr(bxs, 'cpu') else np.asarray(bxs)
                        confs = confs.cpu().numpy() if hasattr(confs, 'cpu') else np.asarray(confs)
                        processed_frame = draw_pose_results(processed_frame, kps, bxs, confs, self.pose_model.names)
                    except Exception as e:
                        logger.warning(f"Pose draw error: {e}")

            return processed_frame, human_detected, detections_info
        except Exception as e:
            logger.error(f"Detection error: {e}")
            return frame, False, []