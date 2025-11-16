import { Server, Socket } from 'socket.io';

export const setupDriverSockets = (io: Server) => {
  io.on('connection', (socket: Socket) => {
    console.log('Dashboard connected for real-time updates');

    // Listen for incoming data from sensors (emitted from another client or API)
    socket.on('sensorData', (data: any) => {
      // Broadcast to all connected dashboards
      io.emit('driverUpdate', { ...data, timestamp: new Date() });
      console.log('Broadcasted update:', data);
    });

    // Handle driver warnings (e.g., send back to device)
    socket.on('sendWarning', (warning: string) => {
      socket.emit('warningReceived', { message: warning });
    });

    socket.on('disconnect', () => {
      console.log('Dashboard disconnected');
    });
  });
};
