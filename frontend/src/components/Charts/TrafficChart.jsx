import React from 'react';
import { useTraffic } from '../../context/TrafficContext';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity } from 'lucide-react';

export const TrafficChart = () => {
  const { trafficHistory } = useTraffic();

  const mockHistory = [
    { time: '12:45', north: 12, south: 10, east: 5, west: 4, total: 31 },
    { time: '12:46', north: 14, south: 11, east: 6, west: 5, total: 36 },
    { time: '12:47', north: 16, south: 12, east: 7, west: 6, total: 41 },
    { time: '12:48', north: 15, south: 13, east: 6, west: 5, total: 39 },
    { time: '12:49', north: 14, south: 12, east: 6, west: 5, total: 37 },
  ];

  const data = trafficHistory.length > 0 ? trafficHistory : mockHistory;

  return (
    <div className="p-5 rounded-3xl glass-panel space-y-4 shadow-xl border border-slate-800">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <Activity className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">Real-Time Vehicle Density & Throughput Spectrum</h3>
        </div>
        <span className="text-[10px] text-slate-400 font-mono">Rolling Live Inflow Stream</span>
      </div>

      <div className="h-44 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="northGlow" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <XAxis dataKey="time" stroke="#64748b" fontSize={10} tickLine={false} />
            <YAxis stroke="#64748b" fontSize={10} tickLine={false} />
            <Tooltip
              contentStyle={{ background: '#090d16', border: '1px solid #06b6d4', borderRadius: '12px', fontSize: '11px' }}
            />
            <Area type="monotone" dataKey="north" name="North Approach" stroke="#06b6d4" strokeWidth={2} fill="url(#northGlow)" />
            <Area type="monotone" dataKey="south" name="South Approach" stroke="#8b5cf6" strokeWidth={2} fill="#8b5cf6" fillOpacity={0.2} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
