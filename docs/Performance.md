# 📊 Performance & Scalability

This document summarizes performance guidance and example results. Your results will vary based on hardware, camera, and settings.

## How to Benchmark
- Run `python benchmark.py` for model and detection timings
- Monitor CPU/GPU usage with your OS tools
- Adjust resolution and frame skip in `camera_service.py`

## Example Results (Local Test Setup)
- Model Loading: ~1.2s
- Detection Speed: ~23ms avg
- Theoretical FPS: ~40-45
- Memory Usage: ~180MB
- Camera FPS: 30

## Tuning Tips
- Reduce input resolution (e.g., 640x360)
- Process every 2nd/3rd frame for UI smoothness
- Limit YOLO classes and use `imgsz=640`
- If available, set `YOLO_DEVICE=cuda` for GPU

## Scaling Considerations
- One camera per processing thread
- For multiple cameras, run multiple API instances or scale on Kubernetes
- Use persistent volumes for logs/models and centralized logging
