'use client'

import { Card } from '@/components/ui/card'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const data = [
  { week: 'W1', score: 70, fill: 'rgb(239, 68, 68)' },
  { week: 'W2', score: 75, fill: 'rgb(234, 179, 8)' },
  { week: 'W3', score: 80, fill: 'rgb(34, 197, 94)' },
  { week: 'W4', score: 85, fill: 'rgb(34, 197, 94)' },
  { week: 'W5', score: 87, fill: 'rgb(34, 197, 94)' },
]

export default function SafetyTrend() {
  return (
    <Card className="bg-card border-border p-6">
      <h3 className="text-lg font-semibold mb-4">Safety Score Trend</h3>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(100, 116, 139, 0.2)" />
          <XAxis 
            dataKey="week" 
            stroke="rgba(148, 163, 184, 0.6)"
            style={{ fontSize: '12px' }}
          />
          <YAxis 
            domain={[0, 100]}
            stroke="rgba(148, 163, 184, 0.6)"
            style={{ fontSize: '12px' }}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: 'rgba(15, 23, 42, 0.95)',
              border: '1px solid rgba(100, 116, 139, 0.3)',
              borderRadius: '8px',
            }}
            labelStyle={{ color: 'rgb(226, 232, 240)' }}
          />
          <Line 
            type="monotone" 
            dataKey="score" 
            stroke="rgb(100, 150, 255)" 
            strokeWidth={3}
            dot={{ fill: 'rgb(100, 150, 255)', r: 5 }}
            activeDot={{ r: 7 }}
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="mt-4 grid grid-cols-5 gap-2">
        {data.map((item) => (
          <div key={item.week} className="text-center text-xs">
            <p className="text-muted-foreground mb-1">{item.week}</p>
            <p className="font-semibold">{item.score}</p>
          </div>
        ))}
      </div>
    </Card>
  )
}
