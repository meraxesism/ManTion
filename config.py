import os
YOLO_MODEL_PATH = os.environ.get('YOLO_MODEL_PATH', 'yolov8n.pt')        # YOLOv8 general detector (person, etc.)
YOLO_POSE_MODEL_PATH = os.environ.get('YOLO_POSE_MODEL_PATH', 'yolov8n-pose.pt')  # YOLOv8 Pose for human skeletons
CAMERA_INDEX = int(os.environ.get('CAMERA_INDEX', 0))  # Change if using a different camera
DETECTION_THRESHOLD = float(os.environ.get('DETECTION_THRESHOLD', 0.4))  # Confidence threshold for detection
ALARM_SOUND_PATH = os.environ.get('ALARM_SOUND_PATH', 'alarm.wav')
LOG_PATH = os.environ.get('LOG_PATH', 'detections.log')