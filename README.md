# ManTion: Industrial-Grade Human Pose Detection System

## Overview
**ManTion** is a state-of-the-art, real-time human pose (skeleton) detection and safety alert system designed for industrial environments. Built on YOLOv8-Pose, it provides robust, accurate detection of human presence and posture, with professional overlays, audible alarms, and comprehensive event logging—ensuring maximum operator safety on the assembly line.

---

## Key Features
- **Real-Time Human Skeleton Detection:** Stick-figure overlays for clear, modern visualization of human presence and posture.
- **Professional Visual Alerts:** Bold, non-intrusive overlays for both detection and safe states.
- **Audible Safety Alarm:** Reliable WAV-based alarm system with robust error handling.
- **Comprehensive Logging:** All detections, alarms, and errors are timestamped and logged for safety audits.
- **Automatic Image Capture on Detection:** Captures and saves 2–3 images per detection event with precise timestamped filenames for traceability.
- **Full-Screen Display Mode:** Automatically adjusts to fit screen for immersive industrial monitoring.
- **Hand Keypoint Detection (via Pose Model):** Displays extended keypoints including hands and wrists for enhanced safety coverage.
- **Industrial Reliability:** Graceful shutdown, error handling, and resource management.
- **Easy Configuration:** All parameters (model, camera, thresholds, alarm, logs) in a single `config.py` file.
- **Modular, Maintainable Codebase:** Clean, extensible Python modules for rapid adaptation and scaling.

---

## Setup
1. **Install Python 3.8+**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Download YOLOv8-Pose model weights:**
   - [yolov8n-pose.pt](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n-pose.pt)
   - Place in your project directory.
4. **Add a WAV alarm sound:**
   - [Download example](https://www.soundjay.com/button/beep-07.wav) and save as `alarm.wav` in your project directory.

---

## Usage
```bash
python main.py
```
- The system will open a live camera feed with real-time skeleton overlays.
- If a human is detected:
  - A visual warning and audible alarm will trigger.
  - 2–3 images will be saved automatically with current date and time.
- All events and errors are logged to `detections.log`.
- Press `q` to quit safely.

---

## Customization
- **Model:** Update `MODEL_PATH` in `config.py` for custom-trained pose models.
- **Camera:** Change `CAMERA_INDEX` in `config.py` for different camera sources.
- **Detection Threshold:** Adjust `DETECTION_THRESHOLD` for sensitivity.
- **Alarm Sound:** Use any WAV file and update `ALARM_SOUND_PATH`.
- **Logging:** All logs are written to the path in `LOG_PATH`.
- **Image Saving Directory:** Change the output folder path in `config.py` under `IMAGE_SAVE_PATH`.

---

## Industrial Deployment Tips
- **Custom Training:** For highest accuracy, train YOLOv8-Pose on your own assembly line images.
- **Testing:** Validate under real lighting and camera positions.
- **Integration:** System can be extended for PLC, email/SMS, or dashboard integration.
- **Maintenance:** Monitor logs and periodically test alarm and detection accuracy.

---

## Support & Further Enhancements
- For advanced integration (multi-camera, dashboards, remote alerts), or custom training, contact your AI/ML team or the Ultralytics community.
- For troubleshooting, consult `detections.log` and ensure all dependencies and files are present.

---

**ManTion** — Professional safety, powered by AI.