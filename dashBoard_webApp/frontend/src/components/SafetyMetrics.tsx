import { Card } from '@/components/ui/card'
import { TrendingUp } from 'lucide-react'

export default function SafetyMetrics() {
  const safetyScore = 87
  const riskLevel = 'Low Risk'
  const discount = '+8%'

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'Low Risk':
        return 'bg-green-500/20 text-green-400 border-green-500/30'
      case 'Medium Risk':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
      case 'High Risk':
        return 'bg-red-500/20 text-red-400 border-red-500/30'
      default:
        return ''
    }
  }

  return (
    <Card className="bg-card border-border p-6 flex flex-col gap-6">
      {/* Safety Score */}
      <div>
        <p className="text-muted-foreground text-sm mb-3">Safety Score</p>
        <div className="flex items-baseline gap-2">
          <div className="text-5xl font-bold text-primary">{safetyScore}</div>
          <span className="text-muted-foreground text-xl">/100</span>
        </div>
      </div>

      {/* Risk Category */}
      <div>
        <p className="text-muted-foreground text-sm mb-3">Risk Category</p>
        <div className={`inline-block px-4 py-2 rounded-lg border ${getRiskColor(riskLevel)}`}>
          <span className="font-semibold text-sm">{riskLevel}</span>
        </div>
      </div>

      {/* Insurance Bonus */}
      <div>
        <p className="text-muted-foreground text-sm mb-3">Potential Bonus</p>
        <div className="flex items-center gap-2">
          <div className="text-3xl font-bold text-green-400">{discount}</div>
          <div className="flex items-center gap-1 text-green-400 text-sm">
            <TrendingUp className="w-4 h-4" />
            Discount
          </div>
        </div>
      </div>

      {/* Status */}
      <div className="pt-4 border-t border-border">
        <p className="text-sm text-green-400">✓ Eligible for premium reduction</p>
      </div>
    </Card>
  )
}

