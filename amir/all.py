import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
import time
import json
import csv
from datetime import datetime
import os

# ============================================
# LOGGER CLASS FOR STORING DETECTION DATA
# ============================================
class DriverLogger:
    def __init__(self, session_name=None):
        # Create logs directory
        self.log_dir = "driver_logs"
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Session info
        if session_name is None:
            self.session_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        else:
            self.session_name = session_name
        
        # File paths
        self.csv_file = os.path.join(self.log_dir, f"session_{self.session_name}.csv")
        self.json_file = os.path.join(self.log_dir, f"session_{self.session_name}.json")
        self.summary_file = os.path.join(self.log_dir, f"summary_{self.session_name}.txt")
        
        # Session data
        self.session_start = datetime.now()
        self.logs = []
        self.statistics = {
            'total_frames': 0,
            'microsleep_count': 0,
            'microsleep_duration': 0.0,
            'distraction_count': 0,
            'distraction_duration': 0.0,
            'phone_usage_count': 0,
            'phone_usage_duration': 0.0,
            'yawn_count': 0,
            'yawn_duration': 0.0,
            'critical_alerts': 0,
            'danger_alerts': 0,
            'warning_alerts': 0
        }
        
        # State tracking
        self.last_states = {
            'microsleep': False,
            'distracted': False,
            'phone_usage': False,
            'yawning': False
        }
        self.state_start_times = {}
        
        # Initialize CSV
        self._init_csv()
        
        print(f"📊 Logging session: {self.session_name}")
        print(f"📁 Log directory: {self.log_dir}")
    
    def _init_csv(self):
        """Initialize CSV file with headers"""
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp', 'frame_number', 'risk_level', 'eye_state', 'ear_value',
                'head_state', 'yaw_angle', 'pitch_angle', 'phone_state', 'phone_confidence',
                'mouth_state', 'mar_value', 'alerts'
            ])
    
    def log_frame(self, frame_number, analysis, eye_data, head_data, phone_data, mouth_data):
        """Log a single frame's detection data"""
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            'timestamp': timestamp,
            'frame_number': frame_number,
            'risk_level': analysis['risk_level'],
            'eye_state': eye_data['state'],
            'ear_value': round(eye_data['ear'], 3),
            'head_state': head_data['state'],
            'yaw_angle': round(head_data['yaw'], 2),
            'pitch_angle': round(head_data['pitch'], 2),
            'phone_state': phone_data['state'],
            'phone_confidence': round(phone_data['confidence'], 2),
            'mouth_state': mouth_data['state'],
            'mar_value': round(mouth_data['mar'], 3),
            'alerts': analysis['alerts']
        }
        
        self.logs.append(log_entry)
        
        # Write to CSV
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, frame_number, analysis['risk_level'], eye_data['state'], eye_data['ear'],
                head_data['state'], head_data['yaw'], head_data['pitch'], phone_data['state'],
                phone_data['confidence'], mouth_data['state'], mouth_data['mar'],
                '; '.join(analysis['alerts'])
            ])
        
        self._update_statistics(analysis, eye_data, head_data, phone_data, mouth_data)
        self.statistics['total_frames'] += 1
    
    def _update_statistics(self, analysis, eye_data, head_data, phone_data, mouth_data):
        """Update running statistics"""
        current_time = time.time()
        
        if analysis['risk_level'] == 'CRITICAL':
            self.statistics['critical_alerts'] += 1
        elif analysis['risk_level'] == 'DANGER':
            self.statistics['danger_alerts'] += 1
        elif analysis['risk_level'] == 'WARNING':
            self.statistics['warning_alerts'] += 1
        
        # Track microsleep
        if eye_data['is_microsleep']:
            if not self.last_states['microsleep']:
                self.statistics['microsleep_count'] += 1
                self.state_start_times['microsleep'] = current_time
            self.last_states['microsleep'] = True
        else:
            if self.last_states['microsleep']:
                duration = current_time - self.state_start_times['microsleep']
                self.statistics['microsleep_duration'] += duration
            self.last_states['microsleep'] = False
        
        # Track distraction
        if head_data['is_distracted']:
            if not self.last_states['distracted']:
                self.statistics['distraction_count'] += 1
                self.state_start_times['distracted'] = current_time
            self.last_states['distracted'] = True
        else:
            if self.last_states['distracted']:
                duration = current_time - self.state_start_times['distracted']
                self.statistics['distraction_duration'] += duration
            self.last_states['distracted'] = False
        
        # Track phone usage
        if phone_data['state'] == 'PHONE_USAGE':
            if not self.last_states['phone_usage']:
                self.statistics['phone_usage_count'] += 1
                self.state_start_times['phone_usage'] = current_time
            self.last_states['phone_usage'] = True
        else:
            if self.last_states['phone_usage']:
                duration = current_time - self.state_start_times['phone_usage']
                self.statistics['phone_usage_duration'] += duration
            self.last_states['phone_usage'] = False
        
        # Track yawning
        if mouth_data['is_yawning']:
            if not self.last_states['yawning']:
                self.statistics['yawn_count'] += 1
                self.state_start_times['yawning'] = current_time
            self.last_states['yawning'] = True
        else:
            if self.last_states['yawning']:
                duration = current_time - self.state_start_times['yawning']
                self.statistics['yawn_duration'] += duration
            self.last_states['yawning'] = False
    
    def save_session(self):
        """Save complete session data"""
        session_duration = (datetime.now() - self.session_start).total_seconds()
        
        session_data = {
            'session_name': self.session_name,
            'start_time': self.session_start.isoformat(),
            'end_time': datetime.now().isoformat(),
            'duration_seconds': round(session_duration, 2),
            'statistics': self.statistics,
            'logs': self.logs[-100:]
        }
        
        with open(self.json_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        self._save_summary(session_duration)
        
        print(f"\n✅ Session saved:")
        print(f"   📄 CSV: {self.csv_file}")
        print(f"   📄 JSON: {self.json_file}")
        print(f"   📄 Summary: {self.summary_file}")
    
    def _save_summary(self, session_duration):
        """Save human-readable summary"""
        with open(self.summary_file, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("DRIVER MONITORING SESSION SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Session: {self.session_name}\n")
            f.write(f"Start: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Duration: {session_duration:.1f} seconds ({session_duration/60:.1f} minutes)\n")
            f.write(f"Total Frames: {self.statistics['total_frames']}\n\n")
            
            f.write("ALERTS SUMMARY\n")
            f.write("-" * 70 + "\n")
            f.write(f"Critical Alerts: {self.statistics['critical_alerts']}\n")
            f.write(f"Danger Alerts: {self.statistics['danger_alerts']}\n")
            f.write(f"Warning Alerts: {self.statistics['warning_alerts']}\n\n")
            
            f.write("SAFETY INCIDENTS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Microsleep Events: {self.statistics['microsleep_count']} "
                   f"(Total: {self.statistics['microsleep_duration']:.1f}s)\n")
            f.write(f"Distraction Events: {self.statistics['distraction_count']} "
                   f"(Total: {self.statistics['distraction_duration']:.1f}s)\n")
            f.write(f"Phone Usage Events: {self.statistics['phone_usage_count']} "
                   f"(Total: {self.statistics['phone_usage_duration']:.1f}s)\n")
            f.write(f"Yawn Events: {self.statistics['yawn_count']} "
                   f"(Total: {self.statistics['yawn_duration']:.1f}s)\n\n")
            
            safety_score = self._calculate_safety_score(session_duration)
            f.write("SAFETY SCORE\n")
            f.write("-" * 70 + "\n")
            f.write(f"Overall Safety: {safety_score}/100\n")
            f.write(f"Rating: {self._get_safety_rating(safety_score)}\n\n")
            f.write("=" * 70 + "\n")
    
    def _calculate_safety_score(self, duration):
        """Calculate safety score (0-100)"""
        if duration == 0:
            return 100
        
        score = 100
        score -= self.statistics['microsleep_count'] * 10
        score -= self.statistics['distraction_count'] * 3
        score -= self.statistics['phone_usage_count'] * 5
        score -= self.statistics['yawn_count'] * 2
        score -= (self.statistics['microsleep_duration'] / duration) * 20
        score -= (self.statistics['distraction_duration'] / duration) * 10
        score -= (self.statistics['phone_usage_duration'] / duration) * 15
        
        return max(0, min(100, score))
    
    def _get_safety_rating(self, score):
        """Get text rating from score"""
        if score >= 90:
            return "EXCELLENT ⭐⭐⭐⭐⭐"
        elif score >= 75:
            return "GOOD ⭐⭐⭐⭐"
        elif score >= 60:
            return "FAIR ⭐⭐⭐"
        elif score >= 40:
            return "POOR ⭐⭐"
        else:
            return "DANGEROUS ⭐"
    
    def print_stats(self):
        """Print current statistics"""
        print("\n" + "=" * 50)
        print("CURRENT SESSION STATISTICS")
        print("=" * 50)
        print(f"Frames Processed: {self.statistics['total_frames']}")
        print(f"Microsleep Events: {self.statistics['microsleep_count']}")
        print(f"Distraction Events: {self.statistics['distraction_count']}")
        print(f"Phone Usage Events: {self.statistics['phone_usage_count']}")
        print(f"Yawn Events: {self.statistics['yawn_count']}")
        print("=" * 50 + "\n")

# ============================================
# MODULE 1: EYE STATE DETECTOR
# ============================================
class EyeStateDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.EAR_THRESHOLD = 0.21
        self.CLOSED_FRAMES_THRESHOLD = 45
        self.LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
        self.closed_frames = 0
        self.eyes_state = "OPEN"
        self.eyes_closed_start = None
        
    def calculate_ear(self, eye_points):
        A = dist.euclidean(eye_points[1], eye_points[5])
        B = dist.euclidean(eye_points[2], eye_points[4])
        C = dist.euclidean(eye_points[0], eye_points[3])
        return (A + B) / (2.0 * C)
        
    def detect(self, frame):
        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        eye_data = {'state': 'NO_FACE', 'ear': 0.0, 'closed_duration': 0.0, 'is_microsleep': False}
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            left_eye = [(int(landmarks[i].x * width), int(landmarks[i].y * height)) for i in self.LEFT_EYE_INDICES]
            right_eye = [(int(landmarks[i].x * width), int(landmarks[i].y * height)) for i in self.RIGHT_EYE_INDICES]
            
            avg_ear = (self.calculate_ear(left_eye) + self.calculate_ear(right_eye)) / 2.0
            
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
            
            eye_data['state'] = self.eyes_state
            eye_data['ear'] = avg_ear
        
        return eye_data

# ============================================
# MODULE 2: HEAD POSE DETECTOR (FIXED DIRECTIONS!)
# ============================================
class HeadPoseDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.YAW_THRESHOLD = 30
        self.PITCH_THRESHOLD = 20
        self.head_state = "FORWARD"
        
    def calculate_head_pose(self, landmarks, width, height):
        nose = np.array([landmarks[1].x * width, landmarks[1].y * height])
        chin = np.array([landmarks[152].x * width, landmarks[152].y * height])
        left_eye = np.array([landmarks[33].x * width, landmarks[33].y * height])
        right_eye = np.array([landmarks[263].x * width, landmarks[263].y * height])
        eye_center = (left_eye + right_eye) / 2
        
        left_eye_to_nose = np.linalg.norm(left_eye - nose)
        right_eye_to_nose = np.linalg.norm(right_eye - nose)
        eye_asymmetry = (right_eye_to_nose - left_eye_to_nose) / ((right_eye_to_nose + left_eye_to_nose) / 2)
        yaw = eye_asymmetry * 50
        
        nose_to_chin = np.linalg.norm(nose - chin)
        eye_to_nose = np.linalg.norm(eye_center - nose)
        pitch_ratio = eye_to_nose / nose_to_chin
        pitch = (pitch_ratio - 0.4) * 100
        
        return yaw, pitch
    
    def detect(self, frame):
        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        pose_data = {'state': 'NO_FACE', 'yaw': 0.0, 'pitch': 0.0, 'is_distracted': False}
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            yaw, pitch = self.calculate_head_pose(landmarks, width, height)
            
            # FIXED DIRECTIONS!
            if abs(yaw) > self.YAW_THRESHOLD:
                self.head_state = "RIGHT" if yaw < 0 else "LEFT"
                pose_data['is_distracted'] = True
            elif pitch < -self.PITCH_THRESHOLD:
                self.head_state = "UP"
                pose_data['is_distracted'] = True
            elif pitch > self.PITCH_THRESHOLD:
                self.head_state = "DOWN"
                pose_data['is_distracted'] = True
            else:
                self.head_state = "FORWARD"
                pose_data['is_distracted'] = False
            
            pose_data['state'] = self.head_state
            pose_data['yaw'] = yaw
            pose_data['pitch'] = pitch
        
        return pose_data

# ============================================
# MODULE 3: PHONE DETECTOR
# ============================================
class PhoneDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        
        try:
            from ultralytics import YOLO
            self.yolo_model = YOLO('yolov8n.pt')
            self.yolo_loaded = True
            print("✓ YOLO loaded for phone object detection")
        except:
            self.yolo_loaded = False
            print("○ Phone detection using hand tracking only")
        
        self.HAND_FACE_DISTANCE = 0.3
        self.HAND_UP_THRESHOLD = 0.6
        self.PHONE_CONFIDENCE = 0.28
        self.detection_history = []
        self.HISTORY_SIZE = 10
        self.CONFIRMATION_THRESHOLD = 0.6
        
    def detect(self, frame):
        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        phone_data = {'state': 'NO_PHONE', 'phone_object_detected': False, 'hand_detected': False, 'hand_near_face': False, 'confidence': 0.0}
        
        phone_bbox = None
        if self.yolo_loaded:
            try:
                results = self.yolo_model(frame, verbose=False, conf=self.PHONE_CONFIDENCE)
                for result in results:
                    for box in result.boxes:
                        class_id = int(box.cls[0])
                        class_name = result.names[class_id]
                        if 'phone' in class_name.lower() or class_id == 67:
                            phone_data['phone_object_detected'] = True
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            phone_bbox = (int(x1), int(y1), int(x2), int(y2))
                            break
            except:
                pass
        
        hands_results = self.hands.process(rgb_frame)
        face_results = self.face_mesh.process(rgb_frame)
        
        face_center = None
        if face_results.multi_face_landmarks:
            landmarks = face_results.multi_face_landmarks[0].landmark
            face_center = np.array([landmarks[1].x, landmarks[1].y])
        
        hand_up = False
        hand_near_phone = False
        
        if hands_results.multi_hand_landmarks:
            phone_data['hand_detected'] = True
            for hand_landmarks in hands_results.multi_hand_landmarks:
                palm_x = hand_landmarks.landmark[9].x
                palm_y = hand_landmarks.landmark[9].y
                hand_center = np.array([palm_x, palm_y])
                
                hand_up = palm_y < self.HAND_UP_THRESHOLD
                
                if face_center is not None:
                    distance = np.linalg.norm(hand_center - face_center)
                    phone_data['hand_near_face'] = distance < self.HAND_FACE_DISTANCE
                
                if phone_bbox is not None:
                    hand_px, hand_py = int(palm_x * width), int(palm_y * height)
                    px1, py1, px2, py2 = phone_bbox
                    if px1-50 < hand_px < px2+50 and py1-50 < hand_py < py2+50:
                        hand_near_phone = True
        
        # Fusion with temporal smoothing
        current_state = 'NO_PHONE'
        current_confidence = 0.0
        
        if phone_data['phone_object_detected'] and hand_near_phone:
            current_state, current_confidence = 'PHONE_USAGE', 0.95
        elif phone_data['phone_object_detected'] and hand_up:
            current_state, current_confidence = 'PHONE_USAGE', 0.85
        elif phone_data['hand_near_face'] and hand_up:
            current_state, current_confidence = 'LIKELY_PHONE', 0.65
        elif phone_data['phone_object_detected']:
            current_state, current_confidence = 'PHONE_VISIBLE', 0.40
        elif hand_up and phone_data['hand_detected']:
            current_state, current_confidence = 'HAND_UP', 0.30
        
        self.detection_history.append({'state': current_state, 'confidence': current_confidence, 'is_phone_usage': current_state in ['PHONE_USAGE', 'LIKELY_PHONE']})
        if len(self.detection_history) > self.HISTORY_SIZE:
            self.detection_history.pop(0)
        
        if len(self.detection_history) >= 5:
            phone_usage_ratio = sum(1 for d in self.detection_history if d['is_phone_usage']) / len(self.detection_history)
            if phone_usage_ratio >= self.CONFIRMATION_THRESHOLD:
                state_counts = {}
                for d in self.detection_history:
                    state_counts[d['state']] = state_counts.get(d['state'], 0) + 1
                phone_data['state'] = max(state_counts, key=state_counts.get)
                phone_data['confidence'] = sum(d['confidence'] for d in self.detection_history) / len(self.detection_history)
            else:
                phone_data['state'] = 'HAND_UP' if current_state in ['PHONE_USAGE', 'LIKELY_PHONE'] else current_state
                phone_data['confidence'] = current_confidence * 0.5
        else:
            phone_data['state'], phone_data['confidence'] = current_state, current_confidence * 0.5
        
        return phone_data

# ============================================
# MODULE 4: MOUTH STATE DETECTOR
# ============================================
class MouthStateDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        
        self.MAR_YAWN_THRESHOLD = 0.4
        self.MAR_OPEN_THRESHOLD = 0.1
        self.YAWN_DURATION_THRESHOLD = 2
        self.MOUTH_TOP, self.MOUTH_BOTTOM, self.MOUTH_LEFT, self.MOUTH_RIGHT = 13, 14, 61, 291
        self.INNER_MOUTH_VERTICAL = [(13, 14), (312, 311)]
        self.mouth_state = "CLOSED"
        self.yawn_start_time = None
        
    def calculate_mar(self, mouth_points):
        vertical_distances = [dist.euclidean(mouth_points[top], mouth_points[bottom]) for top, bottom in self.INNER_MOUTH_VERTICAL]
        avg_vertical = np.mean(vertical_distances)
        horizontal = dist.euclidean(mouth_points[self.MOUTH_LEFT], mouth_points[self.MOUTH_RIGHT])
        return avg_vertical / horizontal if horizontal > 0 else 0
    
    def detect(self, frame):
        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        mouth_data = {'state': 'NO_FACE', 'mar': 0.0, 'is_yawning': False, 'yawn_duration': 0.0}
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            mouth_points = {idx: (int(landmarks[idx].x * width), int(landmarks[idx].y * height)) for idx in [self.MOUTH_TOP, self.MOUTH_BOTTOM, self.MOUTH_LEFT, self.MOUTH_RIGHT, 312, 311]}
            
            mar = self.calculate_mar(mouth_points)
            mouth_data['mar'] = mar
            
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
            else:
                self.mouth_state = "CLOSED"
                self.yawn_start_time = None
            
            mouth_data['state'] = self.mouth_state
        
        return mouth_data

# ============================================
# COMBINED SYSTEM
# ============================================
class DriverMonitoringSystem:
    def __init__(self, enable_logging=True, session_name=None):
        print("Initializing Driver Monitoring System...")
        print("Loading Module 1: Eye State Detection...")
        self.eye_detector = EyeStateDetector()
        print("✓ Eye detector ready")
        
        print("Loading Module 2: Head Pose Detection...")
        self.head_detector = HeadPoseDetector()
        print("✓ Head detector ready")
        
        print("Loading Module 3: Phone Detection (Hand + YOLO)...")
        self.phone_detector = PhoneDetector()
        print("✓ Phone detector ready")
        
        print("Loading Module 4: Mouth State Detection...")
        self.mouth_detector = MouthStateDetector()
        print("✓ Mouth detector ready")
        
        self.enable_logging = enable_logging
        if enable_logging:
            self.logger = DriverLogger(session_name)
        else:
            self.logger = None
        
        self.frame_count = 0
        print("\n✓ All 4 modules loaded successfully!")
        if enable_logging:
            print("✓ Logging enabled\n")
        
    def analyze_driver_state(self, eye_data, head_data, phone_data, mouth_data):
        alerts = []
        risk_level = "SAFE"
        
        if eye_data['is_microsleep']:
            alerts.append(f"MICROSLEEP! ({eye_data['closed_duration']:.1f}s)")
            risk_level = "CRITICAL"
        
        if phone_data['state'] == 'PHONE_USAGE':
            alerts.append(f"PHONE USAGE! ({phone_data['confidence']:.0%})")
            if risk_level not in ["CRITICAL"]:
                risk_level = "DANGER"
        
        if head_data['is_distracted']:
            alerts.append(f"DISTRACTED: Looking {head_data['state']}")
            if risk_level not in ["CRITICAL", "DANGER"]:
                risk_level = "DANGER"
        
        if mouth_data['is_yawning']:
            alerts.append(f"YAWNING - Fatigue ({mouth_data['yawn_duration']:.1f}s)")
            if risk_level == "SAFE":
                risk_level = "WARNING"
        
        if eye_data['state'] == 'CLOSED' and not eye_data['is_microsleep']:
            alerts.append("Eyes closing")
            if risk_level == "SAFE":
                risk_level = "WARNING"
        
        if phone_data['state'] == 'LIKELY_PHONE':
            alerts.append("Possible phone usage")
            if risk_level == "SAFE":
                risk_level = "WARNING"
        
        return {
            'risk_level': risk_level,
            'alerts': alerts,
            'eye_state': eye_data['state'],
            'head_state': head_data['state'],
            'phone_state': phone_data['state'],
            'mouth_state': mouth_data['state']
        }
    
    def process_frame(self, frame):
        height, width, _ = frame.shape
        self.frame_count += 1
        
        eye_data = self.eye_detector.detect(frame)
        head_data = self.head_detector.detect(frame)
        phone_data = self.phone_detector.detect(frame)
        mouth_data = self.mouth_detector.detect(frame)
        
        analysis = self.analyze_driver_state(eye_data, head_data, phone_data, mouth_data)
        
        if self.logger:
            self.logger.log_frame(self.frame_count, analysis, eye_data, head_data, phone_data, mouth_data)
        
        colors = {'SAFE': (0, 255, 0), 'WARNING': (0, 255, 255), 'DANGER': (0, 165, 255), 'CRITICAL': (0, 0, 255)}
        risk_color = colors[analysis['risk_level']]
        
        if analysis['risk_level'] != 'SAFE':
            thickness = 5 if analysis['risk_level'] == 'WARNING' else 10
            cv2.rectangle(frame, (5, 5), (width-5, height-5), risk_color, thickness)
        
        panel_width, panel_height = 350, 180
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (panel_width, panel_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        cv2.rectangle(frame, (0, 0), (panel_width, panel_height), risk_color, 3)
        
        y_offset = 30
        cv2.putText(frame, f"STATUS: {analysis['risk_level']}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, risk_color, 2)
        y_offset += 35
        cv2.putText(frame, f"Eyes: {analysis['eye_state']}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y_offset += 30
        cv2.putText(frame, f"Head: {analysis['head_state']}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y_offset += 30
        cv2.putText(frame, f"Phone: {analysis['phone_state']}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y_offset += 30
        cv2.putText(frame, f"Mouth: {analysis['mouth_state']}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        if analysis['alerts']:
            alert_y = height - 30
            for alert in reversed(analysis['alerts'][-3:]):
                (text_width, text_height), _ = cv2.getTextSize(f"⚠ {alert}", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                overlay = frame.copy()
                cv2.rectangle(overlay, (5, alert_y - text_height - 5), (text_width + 20, alert_y + 5), (0, 0, 0), -1)
                cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
                cv2.putText(frame, f"⚠ {alert}", (10, alert_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, risk_color, 2)
                alert_y -= 35
        
        metrics_x = width - 220
        overlay = frame.copy()
        cv2.rectangle(overlay, (metrics_x - 10, 0), (width, 130), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        cv2.rectangle(frame, (metrics_x - 10, 0), (width, 130), risk_color, 2)
        
        cv2.putText(frame, "METRICS", (metrics_x, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"EAR: {eye_data['ear']:.3f}", (metrics_x, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"MAR: {mouth_data['mar']:.3f}", (metrics_x, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"Yaw: {head_data['yaw']:.1f}°", (metrics_x, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"Pitch: {head_data['pitch']:.1f}°", (metrics_x, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame, analysis

# ============================================
# MAIN APPLICATION
# ============================================
def main():
    print("=" * 70)
    print(" " * 15 + "DRIVER MONITORING SYSTEM")
    print("=" * 70)
    print("\n🔍 Active Modules:")
    print("  ✓ Module 1: Eye State Detection (Microsleep detection)")
    print("  ✓ Module 2: Head Pose Detection (Distraction detection)")
    print("  ✓ Module 3: Phone Detection (Hand + YOLO fusion)")
    print("  ✓ Module 4: Mouth State Detection (Fatigue/yawn detection)")
    print("\n📊 Risk Levels:")
    print("  🟢 SAFE      - All systems normal")
    print("  🟡 WARNING   - Minor issues detected")
    print("  🟠 DANGER    - Serious distraction")
    print("  🔴 CRITICAL  - Immediate danger (microsleep)")
    print("\n⌨️  Controls:")
    print("  Press 'q' to quit and save logs")
    print("  Press 's' to save screenshot")
    print("  Press 'p' to print current statistics")
    print("=" * 70)
    
    system = DriverMonitoringSystem(enable_logging=True)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    fps_start_time = time.time()
    fps_counter = 0
    fps = 0
    screenshot_counter = 0
    
    print("\n🎥 Camera started! Monitoring driver...\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break
        
        frame = cv2.flip(frame, 1)
        annotated_frame, analysis = system.process_frame(frame)
        
        fps_counter += 1
        if time.time() - fps_start_time > 1:
            fps = fps_counter
            fps_counter = 0
            fps_start_time = time.time()
        
        cv2.putText(annotated_frame, f"FPS: {fps}", (10, annotated_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        if analysis['risk_level'] == 'CRITICAL':
            print(f"🚨 CRITICAL: {' | '.join(analysis['alerts'])}")
        elif analysis['risk_level'] == 'DANGER':
            print(f"⚠️  DANGER: {' | '.join(analysis['alerts'])}")
        
        cv2.imshow('Driver Monitoring System', annotated_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            screenshot_counter += 1
            filename = f"screenshot_{screenshot_counter}.png"
            cv2.imwrite(filename, annotated_frame)
            print(f"📸 Screenshot saved: {filename}")
        elif key == ord('p'):
            if system.logger:
                system.logger.print_stats()
    
    cap.release()
    cv2.destroyAllWindows()
    
    if system.logger:
        print("\n💾 Saving session data...")
        system.logger.save_session()
    
    print("\n" + "=" * 70)
    print(" " * 20 + "System Stopped")
    print("=" * 70)

if __name__ == "__main__":
    main()