import { useEffect } from 'react';
import { io } from 'socket.io-client';

useEffect(() => {
  const socket = io('http://localhost:5000');
  
  const handleDriverUpdate = (data) => {
    // Update your state with new data
  };
  
  socket.on('driverUpdate', handleDriverUpdate);
  
  return () => {
    socket.off('driverUpdate', handleDriverUpdate);
    socket.disconnect();
  };
}, []);
