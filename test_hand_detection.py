import cv2
import numpy as np
from detector import Detector
from utils import draw_detections
from config import CAMERA_INDEX

def test_hand_detection():
    """Test the enhanced detection system with hand detection"""
    print("Testing ManTion with Hand Detection")
    print("Press 'q' to quit, 'h' to show/hide hand detection info")
    
    cap = cv2.VideoCapture(CAMERA_INDEX)
    detector = Detector()
    show_info = True
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read from camera")
                break
                
            # Detect humans and hands
            detections = detector.detect(frame)
            
            if detections:
                # Draw all detections (body + hands)
                frame = draw_detections(frame, detections)
                
                if show_info:
                    # Show detection info
                    for i, det in enumerate(detections):
                        hand_count = len(det.get('hand_regions', []))
                        info_text = f"Person {i+1}: {hand_count} hands detected"
                        cv2.putText(frame, info_text, (10, 100 + i*30),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.putText(frame, "HUMAN + HANDS DETECTED!", (50, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            else:
                cv2.putText(frame, "SAFE - NO DETECTION", (50, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
            
            # Show instructions
            cv2.putText(frame, "Press 'q' to quit, 'h' for info", (10, frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow('ManTion - Enhanced Detection', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('h'):
                show_info = not show_info
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Test completed!")

if __name__ == "__main__":
    test_hand_detection()
