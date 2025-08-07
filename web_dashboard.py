from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO, emit
import cv2
import threading
import time
import json
from datetime import datetime
from detector import Detector
from alarm import Alarm
from config import CAMERA_INDEX, DETECTION_THRESHOLD
import logging
from utils import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mantion_industrial_safety_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for multi-camera support
cameras = {}
detection_stats = {
    'total_detections': 0,
    'last_detection': None,
    'system_uptime': datetime.now(),
    'alarms_triggered': 0
}

class CameraManager:
    def __init__(self, camera_id, camera_index):
        self.camera_id = camera_id
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(camera_index)
        self.detector = Detector()
        self.alarm = Alarm()
        self.is_running = False
        self.last_detection = None
        
        if not self.cap.isOpened():
            logger.error(f"Failed to open camera {camera_index}")
            raise RuntimeError(f"Cannot open camera {camera_index}")
        
    def start(self):
        self.is_running = True
        threading.Thread(target=self._process_feed, daemon=True).start()
        logger.info(f"Camera {self.camera_id} started")
        
    def stop(self):
        self.is_running = False
        if self.cap.isOpened():
            self.cap.release()
            logger.info(f"Camera {self.camera_id} stopped")
            
    def _process_feed(self):
        while self.is_running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    logger.warning(f"Failed to read frame from camera {self.camera_id}")
                    time.sleep(0.1)
                    continue
                    
                # Perform detection with skeleton drawing
                processed_frame, human_detected, detections_info = self.detector.detect(frame)
                
                if human_detected:
                    detection_stats['total_detections'] += len(detections_info)
                    detection_stats['last_detection'] = datetime.now().isoformat()
                    detection_stats['alarms_triggered'] += 1
                    
                    # Trigger alarm
                    self.alarm.trigger()
                    
                    # Emit detection event to web clients
                    socketio.emit('detection_alert', {
                        'camera_id': self.camera_id,
                        'detections': len(detections_info),
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    # Stop alarm when no detection
                    self.alarm.stop()
                
                # Emit processed frame to web clients (with skeleton overlay)
                _, buffer = cv2.imencode('.jpg', processed_frame)
                frame_data = buffer.tobytes()
                socketio.emit(f'video_feed_{self.camera_id}', frame_data)
                
                time.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                logger.error(f"Error processing feed for camera {self.camera_id}: {e}")
                time.sleep(1)  # Wait before retrying

def initialize_cameras():
    """Initialize multiple cameras"""
    global cameras
    try:
        # Add cameras - you can modify this for your setup
        cameras['camera_1'] = CameraManager('camera_1', CAMERA_INDEX)
        # Add more cameras as needed:
        # cameras['camera_2'] = CameraManager('camera_2', 1)
        # cameras['camera_3'] = CameraManager('camera_3', 2)
        
        for camera in cameras.values():
            camera.start()
            
        logger.info(f"Initialized {len(cameras)} cameras")
        
    except Exception as e:
        logger.error(f"Failed to initialize cameras: {e}")
        raise

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """API endpoint for detection statistics"""
    uptime = datetime.now() - detection_stats['system_uptime']
    return jsonify({
        'total_detections': detection_stats['total_detections'],
        'last_detection': detection_stats['last_detection'],
        'alarms_triggered': detection_stats['alarms_triggered'],
        'uptime_seconds': int(uptime.total_seconds()),
        'cameras_active': len([c for c in cameras.values() if c.is_running])
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('status', {'message': 'Connected to ManTion Safety Control Center'})
    logger.info("Client connected to web dashboard")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info("Client disconnected from web dashboard")

if __name__ == '__main__':
    try:
        initialize_cameras()
        logger.info("Starting ManTion Safety Control Center web dashboard...")
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        logger.info("Shutting down ManTion Safety Control Center...")
        for camera in cameras.values():
            camera.stop()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        for camera in cameras.values():
            camera.stop() 