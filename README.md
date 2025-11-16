# Smart Driver Monitoring & Insurance Telematics | DriveGuardAI

## Overview 
This project is a real-time driver monitoring and behavior analytics system that detects the driver’s physical and emotional state to prevent accidents and risky situations on the road.  
It combines in-cabin sensors (heart rate, face camera, microphone) with driving behavior data (speeding, harsh events, rule violations, accidents) to generate alerts for the driver and an analytics dashboard for the insurance company.  

## Core Objectives 
- Detect driver states such as drowsy, drunk, distracted, or angry from physiological and visual cues.  
- Alert or wake up the driver in real time using sound, voice, or haptic feedback to avoid accidents.  
- Continuously monitor driving style (speeding, harsh braking, policy violations) using telematics data.   
- Provide an insurer-facing dashboard to track driver risk scores, trends, incidents, and compliance, enabling bonuses or penalties.   

## Features
- Real-time drowsiness, distraction, and emotion detection from face expressions and eye/mouth activity.  
- Heartbeat and basic vital monitoring to detect stress, fatigue, or abnormal patterns while driving.   
- Audio-based monitoring for signs like shouting, conflict, or abnormal noise patterns in the cabin.   
- Telematics-based driving behavior analysis (speed limit compliance, harsh events, crash detection).   
- In-vehicle alerting module (alarm, voice prompts, or notifications) when risk exceeds a threshold.  
- Web dashboard for insurers to visualize risk scores, history, and generate reports per driver or fleet.   

## System Architecture
- Edge device in the vehicle captures video, audio, and sensor data in real time.
- Machine learning models run on the edge or server to classify driver state (normal, drowsy, drunk, angry, distracted).   
- Driving behavior data is collected from GPS, IMU, and vehicle telematics (speed, braking, cornering, acceleration).   
- All events and risk scores are streamed to a backend API and stored in a time-series database.  
- An insurer dashboard consumes this data to display KPIs, risk trends, and driver rankings.   

## Data Sources 
- Heart rate and vitals from in-seat sensors (ECG/PPG modules).   
- Face and eye region from an in-cabin camera for drowsiness, distraction, and emotion detection.  
- Cabin audio from a microphone for stress and conflict cues and voice alerts.   
- Driving behavior from telematics and CAN bus (speed, braking, steering, GPS).   

## Machine Learning Components 
- Computer vision models for eye aspect ratio, yawning, gaze direction, and face expression classification.  
- Optional deep learning models (CNNs, YOLO, or ViT-based architectures) for robust driver state detection.  
- Time-series and rule-based models for telematics risk scoring (speeding frequency, harsh events, crash patterns).   
- Fusion module that combines physiological, visual, audio, and telematics features into a single risk score per time window.  

## Real-Time Alerts
- Local alerts in the vehicle (buzzer, audio message) when drowsiness or distraction persists over a set number of frames or seconds.   
- Escalation logic for repeated high-risk behavior (for example multiple speeding episodes or near-crash events).   
- Optional connectivity to send critical alerts (collision, suspected intoxication) to an emergency contact or operations center.   

## Insurance Dashboard 
- Per-driver risk score based on behavior and state over time (daily, weekly, monthly).   
- Visualization of key metrics: speeding ratio, harsh events, drowsy events, distraction events, total driving hours, and incidents.  
- Segmentation of drivers into low, medium, and high risk groups to support pricing and rewards.   
- Exportable reports and APIs so insurers can integrate the scores into their existing policy systems.   

## Tech Stack
- Backend: Python (Flask), REST APIs. 
- Models: PyTorch, Yolov8n to run on the Raspberry Pi and MediaPipe models for classical vision. For turn detection used GeoPy and Shapely libraries.
- Edge: Raspberry Pi, in-vehicle capturing camera, audio, and sensor data.
- Database: TimescaleDB for events and metrics storage.
- Dashboard: React.

## Getting Started
1. Clone the repository and install dependencies for backend, models, and dashboard.  
2. Configure sensor and camera sources (video device index, audio input, heart rate sensor connection).
3. Start the backend API for data ingestion and real-time inference.  
4. Launch the driver monitoring client (camera + sensors) and connect it to the backend.   
5. Run the insurance dashboard and log in as an insurer to view drivers, scores, and alerts.   

## Data Privacy & Ethics 
This system processes highly sensitive biometric, audio, and behavioral data, so strict access control, encryption, and data minimization are required.   
Insurers and fleet operators should obtain explicit consent, provide transparency about how data is used, and avoid discriminatory or opaque decision-making.   

## Roadmap
- Add support for more emotions and stress levels using multimodal fusion.   
- Improve calibration and personalization of risk scoring per driver and vehicle segment.   
- Integrate with external insurance platforms for automatic bonus/penalty application.   