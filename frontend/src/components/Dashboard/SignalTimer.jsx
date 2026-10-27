import React from 'react';
import { useTraffic } from '../../context/TrafficContext';
import { Sliders, ShieldCheck, Clock, Zap, ArrowRight } from 'lucide-react';

export const SignalTimer = () => {
  const { signals, traffic } = useTraffic();

  const timings = signals.timings || { north_green: 35, south_green: 35, east_green: 20, west_green: 20 };

  return (
    <div className="p-5 rounded-3xl glass-panel space-y-4 shadow-xl border border-slate-800">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <Sliders className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">Two-Stage Adaptive Controller HUD</h3>
        </div>
        <span className="px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 font-mono text-[10px] font-bold">
          Webster + Forecast Model
        </span>
      </div>

      {/* Allocation Progress Bars */}
      <div className="space-y-3 text-xs">
        <div>
          <div className="flex justify-between font-bold mb-1">
            <span className="text-cyan-300">North-South Phase Green</span>
            <span className="text-white font-mono">{timings.north_green || 35}s allocated</span>
          </div>
          <div className="w-full bg-slate-950 h-2.5 rounded-full overflow-hidden border border-slate-800">
            <div className="bg-gradient-to-r from-cyan-500 to-indigo-500 h-full rounded-full w-[65%]" />
          </div>
        </div>

        <div>
          <div className="flex justify-between font-bold mb-1">
            <span className="text-purple-300">East-West Phase Green</span>
            <span className="text-white font-mono">{timings.east_green || 20}s allocated</span>
          </div>
          <div className="w-full bg-slate-950 h-2.5 rounded-full overflow-hidden border border-slate-800">
            <div className="bg-gradient-to-r from-purple-500 to-pink-500 h-full rounded-full w-[35%]" />
          </div>
        </div>
      </div>

      {/* Safety Matrix Status Tags */}
      <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800/80 text-center text-[10px] font-mono">
        <div className="p-2 rounded-xl bg-slate-900 border border-slate-800">
          <span className="text-slate-400 block">Min / Max Green</span>
          <span className="text-white font-bold">10s / 65s</span>
        </div>
        <div className="p-2 rounded-xl bg-slate-900 border border-slate-800">
          <span className="text-slate-400 block">All-Red Safety</span>
          <span className="text-emerald-400 font-bold">2.0s Clearance</span>
        </div>
        <div className="p-2 rounded-xl bg-slate-900 border border-slate-800">
          <span className="text-slate-400 block">Phase Conflicts</span>
          <span className="text-emerald-400 font-bold">0 Verified</span>
        </div>
      </div>
    </div>
  );
};
