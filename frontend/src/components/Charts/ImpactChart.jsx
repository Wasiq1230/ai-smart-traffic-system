import React from 'react';
import { Leaf, Zap, Clock, ShieldCheck } from 'lucide-react';

export const ImpactChart = () => {
  return (
    <div className="p-5 rounded-3xl glass-panel space-y-4 shadow-xl border border-emerald-500/30">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <Leaf className="w-4 h-4 text-emerald-400" />
          <h3 className="text-xs font-bold text-white uppercase tracking-wider">Environmental ESG Impact</h3>
        </div>
        <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">
          ESTIMATED EPA FORMULA
        </span>
      </div>

      <div className="space-y-3 text-xs">
        <div className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-center justify-between">
          <div>
            <span className="text-[10px] text-slate-400 block">CO₂ Reduced</span>
            <span className="text-base font-extrabold text-emerald-300 font-mono">142.8 kg</span>
          </div>
          <span className="text-[10px] text-emerald-400 font-semibold">-24.2% Emissions</span>
        </div>

        <div className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-center justify-between">
          <div>
            <span className="text-[10px] text-slate-400 block">Idle Fuel Saved</span>
            <span className="text-base font-extrabold text-cyan-300 font-mono">48.2 Liters</span>
          </div>
          <span className="text-[10px] text-cyan-400 font-semibold">Reduced Idling</span>
        </div>
      </div>
    </div>
  );
};
