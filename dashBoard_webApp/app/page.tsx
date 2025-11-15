import DashboardHeader from '@/components/dashboard-header'
import SafetyMetrics from '@/components/safety-metrics'
import SafetyTrend from '@/components/safety-trend'
import IncidentsLog from '@/components/incidents-log'
import DriverProfile from '@/components/driver-profile'
import BehaviorBreakdown from '@/components/behavior-breakdown'
import InsuranceImpact from '@/components/insurance-impact'
import DashboardControls from '@/components/dashboard-controls'

export const metadata = {
  title: 'DriveGuard AI Dashboard',
  description: 'Professional driver monitoring and insurance analytics dashboard',
}

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <DashboardHeader />
      
      <main className="p-6 lg:p-8">
        {/* Dashboard Controls */}
        <DashboardControls />
        
        {/* Top Metrics Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <SafetyMetrics />
          <div className="lg:col-span-2">
            <SafetyTrend />
          </div>
        </div>

        {/* Middle Section: Incidents and Profile */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div className="lg:col-span-2">
            <IncidentsLog />
          </div>
          <DriverProfile />
        </div>

        {/* Bottom Section: Behavior and Insurance */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <BehaviorBreakdown />
          <InsuranceImpact />
        </div>
      </main>
    </div>
  )
}
