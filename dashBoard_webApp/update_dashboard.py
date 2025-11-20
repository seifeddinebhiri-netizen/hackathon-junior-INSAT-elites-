"""
Script to read driver logs from CSV files and update the dashboard backend.

This script reads all CSV files in the driver_logs directory and sends 
aggregated data to the Flask backend API.
"""

import csv
import os
import json
from datetime import datetime
from collections import defaultdict
from pathlib import Path
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    try:
        from urllib.request import urlopen, Request
        from urllib.error import URLError
        import urllib.parse
        HAS_URLLIB = True
    except ImportError:
        HAS_URLLIB = False

# Configuration
DRIVER_LOGS_DIR = Path(__file__).parent.parent / 'distraction detector' / 'driver_logs'
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')
DEVICE_ID = os.getenv('DEVICE_ID', 'driver-monitor-001')

def read_driver_logs(log_dir):
    """Read all CSV log files from the directory"""
    log_files = []
    log_dir_path = Path(log_dir)
    
    if not log_dir_path.exists():
        print(f"[-] Directory {log_dir} not found!")
        return []
    
    # Find all CSV files in the directory
    for csv_file in log_dir_path.glob("session_*.csv"):
        log_files.append(csv_file)
    
    if not log_files:
        print(f"[!] No log files found in {log_dir}")
        return []
    
    print(f"[+] Found {len(log_files)} log file(s)")
    return log_files

def parse_csv_log(file_path):
    """Parse a single CSV log file and extract statistics"""
    data = {
        'session_name': file_path.stem,
        'file_path': str(file_path),
        'total_frames': 0,
        'risk_counts': defaultdict(int),
        'eye_states': defaultdict(int),
        'head_states': defaultdict(int),
        'phone_states': defaultdict(int),
        'mouth_states': defaultdict(int),
        'incidents': [],
        'timestamps': [],
        'ear_values': [],
        'mar_values': [],
        'yaw_angles': [],
        'pitch_angles': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                data['total_frames'] += 1
                
                # Count risk levels
                risk_level = row.get('risk_level', 'UNKNOWN')
                data['risk_counts'][risk_level] += 1
                
                # Count states
                data['eye_states'][row.get('eye_state', 'UNKNOWN')] += 1
                data['head_states'][row.get('head_state', 'UNKNOWN')] += 1
                data['phone_states'][row.get('phone_state', 'UNKNOWN')] += 1
                data['mouth_states'][row.get('mouth_state', 'UNKNOWN')] += 1
                
                # Collect incidents (non-SAFE entries)
                alerts = row.get('alerts', '').strip()
                if risk_level != 'SAFE' and alerts:
                    incident = {
                        'timestamp': row.get('timestamp', ''),
                        'risk_level': risk_level,
                        'alerts': alerts,
                        'eye_state': row.get('eye_state', ''),
                        'head_state': row.get('head_state', ''),
                        'phone_state': row.get('phone_state', '')
                    }
                    data['incidents'].append(incident)
                
                # Collect metric values
                timestamp = row.get('timestamp', '')
                if timestamp:
                    data['timestamps'].append(timestamp)
                
                try:
                    ear = float(row.get('ear_value', 0))
                    mar = float(row.get('mar_value', 0))
                    yaw = float(row.get('yaw_angle', 0))
                    pitch = float(row.get('pitch_angle', 0))
                    
                    data['ear_values'].append(ear)
                    data['mar_values'].append(mar)
                    data['yaw_angles'].append(yaw)
                    data['pitch_angles'].append(pitch)
                except (ValueError, TypeError):
                    pass
        
        print(f"  [+] Parsed {data['total_frames']} frames from {file_path.name}")
        
    except Exception as e:
        print(f"  [-] Error reading {file_path}: {e}")
    
    return data

def calculate_statistics(data):
    """Calculate aggregated statistics from parsed data"""
    stats = {
        'total_frames': data['total_frames'],
        'risk_distribution': dict(data['risk_counts']),
        'state_distribution': {
            'eye_states': dict(data['eye_states']),
            'head_states': dict(data['head_states']),
            'phone_states': dict(data['phone_states']),
            'mouth_states': dict(data['mouth_states'])
        },
        'metrics': {}
    }
    
    # Calculate averages
    if data['ear_values']:
        stats['metrics']['avg_ear'] = sum(data['ear_values']) / len(data['ear_values'])
        stats['metrics']['min_ear'] = min(data['ear_values'])
        stats['metrics']['max_ear'] = max(data['ear_values'])
    
    if data['mar_values']:
        stats['metrics']['avg_mar'] = sum(data['mar_values']) / len(data['mar_values'])
        stats['metrics']['min_mar'] = min(data['mar_values'])
        stats['metrics']['max_mar'] = max(data['mar_values'])
    
    if data['yaw_angles']:
        stats['metrics']['avg_yaw'] = sum(data['yaw_angles']) / len(data['yaw_angles'])
    
    if data['pitch_angles']:
        stats['metrics']['avg_pitch'] = sum(data['pitch_angles']) / len(data['pitch_angles'])
    
    # Count incidents
    stats['incident_count'] = len(data['incidents'])
    stats['critical_count'] = sum(1 for i in data['incidents'] if i['risk_level'] == 'CRITICAL')
    stats['danger_count'] = sum(1 for i in data['incidents'] if i['risk_level'] == 'DANGER')
    stats['warning_count'] = sum(1 for i in data['incidents'] if i['risk_level'] == 'WARNING')
    
    # Calculate safety score (0-100)
    if stats['total_frames'] > 0:
        safe_ratio = stats['risk_distribution'].get('SAFE', 0) / stats['total_frames']
        warning_penalty = stats['warning_count'] * 0.02
        danger_penalty = stats['danger_count'] * 0.05
        critical_penalty = stats['critical_count'] * 0.1
        
        safety_score = (safe_ratio * 100) - (warning_penalty * 100) - (danger_penalty * 100) - (critical_penalty * 100)
        stats['safety_score'] = max(0, min(100, safety_score))
    else:
        stats['safety_score'] = 100
    
    # Determine risk category
    if stats['safety_score'] >= 80:
        stats['risk_category'] = 'Low Risk'
    elif stats['safety_score'] >= 60:
        stats['risk_category'] = 'Medium Risk'
    else:
        stats['risk_category'] = 'High Risk'
    
    return stats, data['incidents']

def send_to_backend(stats, incidents, session_name):
    """Send data to the Flask backend API"""
    print(f"\n[->] Sending data to backend at {BACKEND_URL}...")
    
    if not HAS_REQUESTS and not HAS_URLLIB:
        print("[-] Cannot send data: No HTTP library available!")
        print("   Please install 'requests': pip install requests")
        return False
    
    # Test backend connection
    try:
        if HAS_REQUESTS:
            response = requests.get(f"{BACKEND_URL}/", timeout=5)
            if response.status_code != 200:
                print(f"[-] Backend not responding correctly. Status: {response.status_code}")
                return False
        else:
            # Using urllib
            req = Request(f"{BACKEND_URL}/")
            response = urlopen(req, timeout=5)
            if response.getcode() != 200:
                print(f"[-] Backend not responding correctly. Status: {response.getcode()}")
                return False
    except Exception as e:
        print(f"[-] Cannot connect to backend at {BACKEND_URL}")
        print(f"   Make sure the Flask server is running: python app.py")
        print(f"   Error: {e}")
        return False
    
    # Send session summary
    summary_payload = {
        'deviceId': DEVICE_ID,
        'type': 'session_summary',
        'timestamp': datetime.now().isoformat(),
        'values': {
            'session_name': session_name,
            **stats
        }
    }
    
    try:
        if HAS_REQUESTS:
            response = requests.post(
                f"{BACKEND_URL}/api/data",
                json=summary_payload,
                timeout=10
            )
            status_code = response.status_code
        else:
            # Using urllib
            data = json.dumps(summary_payload).encode('utf-8')
            req = Request(
                f"{BACKEND_URL}/api/data",
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            response = urlopen(req, timeout=10)
            status_code = response.getcode()
        
        if status_code in [200, 201]:
            print(f"  [+] Session summary sent")
        else:
            print(f"  [!] Failed to send summary: {status_code}")
    except Exception as e:
        print(f"  [-] Error sending summary: {e}")
    
    # Send recent incidents (last 10)
    recent_incidents = incidents[-10:] if len(incidents) > 10 else incidents
    
    for incident in recent_incidents:
        incident_payload = {
            'deviceId': DEVICE_ID,
            'type': 'incident',
            'timestamp': incident['timestamp'],
            'values': {
                'risk_level': incident['risk_level'],
                'alerts': incident['alerts'],
                'eye_state': incident['eye_state'],
                'head_state': incident['head_state'],
                'phone_state': incident['phone_state']
            }
        }
        
        try:
            if HAS_REQUESTS:
                requests.post(
                    f"{BACKEND_URL}/api/data",
                    json=incident_payload,
                    timeout=5
                )
            else:
                # Using urllib
                data = json.dumps(incident_payload).encode('utf-8')
                req = Request(
                    f"{BACKEND_URL}/api/data",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                urlopen(req, timeout=5)
        except Exception as e:
            print(f"  [!] Error sending incident: {e}")
    
    if recent_incidents:
        print(f"  [+] Sent {len(recent_incidents)} incident(s)")
    
    return True

def main():
    """Main function"""
    print("=" * 70)
    print(" " * 15 + "DASHBOARD UPDATE SCRIPT")
    print("=" * 70)
    print()
    
    # Read log files
    log_files = read_driver_logs(DRIVER_LOGS_DIR)
    if not log_files:
        return
    
    # Process all log files
    all_stats = []
    all_incidents = []
    
    for log_file in log_files:
        print(f"\n[*] Processing: {log_file.name}")
        data = parse_csv_log(log_file)
        
        if data['total_frames'] > 0:
            stats, incidents = calculate_statistics(data)
            all_stats.append((data['session_name'], stats))
            all_incidents.extend(incidents)
    
    if not all_stats:
        print("\n[!] No valid data found in log files!")
        return
    
    # Aggregate across all sessions
    print(f"\n[*] Aggregating statistics from {len(all_stats)} session(s)...")
    
    total_frames = sum(s[1]['total_frames'] for s in all_stats)
    total_incidents = len(all_incidents)
    
    # Combine risk distributions
    combined_risk = defaultdict(int)
    for _, stats in all_stats:
        for risk, count in stats['risk_distribution'].items():
            combined_risk[risk] += count
    
    # Calculate overall safety score
    overall_safety_score = 100
    if total_frames > 0:
        safe_ratio = combined_risk.get('SAFE', 0) / total_frames
        warning_count = sum(1 for i in all_incidents if i['risk_level'] == 'WARNING')
        danger_count = sum(1 for i in all_incidents if i['risk_level'] == 'DANGER')
        critical_count = sum(1 for i in all_incidents if i['risk_level'] == 'CRITICAL')
        
        overall_safety_score = (safe_ratio * 100) - (warning_count * 0.02 * 100) - (danger_count * 0.05 * 100) - (critical_count * 0.1 * 100)
        overall_safety_score = max(0, min(100, overall_safety_score))
    
    if overall_safety_score >= 80:
        risk_category = 'Low Risk'
    elif overall_safety_score >= 60:
        risk_category = 'Medium Risk'
    else:
        risk_category = 'High Risk'
    
    overall_stats = {
        'total_frames': total_frames,
        'total_sessions': len(all_stats),
        'safety_score': round(overall_safety_score, 1),
        'risk_category': risk_category,
        'risk_distribution': dict(combined_risk),
        'incident_count': total_incidents,
        'critical_count': sum(1 for i in all_incidents if i['risk_level'] == 'CRITICAL'),
        'danger_count': sum(1 for i in all_incidents if i['risk_level'] == 'DANGER'),
        'warning_count': sum(1 for i in all_incidents if i['risk_level'] == 'WARNING')
    }
    
    print(f"\n[*] Overall Statistics:")
    print(f"  • Total Frames: {total_frames}")
    print(f"  • Total Sessions: {len(all_stats)}")
    print(f"  • Safety Score: {overall_stats['safety_score']}/100")
    print(f"  • Risk Category: {risk_category}")
    print(f"  • Total Incidents: {total_incidents}")
    print(f"    - Critical: {overall_stats['critical_count']}")
    print(f"    - Danger: {overall_stats['danger_count']}")
    print(f"    - Warning: {overall_stats['warning_count']}")
    
    # Send to backend (use most recent session name)
    if all_stats:
        latest_session = all_stats[-1][0]
        send_to_backend(overall_stats, all_incidents, latest_session)
    
    print("\n" + "=" * 70)
    print(" " * 20 + "Update Complete!")
    print("=" * 70)
    print("\n[Tip] Check the dashboard at http://localhost:3000 (if frontend is running)")

if __name__ == "__main__":
    main()
