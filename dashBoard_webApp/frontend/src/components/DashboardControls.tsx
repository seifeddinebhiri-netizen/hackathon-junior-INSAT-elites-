import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Download, Calendar, User } from 'lucide-react'

export default function DashboardControls() {
  const [dateRange, setDateRange] = useState('5-weeks')

  return (
    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8 p-4 rounded-md bg-white border-2 border-[#e5e7eb]">
      <div className="flex flex-wrap gap-3 w-full sm:w-auto">
        <div className="relative flex-1 sm:flex-initial min-w-[160px]">
          <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-[#6b7280] pointer-events-none" />
          <select 
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-md bg-[#f9fafb] hover:bg-white border-2 border-[#e5e7eb] hover:border-[#0f2048] text-[#0f2048] text-sm font-semibold transition-all focus:outline-none focus:ring-2 focus:ring-[#0f2048]/20 focus:border-[#0f2048] cursor-pointer appearance-none bg-[url('data:image/svg+xml;charset=UTF-8,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%230f2048%22 stroke-width=%222%22><polyline points=%226 9 12 15 18 9%22></polyline></svg>')] bg-[length:16px] bg-[right_0.75rem_center] bg-no-repeat"
          >
            <option value="1-week">Last 1 Week</option>
            <option value="5-weeks">Last 5 Weeks</option>
            <option value="3-months">Last 3 Months</option>
            <option value="1-year">Last Year</option>
          </select>
        </div>
        
        <div className="relative flex-1 sm:flex-initial min-w-[160px]">
          <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-[#6b7280] pointer-events-none" />
          <select className="w-full pl-10 pr-4 py-2.5 rounded-md bg-[#f9fafb] hover:bg-white border-2 border-[#e5e7eb] hover:border-[#0f2048] text-[#0f2048] text-sm font-semibold transition-all focus:outline-none focus:ring-2 focus:ring-[#0f2048]/20 focus:border-[#0f2048] cursor-pointer appearance-none bg-[url('data:image/svg+xml;charset=UTF-8,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%230f2048%22 stroke-width=%222%22><polyline points=%226 9 12 15 18 9%22></polyline></svg>')] bg-[length:16px] bg-[right_0.75rem_center] bg-no-repeat">
            <option>Select Driver</option>
            <option>John Smith</option>
            <option>All Drivers</option>
          </select>
        </div>
      </div>

      <div className="flex gap-2 w-full sm:w-auto">
        <Button 
          variant="outline" 
          size="sm" 
          className="flex items-center gap-2 hover:bg-[#0f2048] hover:text-white hover:border-[#0f2048] border-2 border-[#e5e7eb] text-[#0f2048] font-semibold transition-all"
        >
          <Download className="w-4 h-4" />
          Export
        </Button>
      </div>
    </div>
  )
}

