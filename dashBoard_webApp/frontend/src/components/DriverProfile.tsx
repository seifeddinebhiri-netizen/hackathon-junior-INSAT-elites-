import { Card } from '@/components/ui/card'
import { Clock, MapPin, BarChart3 } from 'lucide-react'

export default function DriverProfile() {
  return (
    <Card className="bg-card border-border p-6">
      <h3 className="text-lg font-semibold mb-4">Driver Profile</h3>
      
      <div className="space-y-4">
        <div className="flex items-center gap-4 pb-4 border-b border-border">
          <div className="w-12 h-12 rounded-full bg-primary flex items-center justify-center">
            <span className="text-primary-foreground font-bold">JS</span>
          </div>
          <div>
            <p className="font-semibold">John Smith</p>
            <p className="text-xs text-muted-foreground">License #DL123456</p>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-start gap-3">
            <Clock className="w-4 h-4 mt-1 text-muted-foreground flex-shrink-0" />
            <div>
              <p className="text-xs text-muted-foreground">Total Driving Hours</p>
              <p className="text-lg font-semibold">2,847 hrs</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <MapPin className="w-4 h-4 mt-1 text-muted-foreground flex-shrink-0" />
            <div>
              <p className="text-xs text-muted-foreground">Trips Completed</p>
              <p className="text-lg font-semibold">384 trips</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <BarChart3 className="w-4 h-4 mt-1 text-muted-foreground flex-shrink-0" />
            <div>
              <p className="text-xs text-muted-foreground">Average Score</p>
              <p className="text-lg font-semibold">83.2 / 100</p>
            </div>
          </div>
        </div>
      </div>
    </Card>
  )
}

