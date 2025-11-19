import { useEffect, useState } from "react";
import { io } from "socket.io-client";

// Define your type BEFORE using it
interface DriverUpdate {
  heartRate?: number;
  facialExpression?: string;
  audioLevel?: number;
  drowsiness?: boolean;
  intoxication?: boolean;
  anger?: boolean;
  // Add any other fields your backend sends
}

useEffect(() => {
  const socket = io("http://localhost:5000");
  
  const [driverData, setDriverData] = useState<DriverUpdate | null>(null);
  
  const handleDriverUpdate = (data: DriverUpdate) => {
    setDriverData(data);  // Update state with incoming data
  };
  
  socket.on('driverUpdate', handleDriverUpdate);
  
  return () => {
    socket.off('driverUpdate', handleDriverUpdate);
    socket.disconnect();
  };
}, []);
