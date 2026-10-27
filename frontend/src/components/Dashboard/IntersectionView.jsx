import React, { useState, useEffect } from 'react';
import { useTraffic } from '../../context/TrafficContext';
import { Siren, AlertTriangle, ShieldCheck, Sparkles, Navigation, Zap } from 'lucide-react';

export const IntersectionView = () => {
  const { traffic, signals, emergency, triggerEmergencyCorridor, clearEmergencyCorridor, simulateAccident } = useTraffic();

  const { lanes } = traffic;
  const sig = signals.signals || { north: 'GREEN', south: 'GREEN', east: 'RED', west: 'RED' };
  const remTime = signals.remaining_seconds || 24;

  // Animated tick for vehicle particle motion
  const [tick, setTick] = useState(0);
  useEffect(() => {
    const interval = setInterval(() => setTick((t) => (t + 1) % 100), 100);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative w-full aspect-square max-w-[640px] mx-auto bg-[#070c18] rounded-3xl p-4 border border-cyan-500/30 shadow-[0_0_50px_rgba(6,182,212,0.15)] overflow-hidden flex items-center justify-center select-none backdrop-blur-2xl">
      {/* Background Radar Grid Sweep */}
      <div className="absolute inset-0 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:16px_16px] opacity-40 pointer-events-none" />

      {/* SVG Canvas */}
      <svg viewBox="0 0 600 600" className="w-full h-full relative z-10">
        <defs>
          <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
          <filter id="glow-red" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        {/* 4 Corner City Blocks (Urban Grass/Building Areas) */}
        <rect x="10" y="10" width="200" height="200" fill="#0c1626" stroke="#1e293b" strokeWidth="2" rx="20" />
        <rect x="390" y="10" width="200" height="200" fill="#0c1626" stroke="#1e293b" strokeWidth="2" rx="20" />
        <rect x="10" y="390" width="200" height="200" fill="#0c1626" stroke="#1e293b" strokeWidth="2" rx="20" />
        <rect x="390" y="390" width="200" height="200" fill="#0c1626" stroke="#1e293b" strokeWidth="2" rx="20" />

        {/* Asphalt Roads */}
        {/* North-South Road */}
        <rect x="210" y="0" width="180" height="600" fill="#111827" />
        {/* East-West Road */}
        <rect x="0" y="210" width="600" height="180" fill="#111827" />

        {/* Center Intersection Junction Box */}
        <rect x="210" y="210" width="180" height="180" fill="#161f33" stroke="#334155" strokeWidth="1" />

        {/* Emergency Preemption Priority Overlay Strip */}
        {emergency?.active && emergency.lane && (
          <rect
            x={emergency.lane === 'north' || emergency.lane === 'south' ? 210 : (emergency.lane === 'west' ? 0 : 390)}
            y={emergency.lane === 'north' ? 0 : (emergency.lane === 'south' ? 390 : 210)}
            width={emergency.lane === 'north' || emergency.lane === 'south' ? 180 : 210}
            height={emergency.lane === 'north' || emergency.lane === 'south' ? 210 : 180}
            fill="rgba(239, 68, 68, 0.3)"
            stroke="#ef4444"
            strokeWidth="3"
            strokeDasharray="8 6"
            className="animate-pulse"
          />
        )}

        {/* Road Dividers & Lane Dashed Yellow Markings */}
        <line x1="300" y1="0" x2="300" y2="200" stroke="#f59e0b" strokeWidth="3" strokeDasharray="12 10" />
        <line x1="300" y1="400" x2="300" y2="600" stroke="#f59e0b" strokeWidth="3" strokeDasharray="12 10" />
        <line x1="0" y1="300" x2="200" y2="300" stroke="#f59e0b" strokeWidth="3" strokeDasharray="12 10" />
        <line x1="400" y1="300" x2="600" y2="300" stroke="#f59e0b" strokeWidth="3" strokeDasharray="12 10" />

        {/* Stop Lines */}
        <line x1="210" y1="206" x2="390" y2="206" stroke="#f8fafc" strokeWidth="5" />
        <line x1="210" y1="394" x2="390" y2="394" stroke="#f8fafc" strokeWidth="5" />
        <line x1="206" y1="210" x2="206" y2="390" stroke="#f8fafc" strokeWidth="5" />
        <line x1="394" y1="210" x2="394" y2="390" stroke="#f8fafc" strokeWidth="5" />

        {/* Pedestrian Zebra Crossings */}
        {[-70, -50, -30, -10, 10, 30, 50, 70].map((offset, i) => (
          <React.Fragment key={i}>
            <rect x={300 + offset - 6} y="180" width="12" height="20" fill="#94a3b8" rx="2" />
            <rect x={300 + offset - 6} y="400" width="12" height="20" fill="#94a3b8" rx="2" />
            <rect x="180" y={300 + offset - 6} width="20" height="12" fill="#94a3b8" rx="2" />
            <rect x="400" y={300 + offset - 6} width="20" height="12" fill="#94a3b8" rx="2" />
          </React.Fragment>
        ))}

        {/* Animated Moving Vehicles Particles */}
        {/* Northbound Flow */}
        {[0, 1, 2, 3].map((i) => {
          const y = ((tick * 4 + i * 90) % 200);
          return (
            <g key={`v-north-${i}`} transform={`translate(250, ${sig.north === 'GREEN' ? y : Math.min(160, 60 + i * 35)})`}>
              <rect x="0" y="0" width="20" height="30" rx="6" fill={i === 0 && emergency?.active ? '#ef4444' : '#06b6d4'} stroke="#ffffff" strokeWidth="1.5" />
              <rect x="4" y="4" width="12" height="6" rx="1" fill="#020617" />
            </g>
          );
        })}

        {/* Southbound Flow */}
        {[0, 1, 2, 3].map((i) => {
          const y = 600 - ((tick * 4 + i * 90) % 200);
          return (
            <g key={`v-south-${i}`} transform={`translate(330, ${sig.south === 'GREEN' ? y : Math.max(410, 540 - i * 35)})`}>
              <rect x="0" y="0" width="20" height="30" rx="6" fill="#8b5cf6" stroke="#ffffff" strokeWidth="1.5" />
              <rect x="4" y="20" width="12" height="6" rx="1" fill="#020617" />
            </g>
          );
        })}

        {/* Westbound Flow */}
        {[0, 1, 2].map((i) => {
          const x = ((tick * 3 + i * 110) % 200);
          return (
            <g key={`v-west-${i}`} transform={`translate(${sig.west === 'GREEN' ? x : Math.min(160, 50 + i * 40)}, 330)`}>
              <rect x="0" y="0" width="30" height="20" rx="6" fill="#f59e0b" stroke="#ffffff" strokeWidth="1.5" />
              <rect x="20" y="4" width="6" height="12" rx="1" fill="#020617" />
            </g>
          );
        })}

        {/* Eastbound Flow */}
        {[0, 1, 2].map((i) => {
          const x = 600 - ((tick * 3 + i * 110) % 200);
          return (
            <g key={`v-east-${i}`} transform={`translate(${sig.east === 'GREEN' ? x : Math.max(410, 550 - i * 40)}, 250)`}>
              <rect x="0" y="0" width="30" height="20" rx="6" fill="#10b981" stroke="#ffffff" strokeWidth="1.5" />
              <rect x="4" y="4" width="6" height="12" rx="1" fill="#020617" />
            </g>
          );
        })}
      </svg>

      {/* 4 DYNAMIC SIGNAL HEAD OVERLAYS */}

      {/* NORTH SIGNAL */}
      <div className="absolute top-3 left-1/2 -translate-x-1/2 flex flex-col items-center bg-[#0a1020]/95 border border-cyan-500/40 px-3.5 py-1.5 rounded-2xl shadow-2xl backdrop-blur-xl z-20">
        <span className="text-[10px] font-extrabold tracking-wider text-cyan-300 uppercase">NORTH APPROACH</span>
        <div className="flex items-center space-x-2 mt-1">
          <div className="flex items-center space-x-1 bg-black/90 px-2 py-1 rounded-full border border-slate-800">
            <div className={`w-3 h-3 rounded-full transition-all duration-300 ${sig.north === 'RED' ? 'bg-red-500 glow-red scale-125' : 'bg-red-950 opacity-30'}`} />
            <div className={`w-3 h-3 rounded-full transition-all duration-300 ${sig.north === 'YELLOW' ? 'bg-amber-400 glow-yellow scale-125' : 'bg-amber-950 opacity-30'}`} />
            <div className={`w-3 h-3 rounded-full transition-all duration-300 ${sig.north === 'GREEN' ? 'bg-emerald-400 glow-green scale-125' : 'bg-emerald-950 opacity-30'}`} />
          </div>
          <span className="font-mono text-xs font-black text-white bg-slate-800 px-2 py-0.5 rounded border border-slate-700">
            {sig.north === 'GREEN' || sig.north === 'YELLOW' ? `${remTime}s` : 'WAIT'}
          </span>
        </div>
      </div>

      {/* SOUTH SIGNAL */}
      <div className="absolute bottom-3 left-1/2 -translate-x-1/2 flex flex-col items-center bg-[#0a1020]/95 border border-purple-500/40 px-3.5 py-1.5 rounded-2xl shadow-2xl backdrop-blur-xl z-20">
        <div className="flex items-center space-x-2 mb-1">
          <div className="flex items-center space-x-1 bg-black/90 px-2 py-1 rounded-full border border-slate-800">
            <div className={`w-3 h-3 rounded-full transition-all duration-300 ${sig.south === 'RED' ? 'bg-red-500 glow-red scale-125' : 'bg-red-950 opacity-30'}`} />
            <div className={`w-3 h-3 rounded-full transition-all duration-300 ${sig.south === 'YELLOW' ? 'bg-amber-400 glow-yellow scale-125' : 'bg-amber-950 opacity-30'}`} />
            <div className={`w-3 h-3 rounded-full transition-all duration-300 ${sig.south === 'GREEN' ? 'bg-emerald-400 glow-green scale-125' : 'bg-emerald-950 opacity-30'}`} />
          </div>
          <span className="font-mono text-xs font-black text-white bg-slate-800 px-2 py-0.5 rounded border border-slate-700">
            {sig.south === 'GREEN' || sig.south === 'YELLOW' ? `${remTime}s` : 'WAIT'}
          </span>
        </div>
        <span className="text-[10px] font-extrabold tracking-wider text-purple-300 uppercase">SOUTH APPROACH</span>
      </div>

      {/* WEST SIGNAL */}
      <div className="absolute left-3 top-1/2 -translate-y-1/2 flex flex-col items-center bg-[#0a1020]/95 border border-amber-500/40 px-2 py-2 rounded-2xl shadow-2xl backdrop-blur-xl z-20">
        <span className="text-[9px] font-extrabold tracking-wider text-amber-300 uppercase">WEST</span>
        <div className="flex flex-col items-center space-y-1 my-1 bg-black/90 p-1.5 rounded-full border border-slate-800">
          <div className={`w-2.5 h-2.5 rounded-full transition-all duration-300 ${sig.west === 'RED' ? 'bg-red-500 glow-red scale-125' : 'bg-red-950 opacity-30'}`} />
          <div className={`w-2.5 h-2.5 rounded-full transition-all duration-300 ${sig.west === 'YELLOW' ? 'bg-amber-400 glow-yellow scale-125' : 'bg-amber-950 opacity-30'}`} />
          <div className={`w-2.5 h-2.5 rounded-full transition-all duration-300 ${sig.west === 'GREEN' ? 'bg-emerald-400 glow-green scale-125' : 'bg-emerald-950 opacity-30'}`} />
        </div>
        <span className="font-mono text-[10px] font-bold text-white bg-slate-800 px-1 py-0.5 rounded">
          {sig.west === 'GREEN' || sig.west === 'YELLOW' ? `${remTime}s` : 'WAIT'}
        </span>
      </div>

      {/* EAST SIGNAL */}
      <div className="absolute right-3 top-1/2 -translate-y-1/2 flex flex-col items-center bg-[#0a1020]/95 border border-emerald-500/40 px-2 py-2 rounded-2xl shadow-2xl backdrop-blur-xl z-20">
        <span className="text-[9px] font-extrabold tracking-wider text-emerald-300 uppercase">EAST</span>
        <div className="flex flex-col items-center space-y-1 my-1 bg-black/90 p-1.5 rounded-full border border-slate-800">
          <div className={`w-2.5 h-2.5 rounded-full transition-all duration-300 ${sig.east === 'RED' ? 'bg-red-500 glow-red scale-125' : 'bg-red-950 opacity-30'}`} />
          <div className={`w-2.5 h-2.5 rounded-full transition-all duration-300 ${sig.east === 'YELLOW' ? 'bg-amber-400 glow-yellow scale-125' : 'bg-amber-950 opacity-30'}`} />
          <div className={`w-2.5 h-2.5 rounded-full transition-all duration-300 ${sig.east === 'GREEN' ? 'bg-emerald-400 glow-green scale-125' : 'bg-emerald-950 opacity-30'}`} />
        </div>
        <span className="font-mono text-[10px] font-bold text-white bg-slate-800 px-1 py-0.5 rounded">
          {sig.east === 'GREEN' || sig.east === 'YELLOW' ? `${remTime}s` : 'WAIT'}
        </span>
      </div>

      {/* CENTER JUNCTION STATUS HUD */}
      <div className="absolute inset-0 m-auto w-36 h-20 pointer-events-none flex flex-col items-center justify-center bg-[#050811]/90 border border-cyan-500/50 rounded-2xl backdrop-blur-2xl shadow-[0_0_30px_rgba(6,182,212,0.3)] z-30">
        <span className="text-[9px] uppercase tracking-widest text-cyan-400 font-extrabold flex items-center space-x-1">
          <Zap className="w-3 h-3 fill-current text-cyan-400" />
          <span>PHASE {signals.current_phase || 1}</span>
        </span>
        <span className="text-xs font-black text-white text-center leading-tight mt-0.5">
          {signals.override_active ? 'EMERGENCY PREEMPTION' : (signals.phase_name?.split(' ')[0] || 'North-South')}
        </span>
        <span className="text-[10px] font-mono text-emerald-400 font-bold mt-0.5">
          {signals.safety_status || 'SAFETY LOCKED'}
        </span>
      </div>
    </div>
  );
};
