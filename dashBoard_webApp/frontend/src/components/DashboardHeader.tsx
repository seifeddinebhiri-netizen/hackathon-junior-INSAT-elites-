import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Shield, Bell, Settings } from 'lucide-react'

export default function DashboardHeader() {
  const [showNotifications, setShowNotifications] = useState(false)
  const navigate = useNavigate()

  return (
    <header className="border-b-2 border-[#0f2048] dark:border-white bg-white dark:bg-[#0f2048] sticky top-0 z-50 shadow-md">
      <div className="px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="relative">
              <div className="w-12 h-12 rounded-lg bg-[#0f2048] dark:bg-white flex items-center justify-center shadow-lg transition-transform hover:scale-105">
                <Shield className="w-6 h-6 text-white dark:text-[#0f2048]" />
              </div>
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-[#e10010] rounded-full border-2 border-white dark:border-[#0f2048]" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-[#0f2048] dark:text-white tracking-tight">
                DriveGuard AI
              </h1>
              <p className="text-xs text-[#6b7280] dark:text-[#9ca3af] mt-0.5 font-medium">
                Insurance Risk Management Dashboard
              </p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center gap-2 px-4 py-2 rounded-md bg-[#0f2048]/5 dark:bg-white/10 border border-[#0f2048]/20 dark:border-white/20">
              <div className="w-2 h-2 bg-[#e10010] rounded-full" />
              <span className="text-sm font-semibold text-[#0f2048] dark:text-white">
                Active Monitoring
              </span>
            </div>
            <div className="flex items-center gap-3">
              {/* Notifications Icon */}
              <div className="relative">
                <button
                  onClick={() => setShowNotifications(!showNotifications)}
                  className="relative w-10 h-10 rounded-full bg-[#0f2048] dark:bg-white flex items-center justify-center hover:bg-[#0f2048]/90 dark:hover:bg-white/90 transition-colors"
                >
                  <Bell className="text-white dark:text-[#0f2048] w-6 h-6" />
                  <span className="absolute top-0 right-0 w-4 h-4 bg-[#e10010] text-white text-xs flex items-center justify-center rounded-full">
                    3
                  </span>
                </button>

                {showNotifications && (
                  <div className="absolute right-0 mt-2 w-64 bg-white dark:bg-[#1a2d5a] border-2 border-[#e5e7eb] dark:border-[#2d3f6b] rounded-lg shadow-lg p-4 z-50">
                    <p className="text-sm font-semibold mb-2 text-[#0f2048] dark:text-white">Notifications</p>
                    <ul className="space-y-2">
                      <li className="text-sm text-[#0f2048] dark:text-white">New incident detected</li>
                      <li className="text-sm text-[#0f2048] dark:text-white">Driver profile updated</li>
                      <li className="text-sm text-[#0f2048] dark:text-white">System maintenance scheduled</li>
                    </ul>
                  </div>
                )}
              </div>

              {/* Settings Icon */}
              <button
                onClick={() => navigate('/settings')}
                className="w-10 h-10 rounded-full bg-[#0f2048] dark:bg-white flex items-center justify-center hover:bg-[#0f2048]/90 dark:hover:bg-white/90 transition-colors"
              >
                <Settings className="text-white dark:text-[#0f2048] w-6 h-6" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

