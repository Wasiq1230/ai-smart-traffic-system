import React, { useState } from 'react';
import { useTraffic } from '../../context/TrafficContext';
import { 
  Play, Siren, AlertTriangle, ShieldCheck, Flame, 
  RotateCcw, Sparkles, CheckCircle2, Car
} from 'lucide-react';

export const ScenarioSwitcher = () => {
  const { triggerEmergencyCorridor, clearEmergencyCorridor, simulateAccident, simulateViolation, advancePhase } = useTraffic();
  const [activeScenario, setActiveScenario] = useState('normal');

  const runScenario = (name) => {
    setActiveScenario(name);
    if (name === 'ambulance') {
      triggerEmergencyCorridor('north', 'ambulance');
    } else if (name === 'accident') {
      simulateAccident('east');
    } else if (name === 'violation') {
      simulateViolation('north');
    } else if (name === 'rush_hour') {
      advancePhase();
    } else {
      clearEmergencyCorridor();
    }
  };

  const scenarios = [
    { id: 'normal', label: '1. Normal Flow', icon: Car, color: 'hover:border-cyan-500/50 hover:bg-cyan-500/10 text-cyan-300' },
    { id: 'rush_hour', label: '2. Rush Hour Spike', icon: Flame, color: 'hover:border-amber-500/50 hover:bg-amber-500/10 text-amber-300' },
    { id: 'ambulance', label: '3. Ambulance Corridor', icon: Siren, color: 'hover:border-rose-500/50 hover:bg-rose-500/10 text-rose-300' },
    { id: 'accident', label: '4. Road Accident', icon: AlertTriangle, color: 'hover:border-yellow-500/50 hover:bg-yellow-500/10 text-yellow-300' },
    { id: 'violation', label: '5. Violation / ANPR', icon: ShieldCheck, color: 'hover:border-purple-500/50 hover:bg-purple-500/10 text-purple-300' }
  ];

  return (
    <div className="p-4 rounded-3xl bg-gradient-to-r from-slate-900/90 via-[#0c1527] to-slate-900/90 border border-cyan-500/30 backdrop-blur-xl shadow-2xl flex flex-col lg:flex-row lg:items-center justify-between gap-4">
      <div className="flex items-center space-x-3">
        <div className="p-2.5 rounded-2xl bg-gradient-to-br from-cyan-500 to-indigo-600 text-slate-950 font-bold shadow-lg shadow-cyan-500/20">
          <Sparkles className="w-4 h-4 text-white" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-black text-white uppercase tracking-wider">Interactive Scenario Studio</span>
            <span className="px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-mono text-[10px] font-bold">1-Click Live Test</span>
          </div>
          <p className="text-[11px] text-slate-400">Trigger live dynamic response across AI Vision, Adaptive Signals & Safety Validator</p>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {scenarios.map((sc) => {
          const Icon = sc.icon;
          const isActive = activeScenario === sc.id;
          return (
            <button
              key={sc.id}
              onClick={() => runScenario(sc.id)}
              className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-2xl text-xs font-bold transition-all transform active:scale-95 border ${
                isActive
                  ? 'bg-cyan-600 text-white border-cyan-400 shadow-lg shadow-cyan-600/30 scale-105'
                  : `bg-slate-900/80 border-slate-800 ${sc.color}`
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{sc.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
