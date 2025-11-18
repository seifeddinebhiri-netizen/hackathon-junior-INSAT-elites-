import { Card } from '@/components/ui/card'
import { Clock, MapPin, BarChart3, User, Award } from 'lucide-react'

export default function DriverProfile() {
  return (
    <Card className="bg-white border-2 border-[#e5e7eb] p-6 hover:shadow-lg transition-all duration-300">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-bold text-[#0f2048]">Driver Profile</h3>
        <Award className="w-5 h-5 text-[#0f2048]" />
      </div>
      
      <div className="space-y-6">
        <div className="flex items-center gap-4 pb-6 border-b-2 border-[#e5e7eb]">
          <div className="relative">
            <div className="w-16 h-16 rounded-full bg-[#0f2048] flex items-center justify-center shadow-lg">
              <User className="w-8 h-8 text-white" />
            </div>
            <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-[#e10010] rounded-full border-2 border-white flex items-center justify-center">
              <div className="w-2 h-2 bg-white rounded-full" />
            </div>
          </div>
          <div className="flex-1">
            <p className="font-bold text-lg mb-1 text-[#0f2048]">John Smith</p>
            <p className="text-xs text-[#6b7280] font-mono font-medium">License #DL123456</p>
            <div className="mt-2 inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-[#0f2048]/10 border-2 border-[#0f2048]/20">
              <div className="w-2 h-2 bg-[#0f2048] rounded-full" />
              <span className="text-xs font-bold text-[#0f2048]">Verified</span>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <div className="group p-4 rounded-md bg-[#f5f7fa] hover:bg-[#e5e7eb] border-2 border-[#e5e7eb] hover:border-[#0f2048]/30 transition-all">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-md bg-[#0f2048] border-2 border-[#0f2048] group-hover:scale-110 transition-transform">
                <Clock className="w-5 h-5 text-white" />
              </div>
              <div className="flex-1">
                <p className="text-xs text-[#6b7280] mb-1 font-semibold uppercase tracking-wide">Total Driving Hours</p>
                <p className="text-2xl font-bold text-[#0f2048]">2,847</p>
                <p className="text-xs text-[#6b7280] mt-0.5 font-medium">hours</p>
              </div>
            </div>
          </div>

          <div className="group p-4 rounded-md bg-[#f5f7fa] hover:bg-[#e5e7eb] border-2 border-[#e5e7eb] hover:border-[#0f2048]/30 transition-all">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-md bg-[#0f2048] border-2 border-[#0f2048] group-hover:scale-110 transition-transform">
                <MapPin className="w-5 h-5 text-white" />
              </div>
              <div className="flex-1">
                <p className="text-xs text-[#6b7280] mb-1 font-semibold uppercase tracking-wide">Trips Completed</p>
                <p className="text-2xl font-bold text-[#0f2048]">384</p>
                <p className="text-xs text-[#6b7280] mt-0.5 font-medium">trips</p>
              </div>
            </div>
          </div>

          <div className="group p-4 rounded-md bg-[#f5f7fa] hover:bg-[#e5e7eb] border-2 border-[#e5e7eb] hover:border-[#0f2048]/30 transition-all">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-md bg-[#0f2048] border-2 border-[#0f2048] group-hover:scale-110 transition-transform">
                <BarChart3 className="w-5 h-5 text-white" />
              </div>
              <div className="flex-1">
                <p className="text-xs text-[#6b7280] mb-1 font-semibold uppercase tracking-wide">Average Score</p>
                <p className="text-2xl font-bold text-[#0f2048]">83.2</p>
                <p className="text-xs text-[#6b7280] mt-0.5 font-medium">/ 100</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>
  )
}

