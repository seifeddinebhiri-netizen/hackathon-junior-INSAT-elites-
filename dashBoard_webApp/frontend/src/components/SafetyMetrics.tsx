import { Card } from '@/components/ui/card'
import { TrendingUp, CheckCircle2, Award } from 'lucide-react'

export default function SafetyMetrics() {
  const safetyScore = 87
  const riskLevel = 'Low Risk'
  const discount = '+8%'
  const circumference = 2 * Math.PI * 45
  const offset = circumference - (safetyScore / 100) * circumference

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'Low Risk':
        return 'bg-[#0f2048]/10 text-[#0f2048] border-[#0f2048]/30'
      case 'Medium Risk':
        return 'bg-[#f59e0b]/10 text-[#f59e0b] border-[#f59e0b]/30'
      case 'High Risk':
        return 'bg-[#e10010]/10 text-[#e10010] border-[#e10010]/30'
      default:
        return ''
    }
  }

  return (
    <Card className="bg-white border-2 border-[#e5e7eb] p-6 flex flex-col gap-6 hover:shadow-lg transition-all duration-300">
      {/* Safety Score with Circular Progress */}
      <div className="flex flex-col items-center">
        <p className="text-[#6b7280] text-sm mb-4 font-semibold uppercase tracking-wide">Overall Safety Score</p>
        <div className="relative w-32 h-32 mb-4">
          <svg className="transform -rotate-90 w-32 h-32">
            <circle
              cx="64"
              cy="64"
              r="45"
              stroke="#e5e7eb"
              strokeWidth="8"
              fill="none"
            />
            <circle
              cx="64"
              cy="64"
              r="45"
              stroke="#0f2048"
              strokeWidth="8"
              fill="none"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              strokeLinecap="round"
              className="transition-all duration-1000 ease-out"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <div className="text-4xl font-bold text-[#0f2048]">{safetyScore}</div>
            <span className="text-xs text-[#6b7280]">/100</span>
          </div>
        </div>
      </div>

      {/* Risk Category */}
      <div className="space-y-2">
        <p className="text-[#6b7280] text-sm font-semibold uppercase tracking-wide">Risk Assessment</p>
        <div className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-md border-2 ${getRiskColor(riskLevel)} transition-all`}>
          <div className="w-2 h-2 rounded-full bg-current" />
          <span className="font-bold text-sm">{riskLevel}</span>
        </div>
      </div>

      {/* Insurance Bonus */}
      <div className="bg-[#0f2048]/5 border-2 border-[#0f2048]/20 rounded-md p-4 space-y-2">
        <div className="flex items-center gap-2 text-[#0f2048] text-sm font-semibold">
          <Award className="w-4 h-4" />
          <span>Insurance Discount</span>
        </div>
        <div className="flex items-baseline gap-2">
          <div className="text-3xl font-bold text-[#0f2048]">{discount}</div>
          <div className="flex items-center gap-1 text-[#0f2048]/70 text-sm font-medium">
            <TrendingUp className="w-4 h-4" />
            <span>Premium Reduction</span>
          </div>
        </div>
      </div>

      {/* Status */}
      <div className="pt-4 border-t-2 border-[#e5e7eb] flex items-center gap-2">
        <CheckCircle2 className="w-5 h-5 text-[#0f2048] flex-shrink-0" />
        <p className="text-sm text-[#0f2048] font-semibold">Eligible for premium reduction</p>
      </div>
    </Card>
  )
}

