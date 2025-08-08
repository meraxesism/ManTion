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
- **10-Second Clip Recording Around Detections:** Records video clips capturing 5 seconds before and 5 seconds after each detection event, providing valuable context for safety review.  
- **SQLite Database Logging:** Detection events are logged to an SQLite database, enabling structured storage and easy querying.  
- **Detection History Viewer Script:** A provided viewer script allows quick inspection of detection logs in a tabular format without manual file parsing.  
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
  - A 10-second video clip will be recorded, capturing 5 seconds before and 5 seconds after detection for detailed context.  
- All events and errors are logged to an SQLite database for structured storage and easy querying (replacing `detections.log`).  
- Use the provided viewer script to inspect detection history in a table format without manual log file access.  
- Press `q` to quit safely.

---

## Customization
- **Model:** Update `MODEL_PATH` in `config.py` for custom-trained pose models.  
- **Camera:** Change `CAMERA_INDEX` in `config.py` for different camera sources.  
- **Detection Threshold:** Adjust `DETECTION_THRESHOLD` for sensitivity.  
- **Alarm Sound:** Use any WAV file and update `ALARM_SOUND_PATH`.  
- **Logging:** Logs are now stored in an SQLite database configured in `config.py` under `DB_PATH`.  
- **Image Saving Directory:** Change the output folder path in `config.py` under `IMAGE_SAVE_PATH`.  
- **Clip Recording Duration:** Configure pre- and post-detection clip durations (`CLIP_PRE_SECONDS` and `CLIP_POST_SECONDS`) in `config.py`.

---

## Industrial Deployment Tips
- **Custom Training:** For highest accuracy, train YOLOv8-Pose on your own assembly line images.  
- **Testing:** Validate under real lighting and camera positions.  
- **Integration:** System can be extended for PLC, email/SMS, or dashboard integration.  
- **Maintenance:** Monitor logs (via SQLite database) and periodically test alarm, clip recording, and detection accuracy.

---

## Support & Further Enhancements
- For advanced integration (multi-camera, dashboards, remote alerts), or custom training, contact your AI/ML team or the Ultralytics community.  
- For troubleshooting, consult the SQLite database logs or `detections.log` if enabled, and ensure all dependencies and files are present.  
- Use the detection history viewer script to streamline audit and review processes.

---

**ManTion** — Professional safety, powered by AI.
