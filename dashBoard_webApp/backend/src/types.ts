export type SensorPayload = {
  deviceId: string;
  timestamp: string;   // ISO string
  type: string;        // e.g. "accelerometer", "heartbeat", "blink"
  values: Record<string, number> | number | string;
}
