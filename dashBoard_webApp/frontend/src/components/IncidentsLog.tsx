import { Card } from '@/components/ui/card'
import { AlertCircle, Zap, Activity, Eye, Flame, Clock } from 'lucide-react'

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
      return {
        bg: 'bg-[#e10010]/10 hover:bg-[#e10010]/15',
        text: 'text-[#e10010]',
        border: 'border-[#e10010]',
        badge: 'bg-[#e10010] text-white border-[#e10010]',
        dot: 'bg-[#e10010]'
      }
    case 'medium':
      return {
        bg: 'bg-[#f59e0b]/10 hover:bg-[#f59e0b]/15',
        text: 'text-[#f59e0b]',
        border: 'border-[#f59e0b]',
        badge: 'bg-[#f59e0b] text-white border-[#f59e0b]',
        dot: 'bg-[#f59e0b]'
      }
    case 'low':
      return {
        bg: 'bg-[#0f2048]/10 hover:bg-[#0f2048]/15',
        text: 'text-[#0f2048]',
        border: 'border-[#0f2048]',
        badge: 'bg-[#0f2048] text-white border-[#0f2048]',
        dot: 'bg-[#0f2048]'
      }
    default:
      return {
        bg: 'bg-[#f5f7fa]',
        text: 'text-[#6b7280]',
        border: 'border-[#e5e7eb]',
        badge: 'bg-white',
        dot: 'bg-[#6b7280]'
      }
  }
}

export default function IncidentsLog() {
  return (
    <Card className="bg-white border-2 border-[#e5e7eb] p-6 hover:shadow-lg transition-all duration-300">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-bold text-[#0f2048] mb-1">Recent Incidents & Alerts</h3>
          <p className="text-xs text-[#6b7280] font-medium">Real-time monitoring updates</p>
        </div>
        <div className="px-3 py-1.5 rounded-md bg-[#e10010]/10 border-2 border-[#e10010]/20">
          <span className="text-xs font-bold text-[#e10010]">{incidents.filter(i => i.severity === 'high').length} Critical</span>
        </div>
      </div>
      
      <div className="space-y-3">
        {incidents.map((incident) => {
          const Icon = incident.icon
          const colors = getSeverityColor(incident.severity)
          return (
            <div
              key={incident.id}
              className={`flex items-center gap-4 p-4 rounded-md border-2 transition-all duration-200 cursor-pointer ${colors.bg} ${colors.border} ${colors.text} group hover:shadow-md`}
            >
              <div className={`p-2.5 rounded-md ${colors.bg} border-2 ${colors.border} group-hover:scale-110 transition-transform`}>
                <Icon className="w-5 h-5" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <p className="font-bold text-sm">{incident.type}</p>
                  <div className={`w-2 h-2 rounded-full ${colors.dot}`} />
                </div>
                <div className="flex items-center gap-1.5 text-xs opacity-80">
                  <Clock className="w-3 h-3" />
                  <span className="font-medium">{incident.timestamp}</span>
                </div>
              </div>
              <span className={`text-xs font-bold px-3 py-1.5 rounded-md border-2 ${colors.badge} whitespace-nowrap`}>
                {incident.severity.charAt(0).toUpperCase() + incident.severity.slice(1)}
              </span>
            </div>
          )
        })}
      </div>
    </Card>
  )
}

