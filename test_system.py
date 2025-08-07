#!/usr/bin/env python3
"""
Test script for ManTion Safety System
Tests all components: detector, alarm, and web dashboard
"""

import cv2
import time
from detector import Detector
from alarm import Alarm
from utils import setup_logging
import logging

def test_detector():
    """Test the YOLOv8-Pose detector"""
    print("🔍 Testing YOLOv8-Pose Detector...")
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize detector
        detector = Detector()
        print("✅ Detector initialized successfully")
        
        # Test with camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Cannot open camera")
            return False
            
        print("📹 Camera opened successfully")
        
        # Test detection for 5 seconds
        start_time = time.time()
        detection_count = 0
        
        while time.time() - start_time < 5:
            ret, frame = cap.read()
            if not ret:
                continue
                
            # Perform detection
            processed_frame, human_detected, detections_info = detector.detect(frame)
            
            if human_detected:
                detection_count += 1
                print(f"🎯 Human detected! Confidence: {detections_info[0]['conf']:.2f}")
            
            # Display frame
            cv2.imshow('ManTion Test - Press Q to exit', processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"✅ Detector test completed. Detections: {detection_count}")
        return True
        
    except Exception as e:
        print(f"❌ Detector test failed: {e}")
        logger.error(f"Detector test failed: {e}")
        return False

def test_alarm():
    """Test the alarm system"""
    print("\n🔊 Testing Alarm System...")
    
    try:
        alarm = Alarm()
        print("✅ Alarm initialized successfully")
        
        # Test alarm trigger
        print("🔊 Triggering alarm...")
        alarm.trigger()
        time.sleep(2)  # Let alarm play for 2 seconds
        
        # Test alarm stop
        print("🔇 Stopping alarm...")
        alarm.stop()
        
        print("✅ Alarm test completed")
        return True
        
    except Exception as e:
        print(f"❌ Alarm test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 ManTion Safety System - Component Tests")
    print("=" * 50)
    
    # Test detector
    detector_ok = test_detector()
    
    # Test alarm
    alarm_ok = test_alarm()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Detector: {'✅ PASS' if detector_ok else '❌ FAIL'}")
    print(f"Alarm: {'✅ PASS' if alarm_ok else '❌ FAIL'}")
    
    if detector_ok and alarm_ok:
        print("\n🎉 All tests passed! System is ready.")
        print("\n🌐 To start the web dashboard:")
        print("   python web_dashboard.py")
        print("   Then open: http://localhost:5000")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 