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
    <div className="min-h-screen bg-white dark:bg-[#0f2048] text-[#0f2048] dark:text-white">
      <DashboardHeader />
      
      <main className="p-6 lg:p-8 animate-fade-in bg-[#f9fafb] dark:bg-[#0f2048]">
        {/* Dashboard Controls */}
        <div className="animate-slide-up">
          <DashboardControls />
        </div>
        
        {/* Top Metrics Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6 animate-slide-up" style={{ animationDelay: '0.1s' }}>
          <SafetyMetrics />
          <div className="lg:col-span-2">
            <SafetyTrend />
          </div>
        </div>

        {/* Middle Section: Incidents and Profile */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6 animate-slide-up" style={{ animationDelay: '0.2s' }}>
          <div className="lg:col-span-2">
            <IncidentsLog />
          </div>
          <DriverProfile />
        </div>

        {/* Bottom Section: Behavior and Insurance */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-slide-up" style={{ animationDelay: '0.3s' }}>
          <BehaviorBreakdown />
          <InsuranceImpact />
        </div>
      </main>
    </div>
  )
}

