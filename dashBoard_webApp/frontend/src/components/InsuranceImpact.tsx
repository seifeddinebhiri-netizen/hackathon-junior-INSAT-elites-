import { Card } from '@/components/ui/card'
import { TrendingUp, AlertCircle } from 'lucide-react'

export default function InsuranceImpact() {
  return (
    <Card className="bg-card border-border p-6">
      <h3 className="text-lg font-semibold mb-6">Insurance Impact</h3>

      <div className="space-y-6">
        {/* Current Premium */}
        <div className="pb-6 border-b border-border">
          <p className="text-xs text-muted-foreground mb-2">Current Annual Premium</p>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold">$1,245</span>
            <span className="text-sm text-muted-foreground">/year</span>
          </div>
        </div>

        {/* Estimated with Discount */}
        <div className="pb-6 border-b border-border">
          <p className="text-xs text-muted-foreground mb-2">With Safety Discount (8%)</p>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-green-400">$1,145</span>
            <span className="text-sm text-green-400">Save $100/year</span>
          </div>
        </div>

        {/* Policy Recommendation */}
        <div className="bg-primary/10 border border-primary/20 rounded-lg p-4">
          <div className="flex gap-3">
            <TrendingUp className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-sm mb-1">Policy Recommendation</p>
              <p className="text-xs text-muted-foreground">
                Maintain your excellent driving behavior to keep your discount and qualify for premium membership benefits.
              </p>
            </div>
          </div>
        </div>

        {/* Warnings */}
        <div className="bg-warning/10 border border-warning/20 rounded-lg p-4">
          <div className="flex gap-3">
            <AlertCircle className="w-5 h-5 text-warning flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-sm mb-1">Safety Alert</p>
              <p className="text-xs text-muted-foreground">
                Reduce drowsiness incidents to maintain your Low Risk status.
              </p>
            </div>
          </div>
        </div>
      </div>
    </Card>
  )
}

