import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Download, Settings } from 'lucide-react'

export default function DashboardControls() {
  const [dateRange, setDateRange] = useState('5-weeks')

  return (
    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
      <div className="flex gap-2 w-full sm:w-auto">
        <select 
          value={dateRange}
          onChange={(e) => setDateRange(e.target.value)}
          className="px-4 py-2 rounded-lg bg-input border border-border text-foreground text-sm"
        >
          <option value="1-week">Last 1 Week</option>
          <option value="5-weeks">Last 5 Weeks</option>
          <option value="3-months">Last 3 Months</option>
          <option value="1-year">Last Year</option>
        </select>
        
        <select className="px-4 py-2 rounded-lg bg-input border border-border text-foreground text-sm">
          <option>Select Driver</option>
          <option>John Smith</option>
          <option>All Drivers</option>
        </select>
      </div>

      <div className="flex gap-2 w-full sm:w-auto">
        <Button variant="outline" size="sm" className="flex items-center gap-2">
          <Download className="w-4 h-4" />
          Export
        </Button>
        <Button variant="outline" size="sm" className="flex items-center gap-2">
          <Settings className="w-4 h-4" />
          Settings
        </Button>
      </div>
    </div>
  )
}

