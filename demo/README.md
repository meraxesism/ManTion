# ManTion Demo Assets

This directory contains visual demonstrations of ManTion in action.

## Screenshots

### Web Interface
- `web-interface-dashboard.png` - Main dashboard with system status
- `web-interface-settings.png` - Configuration panel
- `web-interface-monitoring.png` - Real-time monitoring view

### Detection System
- `detection-human-pose.png` - YOLO human detection with pose estimation
- `detection-hand-tracking.png` - MediaPipe hand tracking overlay
- `gesture-fist-emergency.png` - Fist gesture triggering emergency stop
- `gesture-palm-restart.png` - Open palm gesture for system restart

### System Status
- `line-running-status.png` - Assembly line in running state
- `line-stopped-alert.png` - Emergency stop with visual alerts
- `multi-camera-view.png` - Multiple camera monitoring setup

## GIFs/Videos

### Core Functionality
- `gesture-control-demo.gif` - Complete gesture control workflow
- `real-time-detection.gif` - Live human and hand detection
- `emergency-stop-sequence.gif` - Emergency stop activation and recovery

### Performance Demos
- `30fps-processing.gif` - Real-time 30 FPS processing demonstration
- `multi-hand-tracking.gif` - Multiple hand tracking capabilities

## Creating Demo Content

To capture your own demo content:

1. **Screenshots**: Use your system's screenshot tool while ManTion is running
2. **GIFs**: Use tools like OBS Studio, LICEcap, or ScreenToGif
3. **Performance metrics**: Run `python benchmark.py` to generate real data

## Usage in Documentation

Reference these assets in README.md:
```markdown
![ManTion Dashboard](demo/web-interface-dashboard.png)
![Gesture Control Demo](demo/gesture-control-demo.gif)
```
