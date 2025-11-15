'use client'

import { Card } from '@/components/ui/card'
import { AlertCircle, Zap, Activity, Eye, Flame } from 'lucide-react'

const incidents = [
  {
    id: 1,
    type: 'Drowsiness Alert',
    severity: 'high',
    timestamp: '2 minutes ago',
    icon: Activity,
  },
  {
    id: 2,
    type: 'Hard Braking',
    severity: 'medium',
    timestamp: '1 hour ago',
    icon: Zap,
  },
  {
    id: 3,
    type: 'Speeding Warning',
    severity: 'medium',
    timestamp: '3 hours ago',
    icon: AlertCircle,
  },
  {
    id: 4,
    type: 'Distraction Detected',
    severity: 'high',
    timestamp: '5 hours ago',
    icon: Eye,
  },
  {
    id: 5,
    type: 'Aggressive Acceleration',
    severity: 'low',
    timestamp: '8 hours ago',
    icon: Flame,
  },
]

const getSeverityColor = (severity: string) => {
  switch (severity) {
    case 'high':
      return 'bg-red-500/10 text-red-400 border-red-500/20'
    case 'medium':
      return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20'
    case 'low':
      return 'bg-blue-500/10 text-blue-400 border-blue-500/20'
    default:
      return ''
  }
}

export default function IncidentsLog() {
  return (
    <Card className="bg-card border-border p-6">
      <h3 className="text-lg font-semibold mb-4">Recent Incidents & Alerts</h3>
      
      <div className="space-y-3">
        {incidents.map((incident) => {
          const Icon = incident.icon
          return (
            <div
              key={incident.id}
              className={`flex items-center gap-4 p-3 rounded-lg border ${getSeverityColor(incident.severity)}`}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="font-medium text-sm">{incident.type}</p>
                <p className="text-xs text-muted-foreground">{incident.timestamp}</p>
              </div>
              <span className="text-xs font-semibold px-2 py-1 rounded bg-background/50">
                {incident.severity.charAt(0).toUpperCase() + incident.severity.slice(1)}
              </span>
            </div>
          )
        })}
      </div>
    </Card>
  )
}
