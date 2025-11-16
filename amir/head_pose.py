import cv2
import mediapipe as mp
import numpy as np

class HeadPoseDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Thresholds (degrees)
        self.YAW_THRESHOLD = 30    # Left/Right
        self.PITCH_THRESHOLD = 20  # Up/Down
        
        # Head pose state
        self.head_state = "FORWARD"  # FORWARD, LEFT, RIGHT, DOWN, UP
        
    def calculate_head_pose(self, landmarks, width, height):
        """
        Calculate head pose angles (yaw, pitch, roll)
        """
        # Key facial landmarks for pose estimation
        # Nose tip
        nose = np.array([landmarks[1].x * width, landmarks[1].y * height])
        
        # Chin
        chin = np.array([landmarks[152].x * width, landmarks[152].y * height])
        
        # Left eye corner
        left_eye = np.array([landmarks[33].x * width, landmarks[33].y * height])
        
        # Right eye corner  
        right_eye = np.array([landmarks[263].x * width, landmarks[263].y * height])
        
        # Left mouth corner
        left_mouth = np.array([landmarks[61].x * width, landmarks[61].y * height])
        
        # Right mouth corner
        right_mouth = np.array([landmarks[291].x * width, landmarks[291].y * height])
        
        # Calculate center of eyes
        eye_center = (left_eye + right_eye) / 2
        
        # Calculate yaw (left-right rotation)
        # Based on eye width asymmetry
        left_eye_to_nose = np.linalg.norm(left_eye - nose)
        right_eye_to_nose = np.linalg.norm(right_eye - nose)
        eye_asymmetry = (right_eye_to_nose - left_eye_to_nose) / ((right_eye_to_nose + left_eye_to_nose) / 2)
        yaw = eye_asymmetry * 50  # Scale to approximate degrees
        
        # Calculate pitch (up-down rotation)
        # Based on nose-to-chin distance vs eye-to-nose distance
        nose_to_chin = np.linalg.norm(nose - chin)
        eye_to_nose = np.linalg.norm(eye_center - nose)
        pitch_ratio = eye_to_nose / nose_to_chin
        pitch = (pitch_ratio - 0.4) * 100  # Scale to approximate degrees
        
        return yaw, pitch
    
    def detect(self, frame):
        """
        Detect head pose
        Returns: dict with head pose information
        """
        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        pose_data = {
            'state': 'NO_FACE',
            'yaw': 0.0,
            'pitch': 0.0,
            'is_distracted': False,
            'frame': frame.copy()
        }
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark
                
                # Calculate head pose
                yaw, pitch = self.calculate_head_pose(landmarks, width, height)
                
                # Determine state
                if abs(yaw) > self.YAW_THRESHOLD:
                    self.head_state = "LEFT" if yaw < 0 else "RIGHT"
                    pose_data['is_distracted'] = True
                elif pitch < -self.PITCH_THRESHOLD:
                    self.head_state = "DOWN"
                    pose_data['is_distracted'] = True
                elif pitch > self.PITCH_THRESHOLD:
                    self.head_state = "UP"
                else:
                    self.head_state = "FORWARD"
                    pose_data['is_distracted'] = False
                
                pose_data['state'] = self.head_state
                pose_data['yaw'] = yaw
                pose_data['pitch'] = pitch
                
                # Draw key landmarks
                # Nose
                nose_x = int(landmarks[1].x * width)
                nose_y = int(landmarks[1].y * height)
                cv2.circle(frame, (nose_x, nose_y), 5, (0, 255, 255), -1)
                
                # Eyes
                left_eye_x = int(landmarks[33].x * width)
                left_eye_y = int(landmarks[33].y * height)
                right_eye_x = int(landmarks[263].x * width)
                right_eye_y = int(landmarks[263].y * height)
                cv2.circle(frame, (left_eye_x, left_eye_y), 3, (255, 0, 0), -1)
                cv2.circle(frame, (right_eye_x, right_eye_y), 3, (255, 0, 0), -1)
                
                # Draw pose axes
                # Calculate direction vector for yaw
                axis_length = 100
                yaw_rad = np.radians(yaw)
                end_x = int(nose_x + axis_length * np.sin(yaw_rad))
                end_y = int(nose_y)
                cv2.arrowedLine(frame, (nose_x, nose_y), (end_x, end_y), (0, 255, 0), 2, tipLength=0.3)
                
                # Visualization
                color = (0, 255, 0) if self.head_state == "FORWARD" else (0, 0, 255)
                cv2.putText(frame, f"Head: {self.head_state}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                cv2.putText(frame, f"Yaw: {yaw:.1f}°", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.putText(frame, f"Pitch: {pitch:.1f}°", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                if pose_data['is_distracted']:
                    cv2.rectangle(frame, (5, 5), (width-5, height-5), (0, 165, 255), 5)
                    cv2.putText(frame, "DISTRACTED!", (10, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
        
        pose_data['frame'] = frame
        return pose_data

# Main test
if __name__ == "__main__":
    detector = HeadPoseDetector()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("=== MODULE 2: Head Pose Detection ===")
    print("States: FORWARD, LEFT, RIGHT, DOWN, UP")
    print("Distraction triggers when head turns >20°")
    print("Press 'q' to quit")
    print("=" * 40)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        result = detector.detect(frame)
        
        # Print state changes
        if result['is_distracted']:
            print(f"⚠️ DISTRACTED! Looking {result['state']} (Yaw: {result['yaw']:.1f}°)")
        
        cv2.imshow('Module 2: Head Pose Detection', result['frame'])
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n=== Module 2 Test Complete ===")