from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")

# Database file path
DB_FILE = 'db.json'

def init_db():
    """Initialize database file if it doesn't exist"""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({'data': []}, f)

def read_db():
    """Read data from database"""
    init_db()
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def write_db(data):
    """Write data to database"""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def _parse_timestamp(value):
    """Safely parse ISO timestamps"""
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return datetime.min

def _risk_from_score(score):
    """Return risk label based on score"""
    if score >= 80:
        return 'Low Risk'
    if score >= 50:
        return 'Medium Risk'
    return 'High Risk'

def calculate_safety_score():
    """Compute latest safety score from database"""
    db_data = read_db()
    entries = db_data.get('data', [])

    latest_summary = None
    for entry in entries:
        values = entry.get('values', {})
        if isinstance(values, dict) and 'safety_score' in values:
            if latest_summary is None or _parse_timestamp(entry.get('timestamp')) > _parse_timestamp(latest_summary.get('timestamp')):
                latest_summary = entry

    if latest_summary:
        raw_score = latest_summary.get('values', {}).get('safety_score', 0)
        score = max(0, min(100, int(raw_score)))
        risk = latest_summary.get('values', {}).get('risk_category') or _risk_from_score(score)
        last_updated = latest_summary.get('timestamp')
    else:
        incident_count = sum(1 for entry in entries if entry.get('type') == 'incident')
        score = max(0, 100 - incident_count)
        risk = _risk_from_score(score)
        last_updated = datetime.now().isoformat()

    return {
        'score': score,
        'risk': risk,
        'lastUpdated': last_updated
    }

# REST API Routes
@app.route('/', methods=['GET'])
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Backend is running! Ready for real-time driver data.'
    })

@app.route('/api/data', methods=['POST'])
def create_data():
    """Create new sensor data entry"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'deviceId' not in data or 'type' not in data:
            return jsonify({'error': 'Missing required fields: deviceId and type'}), 400
        
        # Read existing data
        db_data = read_db()
        
        # Create new entry
        entry = {
            'id': str(uuid.uuid4()),
            'deviceId': data['deviceId'],
            'timestamp': data.get('timestamp', datetime.now().isoformat()),
            'type': data['type'],
            'values': data.get('values', {})
        }
        
        # Add to database
        db_data['data'].append(entry)
        write_db(db_data)
        
        # Emit real-time update via Socket.IO
        socketio.emit('driverUpdate', {
            **entry,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({'ok': True, 'id': entry['id']}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data', methods=['GET'])
def get_data():
    """Get all data entries"""
    try:
        db_data = read_db()
        return jsonify(db_data['data'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get aggregated statistics"""
    try:
        db_data = read_db()
        entries = db_data['data']
        
        # Filter by type if provided
        sensor_type = request.args.get('type')
        if sensor_type:
            entries = [e for e in entries if e.get('type') == sensor_type]
        
        if not entries:
            return jsonify({'count': 0, 'averages': {}})
        
        # Calculate averages for numeric values
        numeric_sums = {}
        numeric_counts = {}
        
        for entry in entries:
            values = entry.get('values', {})
            if isinstance(values, dict):
                for key, value in values.items():
                    if isinstance(value, (int, float)):
                        numeric_sums[key] = numeric_sums.get(key, 0) + value
                        numeric_counts[key] = numeric_counts.get(key, 0) + 1
            elif isinstance(values, (int, float)):
                numeric_sums['value'] = numeric_sums.get('value', 0) + values
                numeric_counts['value'] = numeric_counts.get('value', 0) + 1
        
        # Calculate averages
        averages = {
            key: numeric_sums[key] / numeric_counts[key]
            for key in numeric_sums
        }
        
        return jsonify({
            'count': len(entries),
            'averages': averages
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/safety-score', methods=['GET'])
def get_safety_score_route():
    """Provide the latest safety score derived from stored data"""
    try:
        score_payload = calculate_safety_score()
        return jsonify(score_payload)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Socket.IO Events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Dashboard connected for real-time updates')
    emit('connected', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Dashboard disconnected')

@socketio.on('sensorData')
def handle_sensor_data(data):
    """Handle incoming sensor data from devices"""
    try:
        # Validate data
        if not data or 'deviceId' not in data or 'type' not in data:
            emit('error', {'message': 'Invalid data format'})
            return
        
        # Create entry
        entry = {
            'id': str(uuid.uuid4()),
            'deviceId': data['deviceId'],
            'timestamp': data.get('timestamp', datetime.now().isoformat()),
            'type': data['type'],
            'values': data.get('values', {})
        }
        
        # Save to database
        db_data = read_db()
        db_data['data'].append(entry)
        write_db(db_data)
        
        # Broadcast to all connected clients
        socketio.emit('driverUpdate', {
            **entry,
            'timestamp': datetime.now().isoformat()
        })
        
        print(f'Broadcasted update: {data}')
        
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('sendWarning')
def handle_warning(data):
    """Handle warning messages"""
    warning = data.get('message', '')
    emit('warningReceived', {'message': warning})
    print(f'Warning sent: {warning}')

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the app
    print('Starting Flask server on http://localhost:5000')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

