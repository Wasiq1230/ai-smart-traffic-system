import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { Sparkles, TrendingUp, Cpu } from 'lucide-react';

export const PredictionChart = () => {
  const data = [
    { time: 'Now', current: 37, predicted: 37, upper: 37, lower: 37 },
    { time: '+5 min', current: null, predicted: 42, upper: 45, lower: 39 },
    { time: '+10 min', current: null, predicted: 48, upper: 53, lower: 43 },
    { time: '+15 min', current: null, predicted: 56, upper: 64, lower: 48 },
    { time: '+30 min', current: null, predicted: 38, upper: 47, lower: 29 },
  ];

  return (
    <div className="p-5 rounded-3xl glass-panel space-y-4 shadow-2xl border border-purple-500/30">
      <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <div className="p-1.5 rounded-lg bg-purple-500/20 text-purple-400">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-extrabold text-white">AI MULTI-HORIZON TRAFFIC FORECAST</h3>
            <p className="text-[10px] text-slate-400">Sequential LSTM Model (v2.1-hybrid) • 94.2% R² Test Accuracy</p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <span className="px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 font-mono text-[10px] font-bold">
            95% Confidence Bounds
          </span>
        </div>
      </div>

      {/* 4 Horizon Metric Chips */}
      <div className="grid grid-cols-4 gap-2 text-center text-xs">
        <div className="p-2 rounded-2xl bg-slate-900/90 border border-slate-800">
          <span className="text-[10px] text-slate-400 uppercase font-bold block">+5 Min</span>
          <span className="text-base font-extrabold text-cyan-300 font-mono">42 veh</span>
          <span className="text-[9px] text-emerald-400 block font-semibold">+13% Steady</span>
        </div>
        <div className="p-2 rounded-2xl bg-slate-900/90 border border-slate-800">
          <span className="text-[10px] text-slate-400 uppercase font-bold block">+10 Min</span>
          <span className="text-base font-extrabold text-indigo-300 font-mono">48 veh</span>
          <span className="text-[9px] text-amber-400 block font-semibold">+30% Inflow</span>
        </div>
        <div className="p-2 rounded-2xl bg-slate-900/90 border border-purple-500/40 bg-purple-950/20">
          <span className="text-[10px] text-purple-300 uppercase font-bold block">+15 Min Surge</span>
          <span className="text-base font-extrabold text-purple-300 font-mono">56 veh</span>
          <span className="text-[9px] text-rose-400 block font-semibold">Peak Demand</span>
        </div>
        <div className="p-2 rounded-2xl bg-slate-900/90 border border-slate-800">
          <span className="text-[10px] text-slate-400 uppercase font-bold block">+30 Min</span>
          <span className="text-base font-extrabold text-emerald-300 font-mono">38 veh</span>
          <span className="text-[9px] text-slate-400 block font-semibold">Normalized</span>
        </div>
      </div>

      {/* Forecasting Chart Area */}
      <div className="h-44 w-full pt-1">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="forecastGlow" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="confidenceGlow" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.2}/>
                <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <XAxis dataKey="time" stroke="#64748b" fontSize={10} tickLine={false} />
            <YAxis stroke="#64748b" fontSize={10} tickLine={false} domain={[20, 70]} />
            <Tooltip
              contentStyle={{ background: '#090d16', border: '1px solid #8b5cf6', borderRadius: '12px', fontSize: '11px' }}
              labelStyle={{ color: '#ffffff', fontWeight: 'bold' }}
            />
            <Area type="monotone" dataKey="upper" stroke="none" fill="#06b6d4" fillOpacity={0.15} />
            <Area type="monotone" dataKey="predicted" stroke="#8b5cf6" strokeWidth={3} fillOpacity={1} fill="url(#forecastGlow)" />
            <Area type="monotone" dataKey="current" stroke="#06b6d4" strokeWidth={3} fill="#06b6d4" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
