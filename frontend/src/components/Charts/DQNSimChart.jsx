import React from 'react';
import { Cpu, TrendingUp } from 'lucide-react';

export const DQNSimChart = () => {
  return (
    <div className="p-5 rounded-3xl glass-panel space-y-4 shadow-xl border border-purple-500/30">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-purple-400" />
          <h3 className="text-xs font-bold text-white uppercase tracking-wider">DQN Reinforcement Learning Benchmark</h3>
        </div>
        <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 font-bold">
          SIMULATION EXTENSION
        </span>
      </div>

      <div className="space-y-3 text-xs">
        <div className="flex justify-between items-center text-slate-300">
          <span>Fixed-Time Baseline:</span>
          <span className="font-mono text-slate-400">1,440 veh/hr (42s wait)</span>
        </div>
        <div className="flex justify-between items-center text-cyan-300 font-bold">
          <span>Two-Stage Adaptive:</span>
          <span className="font-mono text-cyan-300">1,850 veh/hr (28s wait)</span>
        </div>
        <div className="flex justify-between items-center text-purple-300 font-bold">
          <span>DQN Projected RL:</span>
          <span className="font-mono text-purple-300">2,020 veh/hr (21s wait)</span>
        </div>

        <div className="w-full bg-slate-900 h-2 rounded-full overflow-hidden flex">
          <div className="bg-slate-700 h-full w-[45%]" title="Fixed" />
          <div className="bg-cyan-500 h-full w-[35%]" title="Adaptive" />
          <div className="bg-purple-500 h-full w-[20%]" title="DQN" />
        </div>
      </div>
    </div>
  );
};
