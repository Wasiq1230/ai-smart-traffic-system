import React from 'react';
import { useTraffic } from '../../context/TrafficContext';
import { Car, Activity, Gauge, AlertCircle, Shield, TrendingUp, Users, Zap } from 'lucide-react';

export const VehicleCounter = () => {
  const { traffic, signals } = useTraffic();

  const total = traffic.total_vehicles || 37;
  const avgSpeed = traffic.average_speed_kmh || 34.6;
  const congestion = traffic.overall_congestion || 'MEDIUM';
  const pedestrians = traffic.pedestrian_count || 3;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* 1. Vehicles Served Live */}
      <div className="p-5 rounded-3xl glass-panel hover:border-cyan-500/40 transition-all duration-200 group relative overflow-hidden shadow-xl">
        <div className="absolute top-0 right-0 w-24 h-24 bg-cyan-500/10 rounded-full blur-xl pointer-events-none" />
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Active Intersection Load</span>
          <div className="p-2 rounded-xl bg-cyan-500/15 text-cyan-400 group-hover:scale-110 transition-transform">
            <Car className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-3xl font-extrabold text-white font-mono tracking-tight">{total}</span>
          <span className="text-xs font-semibold text-cyan-400 font-mono">Vehicles in Grid</span>
        </div>
        <div className="flex items-center justify-between text-[11px] text-slate-400 mt-2 pt-2 border-t border-slate-800/80">
          <span>PCU Factor: <strong className="text-white">41.8</strong></span>
          <span className="text-emerald-400 font-semibold">1,850 veh/hr rate</span>
        </div>
      </div>

      {/* 2. Congestion Index */}
      <div className="p-5 rounded-3xl glass-panel hover:border-amber-500/40 transition-all duration-200 group relative overflow-hidden shadow-xl">
        <div className="absolute top-0 right-0 w-24 h-24 bg-amber-500/10 rounded-full blur-xl pointer-events-none" />
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Congestion Level</span>
          <div className={`p-2 rounded-xl text-white group-hover:scale-110 transition-transform ${
            congestion === 'LOW' ? 'bg-emerald-500/20 text-emerald-400' :
            congestion === 'HIGH' ? 'bg-amber-500/20 text-amber-400' : 'bg-purple-500/20 text-purple-400'
          }`}>
            <Activity className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className={`text-2xl font-extrabold tracking-tight ${
            congestion === 'LOW' ? 'text-emerald-400' :
            congestion === 'HIGH' ? 'text-amber-400' : 'text-purple-300'
          }`}>
            {congestion} LEVEL
          </span>
          <span className="text-xs text-slate-400">Queue Index: 0.58</span>
        </div>
        <div className="flex items-center justify-between text-[11px] text-slate-400 mt-2 pt-2 border-t border-slate-800/80">
          <span>Northbound Peak</span>
          <span className="text-amber-300 font-semibold">Stage 2 Anticipated</span>
        </div>
      </div>

      {/* 3. Average Speed Velocity */}
      <div className="p-5 rounded-3xl glass-panel hover:border-emerald-500/40 transition-all duration-200 group relative overflow-hidden shadow-xl">
        <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-500/10 rounded-full blur-xl pointer-events-none" />
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Arterial Flow Velocity</span>
          <div className="p-2 rounded-xl bg-emerald-500/15 text-emerald-400 group-hover:scale-110 transition-transform">
            <Gauge className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-3xl font-extrabold text-white font-mono tracking-tight">{avgSpeed}</span>
          <span className="text-xs font-semibold text-emerald-400 font-mono">km/h Average</span>
        </div>
        <div className="flex items-center justify-between text-[11px] text-slate-400 mt-2 pt-2 border-t border-slate-800/80">
          <span>Speed Limit: 50 km/h</span>
          <span className="text-emerald-400 font-semibold">+22% vs Fixed Cycle</span>
        </div>
      </div>

      {/* 4. Vulnerable Road Users (VRU) & Safety Lock */}
      <div className="p-5 rounded-3xl glass-panel hover:border-purple-500/40 transition-all duration-200 group relative overflow-hidden shadow-xl">
        <div className="absolute top-0 right-0 w-24 h-24 bg-purple-500/10 rounded-full blur-xl pointer-events-none" />
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">VRU & Crosswalk Radar</span>
          <div className="p-2 rounded-xl bg-purple-500/15 text-purple-400 group-hover:scale-110 transition-transform">
            <Users className="w-4 h-4" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-3xl font-extrabold text-white font-mono tracking-tight">{pedestrians}</span>
          <span className="text-xs font-semibold text-purple-300 font-mono">Pedestrians Detected</span>
        </div>
        <div className="flex items-center justify-between text-[11px] text-slate-400 mt-2 pt-2 border-t border-slate-800/80">
          <span>Crosswalk Safety Zone</span>
          <span className="text-emerald-400 font-semibold">Protected Phase</span>
        </div>
      </div>
    </div>
  );
};
