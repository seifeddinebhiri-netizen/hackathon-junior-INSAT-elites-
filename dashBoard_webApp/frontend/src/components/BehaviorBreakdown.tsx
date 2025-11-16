import { Card } from '@/components/ui/card'
import { PieChart, Pie, Cell, Legend, ResponsiveContainer } from 'recharts'

const behaviorData = [
  { name: 'Excellent', value: 45, color: 'rgb(34, 197, 94)' },
  { name: 'Good', value: 35, color: 'rgb(59, 130, 246)' },
  { name: 'Fair', value: 15, color: 'rgb(234, 179, 8)' },
  { name: 'Poor', value: 5, color: 'rgb(239, 68, 68)' },
]

const metrics = [
  { label: 'Attention Level', value: 92, color: 'text-green-400' },
  { label: 'Stress Indicators', value: 18, color: 'text-blue-400' },
  { label: 'Rule Compliance', value: 96, color: 'text-green-400' },
  { label: 'Smooth Driving', value: 88, color: 'text-green-400' },
]

export default function BehaviorBreakdown() {
  return (
    <Card className="bg-card border-border p-6">
      <h3 className="text-lg font-semibold mb-6">Behavior Analysis</h3>

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
                label={({ name, value }) => `${name} ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {behaviorData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Legend 
                verticalAlign="bottom" 
                height={36}
                wrapperStyle={{ paddingTop: '20px' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Metrics */}
        <div className="space-y-4 flex flex-col justify-center">
          {metrics.map((metric, idx) => (
            <div key={idx}>
              <div className="flex justify-between items-center mb-2">
                <p className="text-sm font-medium">{metric.label}</p>
                <p className={`font-semibold ${metric.color}`}>{metric.value}%</p>
              </div>
              <div className="h-2 rounded-full bg-input overflow-hidden">
                <div
                  className={`h-full rounded-full ${
                    metric.value >= 90 ? 'bg-green-500' :
                    metric.value >= 70 ? 'bg-blue-500' :
                    metric.value >= 50 ? 'bg-yellow-500' :
                    'bg-red-500'
                  }`}
                  style={{ width: `${metric.value}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </Card>
  )
}

