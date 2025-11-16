import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
import time

class MouthStateDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Mouth landmark indices
        # Upper lip: 13
        # Lower lip: 14
        # Left corner: 61
        # Right corner: 291
        # More detailed landmarks for MAR calculation
        self.MOUTH_INDICES = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88]
        
        # Key points for MAR (Mouth Aspect Ratio)
        self.MOUTH_TOP = 13
        self.MOUTH_BOTTOM = 14
        self.MOUTH_LEFT = 61
        self.MOUTH_RIGHT = 291
        
        # Inner mouth points for better detection
        self.INNER_MOUTH_VERTICAL = [(13, 14), (312, 311)]  # Top-bottom pairs
        self.INNER_MOUTH_HORIZONTAL = (61, 291)  # Left-right
        
        # Thresholds
        self.MAR_YAWN_THRESHOLD = 0.4  # Mouth Aspect Ratio for yawn
        self.MAR_OPEN_THRESHOLD = 0.1  # Just open mouth
        self.YAWN_DURATION_THRESHOLD = 2  # Seconds
        
        # State tracking
        self.mouth_state = "CLOSED"
        self.yawn_start_time = None
        self.yawn_duration = 0
        
    def calculate_mar(self, mouth_points):
        """
        Calculate Mouth Aspect Ratio (MAR)
        Similar to EAR but for mouth
        """
        # Vertical distances (multiple pairs)
        vertical_distances = []
        for top, bottom in self.INNER_MOUTH_VERTICAL:
            dist_val = dist.euclidean(mouth_points[top], mouth_points[bottom])
            vertical_distances.append(dist_val)
        
        avg_vertical = np.mean(vertical_distances)
        
        # Horizontal distance
        horizontal = dist.euclidean(
            mouth_points[self.MOUTH_LEFT],
            mouth_points[self.MOUTH_RIGHT]
        )
        
        # MAR formula
        mar = avg_vertical / horizontal if horizontal > 0 else 0
        return mar
    
    def detect(self, frame):
        """
        Detect mouth state
        Returns: dict with mouth state information
        """
        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        mouth_data = {
            'state': 'NO_FACE',
            'mar': 0.0,
            'is_yawning': False,
            'yawn_duration': 0.0,
            'frame': frame.copy()
        }
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark
                
                # Extract mouth points as dictionary for easy access
                mouth_points = {}
                for idx in [self.MOUTH_TOP, self.MOUTH_BOTTOM, 
                           self.MOUTH_LEFT, self.MOUTH_RIGHT, 312, 311]:
                    x = int(landmarks[idx].x * width)
                    y = int(landmarks[idx].y * height)
                    mouth_points[idx] = (x, y)
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
                
                # Draw all mouth landmarks
                for idx in self.MOUTH_INDICES:
                    x = int(landmarks[idx].x * width)
                    y = int(landmarks[idx].y * height)
                    cv2.circle(frame, (x, y), 1, (255, 0, 255), -1)
                
                # Calculate MAR
                mar = self.calculate_mar(mouth_points)
                mouth_data['mar'] = mar
                
                # Determine state
                if mar > self.MAR_YAWN_THRESHOLD:
                    if self.yawn_start_time is None:
                        self.yawn_start_time = time.time()
                    
                    current_yawn_duration = time.time() - self.yawn_start_time
                    
                    if current_yawn_duration >= self.YAWN_DURATION_THRESHOLD:
                        self.mouth_state = "YAWNING"
                        mouth_data['is_yawning'] = True
                    else:
                        self.mouth_state = "WIDE_OPEN"
                    
                    mouth_data['yawn_duration'] = current_yawn_duration
                    
                elif mar > self.MAR_OPEN_THRESHOLD:
                    self.mouth_state = "OPEN"
                    self.yawn_start_time = None
                    mouth_data['yawn_duration'] = 0
                else:
                    self.mouth_state = "CLOSED"
                    self.yawn_start_time = None
                    mouth_data['yawn_duration'] = 0
                
                mouth_data['state'] = self.mouth_state
                
                # Draw mouth bounding box
                top_point = mouth_points[self.MOUTH_TOP]
                bottom_point = mouth_points[self.MOUTH_BOTTOM]
                left_point = mouth_points[self.MOUTH_LEFT]
                right_point = mouth_points[self.MOUTH_RIGHT]
                
                # Draw lines showing mouth opening
                cv2.line(frame, top_point, bottom_point, (255, 255, 0), 2)
                cv2.line(frame, left_point, right_point, (255, 255, 0), 2)
                
                # Visualization
                if self.mouth_state == "YAWNING":
                    color = (0, 0, 255)
                    cv2.rectangle(frame, (5, 5), (width-5, height-5), color, 6)
                    cv2.putText(frame, "YAWN DETECTED!", (10, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                elif self.mouth_state == "WIDE_OPEN":
                    color = (0, 165, 255)
                elif self.mouth_state == "OPEN":
                    color = (0, 255, 255)
                else:
                    color = (0, 255, 0)
                
                cv2.putText(frame, f"Mouth: {self.mouth_state}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                cv2.putText(frame, f"MAR: {mar:.3f}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                if mouth_data['yawn_duration'] > 0:
                    cv2.putText(frame, f"Duration: {mouth_data['yawn_duration']:.1f}s", (10, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
        
        mouth_data['frame'] = frame
        return mouth_data

# Main test
if __name__ == "__main__":
    detector = MouthStateDetector()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("=== MODULE 4: Mouth State Detection ===")
    print("States: CLOSED, OPEN, WIDE_OPEN, YAWNING")
    print("Yawn triggers after 1.5s of wide open mouth")
    print("Press 'q' to quit")
    print("=" * 40)
    print("\nTips:")
    print("- Open mouth slightly: OPEN")
    print("- Open mouth wide: WIDE_OPEN")
    print("- Keep wide open >1.5s: YAWNING")
    print("=" * 40)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        result = detector.detect(frame)
        
        # Print state changes
        if result['is_yawning']:
            print(f"🥱 YAWN DETECTED! Duration: {result['yawn_duration']:.2f}s | MAR: {result['mar']:.3f}")
        
        cv2.imshow('Module 4: Mouth State Detection', result['frame'])
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n=== Module 4 Test Complete ===")