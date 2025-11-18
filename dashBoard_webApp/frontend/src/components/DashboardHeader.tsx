import { Shield, Bell } from 'lucide-react'

export default function DashboardHeader() {
  return (
    <header className="border-b-2 border-[#0f2048] bg-white sticky top-0 z-50 shadow-md">
      <div className="px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="relative">
              <div className="w-12 h-12 rounded-lg bg-[#0f2048] flex items-center justify-center shadow-lg transition-transform hover:scale-105">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-[#e10010] rounded-full border-2 border-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-[#0f2048] tracking-tight">
                DriveGuard AI
              </h1>
              <p className="text-xs text-[#6b7280] mt-0.5 font-medium">Insurance Risk Management Dashboard</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center gap-2 px-4 py-2 rounded-md bg-[#0f2048]/5 border border-[#0f2048]/20">
              <div className="w-2 h-2 bg-[#e10010] rounded-full" />
              <span className="text-sm font-semibold text-[#0f2048]">Active Monitoring</span>
            </div>
            <button className="relative p-2 rounded-md hover:bg-[#f5f7fa] transition-colors border border-transparent hover:border-[#e5e7eb]">
              <Bell className="w-5 h-5 text-[#0f2048]" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-[#e10010] rounded-full" />
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

