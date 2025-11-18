import { Card } from '@/components/ui/card'
import { TrendingUp, AlertCircle, DollarSign, Sparkles } from 'lucide-react'

export default function InsuranceImpact() {
  const savings = 100
  const discount = 8
  
  return (
    <Card className="bg-white border-2 border-[#e5e7eb] p-6 hover:shadow-lg transition-all duration-300">
      <div className="flex items-center gap-2 mb-6">
        <div className="p-2 rounded-md bg-[#0f2048] border-2 border-[#0f2048]">
          <DollarSign className="w-5 h-5 text-white" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-[#0f2048]">Insurance Impact</h3>
          <p className="text-xs text-[#6b7280] font-medium">Premium savings & recommendations</p>
        </div>
      </div>

      <div className="space-y-6">
        {/* Current Premium */}
        <div className="pb-6 border-b-2 border-[#e5e7eb]">
          <p className="text-xs text-[#6b7280] mb-3 font-bold uppercase tracking-wide">Current Annual Premium</p>
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-bold text-[#0f2048]">$1,245</span>
            <span className="text-sm text-[#6b7280] font-medium">/year</span>
          </div>
        </div>

        {/* Estimated with Discount */}
        <div className="pb-6 border-b-2 border-[#e5e7eb]">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles className="w-4 h-4 text-[#0f2048]" />
            <p className="text-xs text-[#6b7280] font-bold uppercase tracking-wide">With Safety Discount ({discount}%)</p>
          </div>
          <div className="flex items-baseline gap-2 mb-2">
            <span className="text-4xl font-bold text-[#0f2048]">$1,145</span>
            <span className="text-sm text-[#0f2048]/70 font-medium">/year</span>
          </div>
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#0f2048]/10 border-2 border-[#0f2048]/20">
            <TrendingUp className="w-4 h-4 text-[#0f2048]" />
            <span className="text-sm font-bold text-[#0f2048]">Save ${savings}/year</span>
          </div>
        </div>

        {/* Policy Recommendation */}
        <div className="bg-[#0f2048]/5 border-2 border-[#0f2048]/20 rounded-md p-4 hover:border-[#0f2048]/40 transition-all">
          <div className="flex gap-3">
            <div className="p-2 rounded-md bg-[#0f2048] border-2 border-[#0f2048]">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <div className="flex-1">
              <p className="font-bold text-sm mb-1.5 text-[#0f2048]">Policy Recommendation</p>
              <p className="text-xs text-[#6b7280] leading-relaxed font-medium">
                Maintain your excellent driving behavior to keep your discount and qualify for premium membership benefits.
              </p>
            </div>
          </div>
        </div>

        {/* Warnings */}
        <div className="bg-[#e10010]/5 border-2 border-[#e10010]/20 rounded-md p-4 hover:border-[#e10010]/40 transition-all">
          <div className="flex gap-3">
            <div className="p-2 rounded-md bg-[#e10010] border-2 border-[#e10010]">
              <AlertCircle className="w-5 h-5 text-white" />
            </div>
            <div className="flex-1">
              <p className="font-bold text-sm mb-1.5 text-[#e10010]">Safety Alert</p>
              <p className="text-xs text-[#6b7280] leading-relaxed font-medium">
                Reduce drowsiness incidents to maintain your Low Risk status.
              </p>
            </div>
          </div>
        </div>
      </div>
    </Card>
  )
}

