# Quick Start Guide

## 🚀 Installation & Running

### Step 1: Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Step 2: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Note:** If you don't have `pip`, use `pip3` instead.

### Step 3: Run the Application

**Terminal 1 - Start Flask Backend:**
```bash
cd backend
python app.py
```
Backend runs on: `http://localhost:5000`

**Terminal 2 - Start React Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:3000`

## ✅ Verify Installation

1. Open `http://localhost:3000` in your browser
2. You should see the DriveGuard AI Dashboard
3. Check backend: `http://localhost:5000` should return JSON with status message

## 🔧 Troubleshooting

**Python not found:**
- Make sure Python 3.8+ is installed
- Try `python3` instead of `python`

**npm not found:**
- Install Node.js from https://nodejs.org/
- Restart your terminal after installation

**Port already in use:**
- Change port in `backend/app.py` (line with `port=5000`)
- Change port in `frontend/vite.config.ts` (line with `port: 3000`)

## 📝 Next Steps

- The dashboard currently shows hardcoded data
- Connect your sensor devices to send data via POST `/api/data` or Socket.IO
- Real-time updates will appear automatically via WebSocket

