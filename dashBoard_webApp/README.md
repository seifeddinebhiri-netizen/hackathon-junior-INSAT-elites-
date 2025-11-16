# DriveGuard AI Dashboard

A modern driver monitoring and insurance analytics dashboard built with **React** (Vite) and **Flask**.

## 🏗️ Architecture

- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **Backend**: Flask + Flask-SocketIO for real-time WebSocket communication
- **Database**: JSON file-based storage (can be easily migrated to SQLite/PostgreSQL)

## 📁 Project Structure

```
dashBoard_webApp/
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── lib/          # Utilities
│   │   ├── App.tsx       # Main app component
│   │   └── main.tsx      # Entry point
│   ├── package.json
│   └── vite.config.ts
├── backend/              # Flask backend
│   ├── app.py           # Main Flask application
│   ├── requirements.txt # Python dependencies
│   └── db.json          # Database file (auto-created)
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download](https://www.python.org/)

### Installation

#### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

#### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Running the Application

#### Terminal 1 - Start Backend (Flask)

```bash
cd backend
python app.py
```

Backend will run on: `http://localhost:5000`

#### Terminal 2 - Start Frontend (React)

```bash
cd frontend
npm run dev
```

Frontend will run on: `http://localhost:3000`

## 🔌 API Endpoints

### REST API

- **GET /** - Health check
- **POST /api/data** - Create new sensor data entry
- **GET /api/data** - Get all data entries
- **GET /api/stats?type=<sensor_type>** - Get aggregated statistics

### WebSocket Events (Socket.IO)

- **connect** - Client connects
- **sensorData** - Send sensor data from device
- **driverUpdate** - Receive real-time driver updates
- **sendWarning** - Send warning to driver
- **warningReceived** - Receive warning confirmation

## 📊 Example API Usage

### Send Sensor Data (POST)

```bash
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{
    "deviceId": "driver-001",
    "type": "drowsiness",
    "values": {
      "eyeClosure": 0.85,
      "headPose": 15,
      "alertLevel": "high"
    }
  }'
```

### Get All Data (GET)

```bash
curl http://localhost:5000/api/data
```

### Get Statistics (GET)

```bash
curl http://localhost:5000/api/stats?type=drowsiness
```

## 🎨 Frontend Features

- **Dashboard Header** - Branding and navigation
- **Dashboard Controls** - Date range and driver filters
- **Safety Metrics** - Overall safety score and risk level
- **Safety Trend** - Line chart showing score improvement
- **Incidents Log** - Recent alerts and incidents
- **Driver Profile** - Driver statistics and information
- **Behavior Breakdown** - Pie chart and behavior metrics
- **Insurance Impact** - Premium calculations and recommendations

## 🔧 Development

### Frontend Development

```bash
cd frontend
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
```

### Backend Development

The Flask app runs in debug mode by default. The database file (`db.json`) will be automatically created on first run.

## 📝 Environment Variables

You can create a `.env` file in the backend directory:

```env
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

## 🐛 Troubleshooting

**Port already in use:**
- Change the port in `app.py` (line: `socketio.run(app, port=5000)`)
- Or change the port in `vite.config.ts` for frontend

**Module not found errors:**
- Make sure all dependencies are installed
- Delete `node_modules` and reinstall: `npm install`
- For Python: `pip install -r requirements.txt`

**CORS errors:**
- CORS is enabled by default in the Flask app
- Check that the frontend proxy is configured correctly in `vite.config.ts`

## 📄 License

Check the main project README for license information.

