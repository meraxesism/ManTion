# 🏗️ Architecture

This document describes the system architecture, components, and data flow.

## Overview
- Frontend: React + TypeScript UI with real-time status and overlays
- Backend: Flask REST API with threaded camera service
- AI: YOLOv8 for detection/pose, MediaPipe for hands, custom gesture engine
- Control: Line controller (PLC-ready) and alarm system
- Storage: SQLite for detections, model weights under models/

## Mermaid Diagram
```mermaid
flowchart LR
  subgraph FE[Frontend]
    UI[React 18 UI]
  end

  subgraph API[Backend API (Flask)]
    APIServer[Flask REST API]
    Camera[Camera Service (threaded)]
  end

  subgraph AI[AI Processing]
    YOLO[YOLOv8 Detection & Pose]
    Hands[MediaPipe Hands]
    Gesture[Gesture Engine]
  end

  subgraph CTRL[Control & Safety]
    Line[Line Controller (PLC-ready)]
    Alarm[Alarm System]
  end

  DB[(SQLite: detections.db)]
  Models[(models/: YOLO weights)]

  UI -->|HTTP/JSON| APIServer
  APIServer --> Camera
  Camera --> YOLO
  Camera --> Hands
  YOLO --> Gesture
  Hands --> Gesture
  Gesture --> Line
  Gesture --> Alarm
  APIServer --> DB
  YOLO --> DB
  Hands --> DB
  Models --- YOLO
```

## Technology Stack
- Frontend: React 18, TypeScript, Tailwind CSS
- Backend: Flask, Flask-CORS, threading
- AI/ML: YOLOv8, MediaPipe, OpenCV, NumPy
- Modules: api_server.py, camera_service.py, detector.py, hand_detector.py, line_control.py, alarm.py, config.py, utils.py
