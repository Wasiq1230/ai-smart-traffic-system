import React from 'react';
import { useTraffic } from '../../context/TrafficContext';
import { Siren, AlertTriangle, X, Check, ShieldAlert, Sparkles } from 'lucide-react';

export const AlertBanner = () => {
  const { emergency, alerts, clearEmergencyCorridor, dismissAlert } = useTraffic();

  return (
    <div className="space-y-2">
      {/* Emergency Active Banner */}
      {emergency.active && (
        <div className="bg-red-500/20 border-2 border-red-500 rounded-2xl p-4 flex items-center justify-between shadow-2xl animate-pulse">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-red-500 text-white rounded-xl shadow-lg">
              <Siren className="w-6 h-6 animate-spin" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 bg-red-500 text-white text-[11px] font-black rounded uppercase tracking-wider">
                  Emergency Priority Locked
                </span>
                <span className="text-xs text-red-200 font-mono">Priority Level: {emergency.priority}</span>
              </div>
              <p className="text-white font-bold text-sm mt-0.5">
                Active green corridor opened for {emergency.type?.toUpperCase()} on {emergency.lane?.toUpperCase()} approach. All conflicting signals locked to RED.
              </p>
            </div>
          </div>
          <button
            onClick={clearEmergencyCorridor}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 active:scale-95 text-white font-bold text-xs rounded-xl shadow-md transition flex items-center gap-1.5"
          >
            <Check className="w-4 h-4" />
            Clear Corridor & Restore Adaptive
          </button>
        </div>
      )}

      {/* Dynamic Alerts */}
      {alerts.map((alert) => (
        <div
          key={alert.id}
          className={`p-3.5 rounded-xl border flex items-center justify-between backdrop-blur-md transition ${
            alert.severity === 'CRITICAL'
              ? 'bg-red-950/40 border-red-500/40 text-red-200'
              : alert.severity === 'HIGH'
              ? 'bg-amber-950/40 border-amber-500/40 text-amber-200'
              : 'bg-blue-950/40 border-blue-500/40 text-blue-200'
          }`}
        >
          <div className="flex items-center gap-3">
            <AlertTriangle className={`w-5 h-5 shrink-0 ${alert.severity === 'CRITICAL' ? 'text-red-400' : 'text-amber-400'}`} />
            <div>
              <div className="font-bold text-xs uppercase tracking-wider text-white">{alert.title}</div>
              <div className="text-xs opacity-90 mt-0.5">{alert.message}</div>
            </div>
          </div>
          <button
            onClick={() => dismissAlert(alert.id)}
            className="p-1 hover:bg-white/10 rounded-lg text-slate-400 hover:text-white transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      ))}
    </div>
  );
};
