# Update Dashboard Script

This script reads logs from the distraction detector and sends them to the dashboard backend API.

## Features

- ✅ Reads CSV log files from `distraction detector/driver_logs/`
- ✅ Parses and sends incidents (DANGER/CRITICAL events) to backend
- ✅ Sends behavior data for regular monitoring
- ✅ Calculates and sends safety scores
- ✅ Batch processing with progress indicators
- ✅ Error handling and connection checking

## Prerequisites

Install required Python packages:

```bash
pip install requests
```

Or install all backend requirements:

```bash
cd backend
pip install -r requirements.txt
```

## Usage

### Basic Usage

Process all log files in the default directory:

```bash
python update_dashboard.py
```

### Process a Specific File

```bash
python update_dashboard.py --file "distraction detector/driver_logs/session_20251116_123232.csv"
```

### Custom Backend URL

```bash
python update_dashboard.py --backend-url http://localhost:5000
```

### Custom Device ID

```bash
python update_dashboard.py --device-id driver-monitor-002
```

### Custom Logs Directory

```bash
python update_dashboard.py --logs-dir "path/to/logs"
```

### All Options

```bash
python update_dashboard.py \
  --backend-url http://localhost:5000 \
  --device-id driver-monitor-001 \
  --logs-dir "distraction detector/driver_logs"
```

## Environment Variables

You can also set these as environment variables:

```bash
export BACKEND_URL=http://localhost:5000
export DEVICE_ID=driver-monitor-001
python update_dashboard.py
```

## How It Works

1. **Connection Check**: Verifies backend is accessible
2. **File Discovery**: Finds all `session_*.csv` files in the logs directory
3. **Data Parsing**: 
   - Converts CSV rows to API format
   - Identifies incidents (DANGER/CRITICAL) vs behavior data
4. **Data Sending**: 
   - Sends entries to `/api/data` endpoint
   - Processes in batches to avoid overwhelming the backend
5. **Safety Score**: Calculates and sends final safety score summary

## Data Types Sent

### Incidents (`type: 'incident'`)
Sent when `risk_level` is `DANGER` or `CRITICAL`:
- Includes severity, incident type, and all sensor data
- Appears in the Incidents Log component

### Behavior Data (`type: 'behavior'`)
Sent for regular monitoring frames:
- Includes eye state, head pose, phone detection, mouth state
- Used for behavior analysis

### Safety Score (`type: 'safetyScore'`)
Calculated summary sent at the end:
- Score (0-100) based on incidents and behaviors
- Risk category (Low/Medium/High Risk)
- Total frames processed

## Example Output

```
======================================================================
                    Dashboard Update Script
======================================================================
Backend URL: http://localhost:5000
Device ID: driver-monitor-001
Logs Directory: distraction detector/driver_logs
======================================================================
✓ Backend connection successful

Found 1 log file(s)

📄 Processing: session_20251116_123232.csv
   ✓ Sent 50 entries...
   ✓ Sent 100 entries...
   📊 Calculating safety score from 1334 entries...
   ✓ Safety score sent: 87/100 (Low Risk)
   ✅ Completed: 1335 sent, 0 errors

======================================================================
                    Summary
======================================================================
Total entries sent: 1335
Total errors: 0
======================================================================
```

## Troubleshooting

### Backend Not Running
```
❌ Cannot connect to backend at http://localhost:5000
```
**Solution**: Start the backend server:
```bash
cd backend
python app.py
```

### No Log Files Found
```
⚠️  No CSV log files found in distraction detector/driver_logs
```
**Solution**: Ensure the distraction detector has created log files, or check the path.

### Connection Timeout
**Solution**: Increase timeout in the script or check network connectivity.

## Integration with Distraction Detector

After running the distraction detector, logs are automatically saved to:
```
distraction detector/driver_logs/session_YYYYMMDD_HHMMSS.csv
```

Run this script to push those logs to the dashboard:

```bash
# After running distraction detector
python update_dashboard.py
```

The dashboard will update in real-time with:
- Recent incidents and alerts
- Safety metrics and scores
- Behavior breakdown
- Driver profile statistics

