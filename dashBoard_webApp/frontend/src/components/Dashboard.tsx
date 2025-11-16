import DashboardHeader from './DashboardHeader'
import SafetyMetrics from './SafetyMetrics'
import SafetyTrend from './SafetyTrend'
import IncidentsLog from './IncidentsLog'
import DriverProfile from './DriverProfile'
import BehaviorBreakdown from './BehaviorBreakdown'
import InsuranceImpact from './InsuranceImpact'
import DashboardControls from './DashboardControls'

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

