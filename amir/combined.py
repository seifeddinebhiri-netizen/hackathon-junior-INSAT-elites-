import cv2
import mediapipe as mp
import numpy as np
from ultralytics import YOLO

class PhoneDetector:
    def __init__(self):
        # Hand detection with Mediapipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.4,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Face detection for reference
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # YOLO for phone detection (lightweight)
        try:
            print("Loading YOLOv8n model...")
            self.yolo_model = YOLO('yolov8n.pt')  # Nano version - very lightweight!
            self.yolo_loaded = True
            print("✓ YOLOv8n model loaded successfully")
        except Exception as e:
            print(f"⚠️ Could not load YOLO: {e}")
            print("Running with hand detection only")
            self.yolo_loaded = False
        
        # Detection parameters
        self.HAND_FACE_DISTANCE = 0.3
        self.HAND_UP_THRESHOLD = 0.6
        self.PHONE_CONFIDENCE = 0.28
        
        # State
        self.phone_state = "NO_PHONE"
        
    def detect(self, frame):
        """
        Combined phone detection using hands + YOLO
        Returns: dict with phone usage information
        """
        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        phone_data = {
            'state': 'NO_PHONE',
            'hand_detected': False,
            'phone_object_detected': False,
            'hand_near_face': False,
            'confidence': 0.0,
            'reason': '',
            'frame': frame.copy()
        }
        
        # 1. YOLO Phone Detection
        phone_bbox = None
        if self.yolo_loaded:
            results = self.yolo_model(frame, verbose=False, conf=self.PHONE_CONFIDENCE)
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    class_id = int(box.cls[0])
                    class_name = result.names[class_id]
                    confidence = float(box.conf[0])
                    
                    # Check if it's a phone (class 67 in COCO) or cell phone
                    if 'phone' in class_name.lower() or class_id == 67:
                        phone_data['phone_object_detected'] = True
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        phone_bbox = (int(x1), int(y1), int(x2), int(y2))
                        
                        # Draw phone detection
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), 
                                     (0, 0, 255), 3)
                        cv2.putText(frame, f"Phone: {confidence:.2f}", 
                                   (int(x1), int(y1) - 10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # 2. Hand Detection
        hands_results = self.hands.process(rgb_frame)
        face_results = self.face_mesh.process(rgb_frame)
        
        face_center = None
        if face_results.multi_face_landmarks:
            landmarks = face_results.multi_face_landmarks[0].landmark
            face_center = np.array([landmarks[1].x, landmarks[1].y])
            
            face_x = int(face_center[0] * width)
            face_y = int(face_center[1] * height)
            cv2.circle(frame, (face_x, face_y), 8, (255, 0, 255), -1)
        
        hand_up = False
        hand_near_phone = False
        
        if hands_results.multi_hand_landmarks:
            phone_data['hand_detected'] = True
            
            for hand_landmarks in hands_results.multi_hand_landmarks:
                # Draw hand
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2)
                )
                
                # Hand center (palm)
                palm_x = hand_landmarks.landmark[9].x
                palm_y = hand_landmarks.landmark[9].y
                hand_center = np.array([palm_x, palm_y])
                
                # Check if hand is up
                hand_up = palm_y < self.HAND_UP_THRESHOLD
                
                # Check if hand is near face
                if face_center is not None:
                    distance = np.linalg.norm(hand_center - face_center)
                    phone_data['hand_near_face'] = distance < self.HAND_FACE_DISTANCE
                    
                    if phone_data['hand_near_face']:
                        hand_x = int(palm_x * width)
                        hand_y = int(palm_y * height)
                        face_x = int(face_center[0] * width)
                        face_y = int(face_center[1] * height)
                        cv2.line(frame, (hand_x, hand_y), (face_x, face_y), 
                                (255, 0, 0), 3)
                
                # Check if hand is near phone object
                if phone_bbox is not None:
                    hand_px = int(palm_x * width)
                    hand_py = int(palm_y * height)
                    px1, py1, px2, py2 = phone_bbox
                    
                    # Check if hand is within phone bounding box (with margin)
                    margin = 50
                    if (px1 - margin < hand_px < px2 + margin and 
                        py1 - margin < hand_py < py2 + margin):
                        hand_near_phone = True
                        cv2.circle(frame, (hand_px, hand_py), 15, (0, 255, 255), -1)
        
        # 3. Fusion Logic - Determine Phone Usage State
        if phone_data['phone_object_detected'] and hand_near_phone:
            # STRONGEST: Phone object + hand touching it
            phone_data['state'] = 'PHONE_USAGE'
            phone_data['confidence'] = 0.95
            phone_data['reason'] = 'Phone object + hand contact'
            
        elif phone_data['phone_object_detected'] and hand_up:
            # STRONG: Phone visible + hand up
            phone_data['state'] = 'PHONE_USAGE'
            phone_data['confidence'] = 0.85
            phone_data['reason'] = 'Phone object + hand raised'
            
        elif phone_data['hand_near_face'] and hand_up:
            # MEDIUM: Hand near face in phone position
            phone_data['state'] = 'LIKELY_PHONE'
            phone_data['confidence'] = 0.65
            phone_data['reason'] = 'Hand near face (phone position)'
            
        elif phone_data['phone_object_detected']:
            # LOW: Phone visible but not being held
            phone_data['state'] = 'PHONE_VISIBLE'
            phone_data['confidence'] = 0.40
            phone_data['reason'] = 'Phone in view (not held)'
            
        elif hand_up and phone_data['hand_detected']:
            # WEAK: Just hand up
            phone_data['state'] = 'HAND_UP'
            phone_data['confidence'] = 0.30
            phone_data['reason'] = 'Hand raised (suspicious)'
            
        else:
            phone_data['state'] = 'NO_PHONE'
            phone_data['confidence'] = 0.0
            phone_data['reason'] = 'All clear'
        
        # 4. Visualization
        # Color based on risk level
        if phone_data['state'] == 'PHONE_USAGE':
            color = (0, 0, 255)  # Red - Danger
            cv2.rectangle(frame, (5, 5), (width-5, height-5), color, 8)
            cv2.putText(frame, "PHONE USAGE!", (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
        elif phone_data['state'] == 'LIKELY_PHONE':
            color = (0, 140, 255)  # Orange - Warning
            cv2.rectangle(frame, (5, 5), (width-5, height-5), color, 5)
        elif phone_data['state'] == 'PHONE_VISIBLE':
            color = (0, 255, 255)  # Yellow - Caution
        elif phone_data['state'] == 'HAND_UP':
            color = (0, 255, 0)  # Green - Monitor
        else:
            color = (0, 255, 0)  # Green - Safe
        
        # Status display
        cv2.putText(frame, f"State: {phone_data['state']}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, f"Confidence: {phone_data['confidence']:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Reason: {phone_data['reason']}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Indicators
        indicators_y = height - 60
        if phone_data['phone_object_detected']:
            cv2.putText(frame, "📱 Phone Object", (10, indicators_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            indicators_y += 20
        if phone_data['hand_detected']:
            cv2.putText(frame, "✋ Hand", (10, indicators_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            indicators_y += 20
        if phone_data['hand_near_face']:
            cv2.putText(frame, "📞 Near Face", (10, indicators_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        
        phone_data['frame'] = frame
        return phone_data

# Main test
if __name__ == "__main__":
    print("=" * 50)
    print("MODULE 3: Combined Phone Detection")
    print("=" * 50)
    print("\nDetection Methods:")
    print("1. YOLOv8n - Phone object detection")
    print("2. Mediapipe - Hand tracking")
    print("3. Fusion - Combining both for accuracy")
    print("\nStates:")
    print("- NO_PHONE: Safe")
    print("- HAND_UP: Suspicious")
    print("- PHONE_VISIBLE: Phone in view")
    print("- LIKELY_PHONE: Hand near face")
    print("- PHONE_USAGE: DANGER! Using phone")
    print("\nPress 'q' to quit")
    print("=" * 50)
    
    detector = PhoneDetector()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        result = detector.detect(frame)
        
        # Print alerts
        if result['state'] == 'PHONE_USAGE':
            print(f"🚨 PHONE USAGE! Confidence: {result['confidence']:.2f} | {result['reason']}")
        elif result['state'] == 'LIKELY_PHONE':
            print(f"⚠️  Likely phone use | {result['reason']}")
        
        cv2.imshow('Module 3: Phone Detection (Hand + YOLO)', result['frame'])
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n=== Module 3 Test Complete ===")