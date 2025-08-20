from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import os
import cv2
import traceback
from camera_service import camera_service

app = Flask(__name__)
CORS(app)

# In-memory settings and status (to be replaced with real logic)
settings = {
    'cameraIndex': 0,
    'detectionThreshold': 0.4,
    'maxHands': 2,
    'alarmEnabled': True,
    'debounceMs': 400,
    'resolution': '1280x720',
    'fps': 30
}
system_status = {
    'isSystemActive': False,
    'systemStatus': 'idle',
    'connectionStatus': 'disconnected'
}

@app.route('/api/cameras', methods=['GET'])
def get_cameras():
    cameras = []
    for idx in range(6):
        cap = cv2.VideoCapture(idx)
        if cap is not None and cap.isOpened():
            name = f"Camera {idx}"
            if idx == 0:
                name = "Built-in Camera"
            else:
                name = f"USB Camera {idx}"
            cameras.append({'index': idx, 'name': name, 'status': 'available'})
            cap.release()
        else:
            cameras.append({'index': idx, 'name': f'Camera {idx}', 'status': 'unavailable'})
    return jsonify(cameras)

@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify(settings)

@app.route('/api/settings', methods=['POST'])
def update_settings():
    data = request.json
    settings.update(data)
    return jsonify({'success': True, 'settings': settings})

@app.route('/api/start', methods=['POST'])
def start_system():
    try:
        if camera_service.is_running:
            return jsonify({'success': False, 'status': system_status, 'error': 'System already running'}), 400
        
        success = camera_service.start()
        if success:
            system_status['isSystemActive'] = True
            system_status['systemStatus'] = 'running'
            system_status['connectionStatus'] = 'connected'
            print('Started camera detection service')
            return jsonify({'success': True, 'status': system_status})
        else:
            system_status['isSystemActive'] = False
            system_status['systemStatus'] = 'idle'
            system_status['connectionStatus'] = 'disconnected'
            return jsonify({'success': False, 'error': 'Failed to start camera service', 'status': system_status}), 500
    except Exception as e:
        print('Failed to start camera service:', e)
        traceback.print_exc()
        system_status['isSystemActive'] = False
        system_status['systemStatus'] = 'idle'
        system_status['connectionStatus'] = 'disconnected'
        return jsonify({'success': False, 'error': str(e), 'status': system_status}), 500

@app.route('/api/stop', methods=['POST'])
def stop_system():
    try:
        camera_service.stop()
        system_status['isSystemActive'] = False
        system_status['systemStatus'] = 'idle'
        system_status['connectionStatus'] = 'disconnected'
        print('Stopped camera detection service')
        return jsonify({'success': True, 'status': system_status})
    except Exception as e:
        print('Error stopping camera service:', e)
        return jsonify({'success': False, 'error': str(e), 'status': system_status}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    if camera_service.is_running:
        system_status['isSystemActive'] = True
        system_status['systemStatus'] = 'running'
        system_status['connectionStatus'] = 'connected'
    else:
        system_status['isSystemActive'] = False
        system_status['systemStatus'] = 'idle'
        system_status['connectionStatus'] = 'disconnected'
    return jsonify(system_status)

@app.route('/api/camera-status', methods=['GET'])
def get_camera_status():
    """Get detailed camera detection status"""
    return jsonify(camera_service.get_status())

if __name__ == '__main__':
    # DO NOT use debug or reloader when managing subprocesses
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
