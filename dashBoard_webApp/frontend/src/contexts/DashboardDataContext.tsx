import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { io, Socket } from 'socket.io-client'

type RiskLevel = 'Low Risk' | 'Medium Risk' | 'High Risk'
type ConnectionStatus = 'connecting' | 'connected' | 'disconnected'

type IncidentSeverity = 'low' | 'medium' | 'high'

interface Incident {
  id: string
  type: string
  severity: IncidentSeverity
  timestamp: string
  relativeTime: string
}

interface TrendPoint {
  label: string
  score: number
}

interface BehaviorMetric {
  key: string
  label: string
  value: number
  icon: string
}

interface InsuranceInfo {
  premium: number
  discountPercent: number
  savings: number
}

interface DriverProfileData {
  name: string
  license: string
  hours: number
  trips: number
  avgScore: number
}

interface DashboardData {
  safetyScore: number
  riskLevel: RiskLevel
  discountPercent: number
  trend: TrendPoint[]
  incidents: Incident[]
  behaviorMetrics: BehaviorMetric[]
  insurance: InsuranceInfo
  driverProfile: DriverProfileData
  lastUpdated?: string
}

interface DashboardDataContextValue {
  data: DashboardData
  status: ConnectionStatus
}

const defaultTrend: TrendPoint[] = [
  { label: 'W1', score: 70 },
  { label: 'W2', score: 75 },
  { label: 'W3', score: 80 },
  { label: 'W4', score: 85 },
  { label: 'W5', score: 87 },
]

const defaultIncidents: Incident[] = [
  {
    id: '1',
    type: 'Drowsiness Alert',
    severity: 'high',
    timestamp: new Date().toISOString(),
    relativeTime: 'Just now',
  },
  {
    id: '2',
    type: 'Hard Braking',
    severity: 'medium',
    timestamp: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
    relativeTime: '1 hr ago',
  },
]

const defaultBehaviorMetrics: BehaviorMetric[] = [
  { key: 'attention', label: 'Attention Level', value: 92, icon: '👁️' },
  { key: 'stress', label: 'Stress Indicators', value: 18, icon: '🧘' },
  { key: 'compliance', label: 'Rule Compliance', value: 96, icon: '✅' },
  { key: 'smooth', label: 'Smooth Driving', value: 88, icon: '🚗' },
]

const defaultDashboardData: DashboardData = {
  safetyScore: 87,
  riskLevel: 'Low Risk',
  discountPercent: 8,
  trend: defaultTrend,
  incidents: defaultIncidents,
  behaviorMetrics: defaultBehaviorMetrics,
  insurance: {
    premium: 1245,
    discountPercent: 8,
    savings: 100,
  },
  driverProfile: {
    name: 'John Smith',
    license: 'License #DL123456',
    hours: 2847,
    trips: 384,
    avgScore: 83.2,
  },
  lastUpdated: undefined,
}

const DashboardDataContext = createContext<DashboardDataContextValue>({
  data: defaultDashboardData,
  status: 'connecting',
})

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:5000'

export function DashboardDataProvider({ children }: { children: React.ReactNode }) {
  const [data, setData] = useState<DashboardData>(defaultDashboardData)
  const [status, setStatus] = useState<ConnectionStatus>('connecting')

  useEffect(() => {
    let socket: Socket | null = null
    let isMounted = true

    async function loadInitialData() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/data`)
        if (!response.ok) return
        const entries = await response.json()

        if (Array.isArray(entries) && isMounted) {
          setData((prev) => entries.reduce(processEntry, prev))
        }
      } catch (error) {
        console.error('Failed to load initial data', error)
      }
    }

    loadInitialData()

    socket = io(API_BASE_URL, {
      transports: ['websocket'],
    })

    socket.on('connect', () => setStatus('connected'))
    socket.on('disconnect', () => setStatus('disconnected'))
    socket.on('driverUpdate', (entry) => {
      setData((prev) => processEntry(entry, prev))
    })

    return () => {
      isMounted = false
      socket?.disconnect()
    }
  }, [])

  const value = useMemo(() => ({ data, status }), [data, status])

  return <DashboardDataContext.Provider value={value}>{children}</DashboardDataContext.Provider>
}

export function useDashboardData() {
  return useContext(DashboardDataContext)
}

function processEntry(entry: any, previous: DashboardData): DashboardData {
  if (!entry || typeof entry !== 'object') {
    return previous
  }

  const timestamp = entry.timestamp ?? new Date().toISOString()
  const values = entry.values ?? {}
  let next: DashboardData = {
    ...previous,
    lastUpdated: timestamp,
  }

  switch (entry.type) {
    case 'safety':
    case 'safetyScore': {
      const rawScore = getNumericValue(values, ['score', 'value'])
      if (typeof rawScore === 'number') {
        const score = clamp(rawScore, 0, 100)
        next = {
          ...next,
          safetyScore: score,
          riskLevel: getRiskLevel(score),
          discountPercent:
            typeof values.discount === 'number'
              ? values.discount
              : next.discountPercent,
          trend: updateTrend(next.trend, score, timestamp),
        }
      }
      break
    }
    case 'incident': {
      const incident = toIncident(entry, values, timestamp)
      next = {
        ...next,
        incidents: [incident, ...next.incidents].slice(0, 8),
      }
      break
    }
    case 'behavior': {
      const updatedMetrics = next.behaviorMetrics.map((metric) => {
        const incomingValue = getNumericValue(values, [metric.key, metric.label])
        if (typeof incomingValue === 'number') {
          return { ...metric, value: clamp(incomingValue, 0, 100) }
        }
        return metric
      })
      next = { ...next, behaviorMetrics: updatedMetrics }
      break
    }
    case 'insurance': {
      const premium = getNumericValue(values, ['premium']) ?? next.insurance.premium
      const discountPercent =
        getNumericValue(values, ['discountPercent', 'discount']) ?? next.insurance.discountPercent
      const savings = getNumericValue(values, ['savings']) ?? Math.round((premium * discountPercent) / 100)
      next = {
        ...next,
        insurance: {
          premium,
          discountPercent,
          savings,
        },
      }
      break
    }
    case 'driverStats': {
      next = {
        ...next,
        driverProfile: {
          ...next.driverProfile,
          hours: getNumericValue(values, ['hours']) ?? next.driverProfile.hours,
          trips: getNumericValue(values, ['trips']) ?? next.driverProfile.trips,
          avgScore: getNumericValue(values, ['avgScore', 'averageScore']) ?? next.driverProfile.avgScore,
        },
      }
      break
    }
    default: {
      // Unknown event type, keep lastUpdated only
      break
    }
  }

  return next
}

function getNumericValue(obj: Record<string, any>, keys: string[]) {
  for (const key of keys) {
    const normalizedKey = key?.toString()
    if (normalizedKey && typeof obj[normalizedKey] === 'number') {
      return obj[normalizedKey]
    }
  }
  return undefined
}

function clamp(value: number, min: number, max: number) {
  return Math.max(min, Math.min(max, value))
}

function getRiskLevel(score: number): RiskLevel {
  if (score >= 85) return 'Low Risk'
  if (score >= 70) return 'Medium Risk'
  return 'High Risk'
}

function updateTrend(trend: TrendPoint[], score: number, timestamp: string): TrendPoint[] {
  const label = formatTrendLabel(timestamp)
  const next = [...trend, { label, score }]
  return next.slice(-7)
}

function formatTrendLabel(timestamp: string) {
  const date = new Date(timestamp)
  if (Number.isNaN(date.getTime())) return `T-${Date.now()}`
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function toIncident(entry: any, values: Record<string, any>, timestamp: string): Incident {
  const severity = (values.severity ?? entry.severity ?? 'medium').toLowerCase() as IncidentSeverity
  const type = values.type ?? values.incidentType ?? entry.type ?? 'Incident'

  return {
    id: entry.id ?? crypto.randomUUID(),
    type,
    severity: ['low', 'medium', 'high'].includes(severity) ? severity : 'medium',
    timestamp,
    relativeTime: formatRelativeTime(timestamp),
  }
}

function formatRelativeTime(timestamp: string) {
  const date = new Date(timestamp)
  if (Number.isNaN(date.getTime())) return 'Just now'

  const diffMs = Date.now() - date.getTime()
  const minute = 60 * 1000
  const hour = 60 * minute
  const day = 24 * hour

  if (diffMs < minute) return 'Just now'
  if (diffMs < hour) return `${Math.floor(diffMs / minute)} min ago`
  if (diffMs < day) return `${Math.floor(diffMs / hour)} hr ago`

  return date.toLocaleDateString()
}

