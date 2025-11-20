import { io, Socket } from "socket.io-client";

// Define your type BEFORE using it
export interface DriverUpdate {
  heartRate?: number;
  facialExpression?: string;
  audioLevel?: number;
  drowsiness?: boolean;
  intoxication?: boolean;
  anger?: boolean;
  // Add any other fields your backend sends
}

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:5000'

/**
 * Creates a socket connection to the backend
 * @returns Socket instance
 */
export function createSocket(): Socket {
  return io(API_BASE_URL, {
    transports: ['websocket'],
  })
}
