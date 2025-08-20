#!/usr/bin/env python3
"""
ManTion Performance Benchmarking Script
Generates real performance metrics for documentation
"""

import time
import psutil
import cv2
import numpy as np
import json
import sys
import os
from datetime import datetime
from detector import Detector
from hand_detector import HandDetector

class ManTionBenchmark:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "system_info": self._get_system_info(),
            "benchmarks": {}
        }
        
    def _get_system_info(self):
        return {
            "cpu": {
                "model": "Unknown",  # Would need platform-specific detection
                "cores": psutil.cpu_count(),
                "frequency": psutil.cpu_freq().current if psutil.cpu_freq() else "Unknown"
            },
            "memory": {
                "total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "available_gb": round(psutil.virtual_memory().available / (1024**3), 2)
            },
            "python_version": sys.version.split()[0]
        }
    
    def benchmark_model_loading(self):
        """Benchmark AI model initialization time"""
        print("🔄 Benchmarking model loading...")
        
        start_time = time.time()
        detector = Detector()
        detector_load_time = time.time() - start_time
        
        start_time = time.time()
        hand_detector = HandDetector(max_hands=2, detection_conf=0.7, tracking_conf=0.7)
        hand_load_time = time.time() - start_time
        
        total_load_time = detector_load_time + hand_load_time
        
        self.results["benchmarks"]["model_loading"] = {
            "yolo_load_time_ms": round(detector_load_time * 1000, 2),
            "mediapipe_load_time_ms": round(hand_load_time * 1000, 2),
            "total_load_time_ms": round(total_load_time * 1000, 2)
        }
        
        print(f"✅ Model loading: {total_load_time:.2f}s")
        return detector, hand_detector
    
    def benchmark_detection_performance(self, detector, hand_detector, num_frames=100):
        """Benchmark detection performance on synthetic frames"""
        print(f"🔄 Benchmarking detection on {num_frames} frames...")
        
        # Create synthetic test frame
        test_frame = np.random.randint(0, 255, (720, 1280, 3), dtype=np.uint8)
        
        detection_times = []
        hand_detection_times = []
        memory_usage = []
        
        for i in range(num_frames):
            # Memory usage
            memory_usage.append(psutil.Process().memory_info().rss / 1024 / 1024)  # MB
            
            # YOLO detection
            start_time = time.time()
            processed, human_detected, detections = detector.detect(test_frame)
            detection_time = time.time() - start_time
            detection_times.append(detection_time * 1000)  # Convert to ms
            
            # Hand detection
            start_time = time.time()
            processed, hands = hand_detector.detect_hands(processed, draw=False)
            hand_time = time.time() - start_time
            hand_detection_times.append(hand_time * 1000)  # Convert to ms
            
            if i % 20 == 0:
                print(f"  Progress: {i+1}/{num_frames} frames")
        
        # Calculate statistics
        avg_detection_time = np.mean(detection_times)
        avg_hand_time = np.mean(hand_detection_times)
        total_avg_time = avg_detection_time + avg_hand_time
        theoretical_fps = 1000 / total_avg_time if total_avg_time > 0 else 0
        avg_memory = np.mean(memory_usage)
        
        self.results["benchmarks"]["detection_performance"] = {
            "frames_tested": num_frames,
            "avg_yolo_detection_ms": round(avg_detection_time, 2),
            "avg_hand_detection_ms": round(avg_hand_time, 2),
            "avg_total_processing_ms": round(total_avg_time, 2),
            "theoretical_max_fps": round(theoretical_fps, 1),
            "avg_memory_usage_mb": round(avg_memory, 1),
            "peak_memory_usage_mb": round(max(memory_usage), 1)
        }
        
        print(f"✅ Detection performance: {total_avg_time:.1f}ms avg, {theoretical_fps:.1f} FPS theoretical max")
    
    def benchmark_camera_performance(self):
        """Benchmark actual camera performance if available"""
        print("🔄 Testing camera performance...")
        
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("⚠️  No camera available for live testing")
                return
            
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            cap.set(cv2.CAP_PROP_FPS, 30)
            
            frame_times = []
            successful_reads = 0
            
            for i in range(30):  # Test 30 frames
                start_time = time.time()
                ret, frame = cap.read()
                frame_time = time.time() - start_time
                
                if ret:
                    successful_reads += 1
                    frame_times.append(frame_time * 1000)
            
            cap.release()
            
            if frame_times:
                avg_frame_time = np.mean(frame_times)
                actual_fps = 1000 / avg_frame_time if avg_frame_time > 0 else 0
                
                self.results["benchmarks"]["camera_performance"] = {
                    "successful_reads": successful_reads,
                    "total_attempts": 30,
                    "avg_frame_read_ms": round(avg_frame_time, 2),
                    "actual_camera_fps": round(actual_fps, 1),
                    "camera_available": True
                }
                
                print(f"✅ Camera performance: {actual_fps:.1f} FPS actual")
            else:
                self.results["benchmarks"]["camera_performance"] = {
                    "camera_available": False,
                    "error": "No successful frame reads"
                }
                
        except Exception as e:
            self.results["benchmarks"]["camera_performance"] = {
                "camera_available": False,
                "error": str(e)
            }
            print(f"⚠️  Camera test failed: {e}")
    
    def run_full_benchmark(self):
        """Run complete benchmark suite"""
        print("🚀 Starting ManTion Performance Benchmark")
        print("=" * 50)
        
        # Model loading benchmark
        detector, hand_detector = self.benchmark_model_loading()
        
        # Detection performance benchmark
        self.benchmark_detection_performance(detector, hand_detector)
        
        # Camera performance benchmark
        self.benchmark_camera_performance()
        
        # System resource summary
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        self.results["system_resources"] = {
            "cpu_usage_percent": cpu_percent,
            "memory_usage_percent": memory_percent,
            "benchmark_duration_s": time.time() - self.start_time
        }
        
        print("\n" + "=" * 50)
        print("📊 Benchmark Complete!")
        self._print_summary()
        
        return self.results
    
    def _print_summary(self):
        """Print benchmark summary"""
        b = self.results["benchmarks"]
        
        print(f"\n🏆 Performance Summary:")
        print(f"  Model Loading: {b['model_loading']['total_load_time_ms']}ms")
        
        if "detection_performance" in b:
            dp = b["detection_performance"]
            print(f"  Detection Speed: {dp['avg_total_processing_ms']}ms avg")
            print(f"  Theoretical FPS: {dp['theoretical_max_fps']}")
            print(f"  Memory Usage: {dp['avg_memory_usage_mb']}MB avg")
        
        if "camera_performance" in b and b["camera_performance"].get("camera_available"):
            cp = b["camera_performance"]
            print(f"  Camera FPS: {cp['actual_camera_fps']}")
    
    def save_results(self, filename="benchmark_results.json"):
        """Save benchmark results to file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"📁 Results saved to {filename}")

def main():
    benchmark = ManTionBenchmark()
    benchmark.start_time = time.time()
    
    try:
        results = benchmark.run_full_benchmark()
        benchmark.save_results()
        
        # Generate markdown summary for README
        generate_readme_snippet(results)
        
    except KeyboardInterrupt:
        print("\n⏹️  Benchmark interrupted by user")
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()

def generate_readme_snippet(results):
    """Generate markdown snippet for README"""
    b = results["benchmarks"]
    sys_info = results["system_info"]
    
    snippet = f"""
## 📊 **Real Performance Benchmarks**

*Benchmarked on {datetime.now().strftime('%Y-%m-%d')}*

| **Metric** | **Performance** | **Hardware** |
|------------|-----------------|--------------|
| **Model Loading** | {b['model_loading']['total_load_time_ms']}ms | {sys_info['cpu']['cores']} cores, {sys_info['memory']['total_gb']}GB RAM |
"""
    
    if "detection_performance" in b:
        dp = b["detection_performance"]
        snippet += f"| **Detection Speed** | {dp['avg_total_processing_ms']}ms avg | {dp['theoretical_max_fps']} FPS theoretical |\n"
        snippet += f"| **Memory Usage** | {dp['avg_memory_usage_mb']}MB avg | Peak: {dp['peak_memory_usage_mb']}MB |\n"
    
    if "camera_performance" in b and b["camera_performance"].get("camera_available"):
        cp = b["camera_performance"]
        snippet += f"| **Camera Performance** | {cp['actual_camera_fps']} FPS | 1280x720 resolution |\n"
    
    with open("benchmark_snippet.md", "w") as f:
        f.write(snippet)
    
    print(f"📝 README snippet saved to benchmark_snippet.md")

if __name__ == "__main__":
    main()
