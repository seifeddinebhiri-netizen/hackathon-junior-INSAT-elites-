import { Card } from '@/components/ui/card'
import { PieChart, Pie, Cell, Legend, ResponsiveContainer, Tooltip } from 'recharts'
import { Brain } from 'lucide-react'

const behaviorData = [
  { name: 'Excellent', value: 45, color: '#0f2048' },
  { name: 'Good', value: 35, color: '#1e40af' },
  { name: 'Fair', value: 15, color: '#f59e0b' },
  { name: 'Poor', value: 5, color: '#e10010' },
]

const metrics = [
  { label: 'Attention Level', value: 92, color: 'text-[#0f2048]', icon: '👁️' },
  { label: 'Stress Indicators', value: 18, color: 'text-[#0f2048]', icon: '🧘' },
  { label: 'Rule Compliance', value: 96, color: 'text-[#0f2048]', icon: '✅' },
  { label: 'Smooth Driving', value: 88, color: 'text-[#0f2048]', icon: '🚗' },
]

const RADIAN = Math.PI / 180
const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: any) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5
  const x = cx + radius * Math.cos(-midAngle * RADIAN)
  const y = cy + radius * Math.sin(-midAngle * RADIAN)

  return (
    <text 
      x={x} 
      y={y} 
      fill="white" 
      textAnchor={x > cx ? 'start' : 'end'} 
      dominantBaseline="central"
      fontSize={12}
      fontWeight={600}
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  )
}

export default function BehaviorBreakdown() {
  return (
    <Card className="bg-white border-2 border-[#e5e7eb] p-6 hover:shadow-lg transition-all duration-300">
      <div className="flex items-center gap-2 mb-6">
        <div className="p-2 rounded-md bg-[#0f2048] border-2 border-[#0f2048]">
          <Brain className="w-5 h-5 text-white" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-[#0f2048]">Behavior Analysis</h3>
          <p className="text-xs text-[#6b7280] font-medium">Driving pattern breakdown</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {/* Pie Chart */}
        <div>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={behaviorData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={renderCustomizedLabel}
                outerRadius={90}
                fill="#8884d8"
                dataKey="value"
                stroke="#ffffff"
                strokeWidth={3}
              >
                {behaviorData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{
                  backgroundColor: '#ffffff',
                  border: '2px solid #0f2048',
                  borderRadius: '8px',
                }}
                labelStyle={{ color: '#0f2048', fontWeight: 700 }}
                itemStyle={{ color: '#0f2048', fontWeight: 600 }}
              />
              <Legend 
                verticalAlign="bottom" 
                height={36}
                wrapperStyle={{ paddingTop: '20px', fontSize: '12px', fontWeight: 600 }}
                iconType="circle"
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Metrics */}
        <div className="space-y-4 flex flex-col justify-center">
          {metrics.map((metric, idx) => {
            const barColor = 
              metric.value >= 90 ? 'bg-[#0f2048]' :
              metric.value >= 70 ? 'bg-[#1e40af]' :
              metric.value >= 50 ? 'bg-[#f59e0b]' :
              'bg-[#e10010]'
            
            return (
              <div key={idx} className="group">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-base">{metric.icon}</span>
                    <p className="text-sm font-bold text-[#0f2048]">{metric.label}</p>
                  </div>
                  <p className={`font-bold text-lg ${metric.color}`}>{metric.value}%</p>
                </div>
                <div className="h-3 rounded-full bg-[#f5f7fa] overflow-hidden border border-[#e5e7eb]">
                  <div
                    className={`h-full rounded-full ${barColor} transition-all duration-1000 ease-out`}
                    style={{ width: `${metric.value}%` }}
                  />
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </Card>
  )
}

