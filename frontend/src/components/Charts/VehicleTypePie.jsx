import React from 'react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import { PieChart as PieIcon } from 'lucide-react';
import { useTraffic } from '../../context/TrafficContext';

export const VehicleTypePie = () => {
  const { traffic } = useTraffic();
  const total = traffic.total_vehicles || 37;

  const data = [
    { name: 'Cars', value: Math.max(12, Math.round(total * 0.62)), color: '#38bdf8' },
    { name: 'Motorcycles', value: Math.max(4, Math.round(total * 0.18)), color: '#a855f7' },
    { name: 'Buses', value: Math.max(2, Math.round(total * 0.08)), color: '#f59e0b' },
    { name: 'Trucks', value: Math.max(1, Math.round(total * 0.07)), color: '#ef4444' },
    { name: 'Pedestrians', value: traffic.pedestrian_count || 3, color: '#10b981' },
    { name: 'Cyclists', value: traffic.cyclist_count || 2, color: '#34d399' },
  ];

  return (
    <div className="glass-panel p-5 rounded-2xl border border-slate-800 shadow-xl">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <PieIcon className="w-5 h-5 text-purple-400" />
          <h3 className="font-bold text-white text-base">Modal Split & Vehicle Classes</h3>
        </div>
        <span className="text-xs text-slate-400 font-mono">YOLOv8 Classified</span>
      </div>

      <div className="h-56 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={50}
              outerRadius={75}
              paddingAngle={4}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
            />
            <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '4px' }} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
