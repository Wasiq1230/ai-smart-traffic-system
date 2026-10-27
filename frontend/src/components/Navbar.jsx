import React, { useState, useEffect } from 'react';
import { useTraffic } from '../context/TrafficContext';
import { 
  Zap, Radio, Clock, ShieldCheck, Siren, Activity,
  Sliders, LayoutDashboard, BarChart2, ChevronDown, Wifi, WifiOff,
  Sparkles, Maximize2, AlertTriangle
} from 'lucide-react';

export const Navbar = ({ currentPage, setCurrentPage }) => {
  const { traffic, signals, emergency, connectionStatus, clearEmergencyCorridor } = useTraffic();
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="h-16 border-b border-slate-800/80 bg-[#050811]/95 backdrop-blur-2xl sticky top-0 z-40 px-4 lg:px-8 flex items-center justify-between shadow-2xl">
      {/* Left: Brand Identity & Intersection Selector */}
      <div className="flex items-center space-x-6">
        <div className="flex items-center space-x-3 group cursor-pointer">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-500 via-indigo-600 to-purple-600 flex items-center justify-center text-white font-extrabold shadow-lg shadow-cyan-500/25 group-hover:scale-105 transition-transform">
            <Zap className="w-5 h-5 fill-current text-cyan-200" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="font-extrabold text-white text-base tracking-tight leading-none">
                NEURAL<span className="text-cyan-400">TRAFFIC</span> OS
              </h1>
              <span className="px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300 text-[10px] font-black tracking-widest border border-cyan-500/40 uppercase">
                PRO MAX
              </span>
            </div>
            <p className="text-[10px] text-slate-400 font-medium">Urban Adaptive Signal Intelligence & Vision Radar</p>
          </div>
        </div>

        {/* Intersection Quick Switcher */}
        <div className="hidden xl:flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-slate-900/80 border border-slate-800 text-xs">
          <Radio className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
          <span className="text-slate-400">Junction:</span>
          <span className="text-white font-bold">INT-001 (Broadway & 5th Ave)</span>
          <ChevronDown className="w-3.5 h-3.5 text-slate-500 cursor-pointer hover:text-cyan-300" />
        </div>
      </div>

      {/* Center: Live Navigation Tabs */}
      <nav className="hidden md:flex items-center gap-1.5 bg-slate-900/90 p-1.5 rounded-2xl border border-slate-800 shadow-inner">
        <button
          onClick={() => setCurrentPage('dashboard')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-extrabold transition-all ${
            currentPage === 'dashboard'
              ? 'bg-gradient-to-r from-cyan-600 to-indigo-600 text-white shadow-lg shadow-cyan-500/25 scale-105'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <LayoutDashboard className="w-4 h-4" />
          <span>Live Command</span>
        </button>

        <button
          onClick={() => setCurrentPage('analytics')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-extrabold transition-all ${
            currentPage === 'analytics'
              ? 'bg-gradient-to-r from-cyan-600 to-indigo-600 text-white shadow-lg shadow-cyan-500/25 scale-105'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <BarChart2 className="w-4 h-4" />
          <span>Forecasting & ESG</span>
        </button>

        <button
          onClick={() => setCurrentPage('settings')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-extrabold transition-all ${
            currentPage === 'settings'
              ? 'bg-gradient-to-r from-cyan-600 to-indigo-600 text-white shadow-lg shadow-cyan-500/25 scale-105'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <Sliders className="w-4 h-4" />
          <span>Safety Validator</span>
        </button>
      </nav>

      {/* Right: Subsystem Health & Telemetry Indicators */}
      <div className="flex items-center space-x-3">
        {/* Emergency Preemption Active Pill */}
        {emergency?.active && (
          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-rose-500/20 border border-rose-500/60 text-rose-300 text-xs font-bold animate-pulse">
            <Siren className="w-4 h-4 text-rose-400 animate-spin" />
            <span>EMERGENCY CORRIDOR ({emergency.lane?.toUpperCase()})</span>
            <button 
              onClick={clearEmergencyCorridor} 
              className="text-[10px] bg-rose-600 hover:bg-rose-500 text-white px-2 py-0.5 rounded ml-1"
            >
              Clear
            </button>
          </div>
        )}

        {/* Subsystem Health Pill */}
        <div className="hidden lg:flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-semibold">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Safety Locked (0 Conflicts)</span>
        </div>

        {/* WebSocket Status Indicator */}
        <div className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-xl border text-xs font-mono font-bold ${
          connectionStatus === 'live'
            ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
            : 'bg-amber-500/10 border-amber-500/30 text-amber-400 animate-pulse'
        }`}>
          {connectionStatus === 'live' ? <Wifi className="w-3.5 h-3.5" /> : <WifiOff className="w-3.5 h-3.5" />}
          <span>{connectionStatus === 'live' ? 'WS Live' : 'Reconnecting...'}</span>
        </div>

        {/* Live Mission Clock */}
        <div className="hidden sm:flex items-center space-x-1.5 text-xs text-slate-300 font-mono bg-slate-900/90 px-3 py-1.5 rounded-xl border border-slate-800 shadow-inner">
          <Clock className="w-3.5 h-3.5 text-cyan-400" />
          <span>{currentTime}</span>
        </div>
      </div>
    </header>
  );
};
