import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
import time

# Eye Aspect Ratio (EAR) calculation
def calculate_ear(eye_points):
    """Calculate Eye Aspect Ratio"""
    A = dist.euclidean(eye_points[1], eye_points[5])
    B = dist.euclidean(eye_points[2], eye_points[4])
    C = dist.euclidean(eye_points[0], eye_points[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Mediapipe Face Mesh indices for eyes
LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]

class EyeStateDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Thresholds
        self.EAR_THRESHOLD = 0.21
        self.CLOSED_FRAMES_THRESHOLD = 45  # ~1.5 seconds at 30fps
        
        # State tracking
        self.closed_frames = 0
        self.eyes_state = "OPEN"  # OPEN, CLOSED, MICROSLEEP
        self.eyes_closed_start = None
        self.eyes_closed_duration = 0
        
    def detect(self, frame):
        """
        Detect eye state
        Returns: dict with eye state information
        """
        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        eye_data = {
            'state': 'NO_FACE',
            'ear': 0.0,
            'closed_duration': 0.0,
            'is_microsleep': False,
            'frame': frame.copy()
        }
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark
                
                # Extract eye coordinates
                left_eye = []
                for idx in LEFT_EYE_INDICES:
                    x = int(landmarks[idx].x * width)
                    y = int(landmarks[idx].y * height)
                    left_eye.append((x, y))
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
                
                right_eye = []
                for idx in RIGHT_EYE_INDICES:
                    x = int(landmarks[idx].x * width)
                    y = int(landmarks[idx].y * height)
                    right_eye.append((x, y))
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
                
                # Calculate EAR
                left_ear = calculate_ear(left_eye)
                right_ear = calculate_ear(right_eye)
                avg_ear = (left_ear + right_ear) / 2.0
                
                # Determine state
                if avg_ear < self.EAR_THRESHOLD:
                    if self.eyes_closed_start is None:
                        self.eyes_closed_start = time.time()
                    
                    self.closed_frames += 1
                    current_duration = time.time() - self.eyes_closed_start
                    
                    if self.closed_frames >= self.CLOSED_FRAMES_THRESHOLD:
                        self.eyes_state = "MICROSLEEP"
                        eye_data['is_microsleep'] = True
                    else:
                        self.eyes_state = "CLOSED"
                    
                    eye_data['closed_duration'] = current_duration
                else:
                    self.eyes_state = "OPEN"
                    self.closed_frames = 0
                    self.eyes_closed_start = None
                    eye_data['closed_duration'] = 0
                
                eye_data['state'] = self.eyes_state
                eye_data['ear'] = avg_ear
                
                # Draw visualization
                color = (0, 255, 0) if self.eyes_state == "OPEN" else (0, 0, 255)
                cv2.putText(frame, f"Eyes: {self.eyes_state}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                cv2.putText(frame, f"EAR: {avg_ear:.3f}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                if eye_data['closed_duration'] > 0:
                    cv2.putText(frame, f"Closed: {eye_data['closed_duration']:.1f}s", (10, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
                
                if eye_data['is_microsleep']:
                    cv2.rectangle(frame, (5, 5), (width-5, height-5), (0, 0, 255), 8)
                    cv2.putText(frame, "MICROSLEEP ALERT!", (10, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        eye_data['frame'] = frame
        return eye_data

# Main test
if __name__ == "__main__":
    detector = EyeStateDetector()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("=== MODULE 1: Eye State Detection ===")
    print("States: OPEN, CLOSED, MICROSLEEP")
    print("Microsleep triggers after 1.5s eyes closed")
    print("Press 'q' to quit")
    print("=" * 40)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        result = detector.detect(frame)
        
        # Print state changes
        if result['is_microsleep']:
            print(f"⚠️ MICROSLEEP! Duration: {result['closed_duration']:.2f}s")
        
        cv2.imshow('Module 1: Eye State Detection', result['frame'])
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n=== Module 1 Test Complete ===")