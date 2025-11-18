import { Card } from '@/components/ui/card'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts'
import { TrendingUp } from 'lucide-react'

const data = [
  { week: 'W1', score: 70 },
  { week: 'W2', score: 75 },
  { week: 'W3', score: 80 },
  { week: 'W4', score: 85 },
  { week: 'W5', score: 87 },
]

export default function SafetyTrend() {
  const trend = ((data[data.length - 1].score - data[0].score) / data[0].score * 100).toFixed(1)
  
  return (
    <Card className="bg-white border-2 border-[#e5e7eb] p-6 hover:shadow-lg transition-all duration-300">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-bold text-[#0f2048] mb-1">Safety Score Trend</h3>
          <p className="text-xs text-[#6b7280] font-medium">5-week performance overview</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-[#0f2048]/10 border-2 border-[#0f2048]/20">
          <TrendingUp className="w-4 h-4 text-[#0f2048]" />
          <span className="text-sm font-bold text-[#0f2048]">+{trend}%</span>
        </div>
      </div>
      
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="scoreGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#0f2048" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#0f2048" stopOpacity={0.05}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="week" 
            stroke="#6b7280"
            style={{ fontSize: '12px', fontWeight: 600 }}
            tickLine={false}
          />
          <YAxis 
            domain={[60, 100]}
            stroke="#6b7280"
            style={{ fontSize: '12px', fontWeight: 600 }}
            tickLine={false}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: '#ffffff',
              border: '2px solid #0f2048',
              borderRadius: '8px',
              boxShadow: '0 4px 6px -1px rgba(15, 32, 72, 0.2)',
            }}
            labelStyle={{ color: '#0f2048', fontWeight: 700 }}
            itemStyle={{ color: '#0f2048', fontWeight: 600 }}
          />
          <Area 
            type="monotone" 
            dataKey="score" 
            stroke="#0f2048" 
            strokeWidth={3}
            fill="url(#scoreGradient)"
            dot={{ fill: '#0f2048', r: 5, strokeWidth: 2, stroke: '#ffffff' }}
            activeDot={{ r: 7, strokeWidth: 2, stroke: '#0f2048', fill: '#e10010' }}
          />
        </AreaChart>
      </ResponsiveContainer>

      <div className="mt-6 grid grid-cols-5 gap-3">
        {data.map((item, index) => {
          const isLatest = index === data.length - 1
          return (
            <div 
              key={item.week} 
              className={`text-center p-3 rounded-md border-2 transition-all ${
                isLatest 
                  ? 'bg-[#0f2048] border-[#0f2048] text-white' 
                  : 'bg-[#f5f7fa] border-[#e5e7eb] text-[#0f2048] hover:border-[#0f2048]/50'
              }`}
            >
              <p className={`text-xs mb-2 font-semibold ${isLatest ? 'text-white/80' : 'text-[#6b7280]'}`}>{item.week}</p>
              <p className={`text-lg font-bold ${isLatest ? 'text-white' : 'text-[#0f2048]'}`}>{item.score}</p>
            </div>
          )
        })}
      </div>
    </Card>
  )
}

