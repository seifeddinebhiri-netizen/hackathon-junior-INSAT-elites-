import express, { Application, Request, Response } from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import dotenv from 'dotenv';
import driverRoutes from './routes/driverRoutes';
import { setupDriverSockets } from './sockets/driverSockets';

dotenv.config();  // Loads .env file

const app: Application = express();
app.use('/', driverRoutes);
const server = createServer(app);  // HTTP server for Socket.io
const io = new Server(server, { cors: { origin: "*" } });  // Enable CORS for Socket.io

const PORT = process.env.PORT || 3001;  // Backend on port 3001, frontend on 3000

setupDriverSockets(io);

app.use(cors());  // Allow requests from frontend
app.use(express.json());  // Parse JSON bodies

// Basic route to test backend
app.get('/', (req: Request, res: Response) => {
  res.send('Backend is running! Ready for real-time driver data.');
});

// Socket.io setup for real-time (detailed next)
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  socket.on('disconnect', () => console.log('Client disconnected'));
});

server.listen(PORT, () => {
  console.log(`Backend server listening on port ${PORT}`);
});
