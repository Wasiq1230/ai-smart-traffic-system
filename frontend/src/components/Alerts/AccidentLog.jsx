import React from 'react';
import { useTraffic } from '../../context/TrafficContext';
import { AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';

export const AccidentLog = () => {
  const { accidents, resolveAccident } = useTraffic();

  const mockAccidents = [
    { id: 'acc-1', incident_id: 'INC-STOP-104', type: 'collision', lane: 'Eastbound', severity: 'HIGH', status: 'CONFIRMED', description: 'Stationary vehicle obstruction detected in travel lane for >12s' }
  ];

  const list = accidents.length > 0 ? accidents : mockAccidents;

  return (
    <div className="p-5 rounded-3xl glass-panel space-y-4 shadow-xl border border-amber-500/30">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <AlertTriangle className="w-4 h-4 text-amber-400" />
          <h3 className="text-xs font-bold text-white uppercase tracking-wider">Active Road Incidents & Collision Radar</h3>
        </div>
        <span className="px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-mono text-[10px] font-bold">
          {list.length} Active
        </span>
      </div>

      <div className="space-y-2.5 max-h-56 overflow-y-auto">
        {list.map((inc) => (
          <div key={inc.id} className="p-3.5 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-center justify-between gap-3 text-xs">
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-mono font-bold text-amber-300">{inc.incident_id || 'INC-101'}</span>
                <span className="px-1.5 py-0.2 rounded bg-rose-500/20 text-rose-300 font-bold text-[9px] uppercase">
                  {inc.severity || 'HIGH'}
                </span>
              </div>
              <p className="text-[11px] text-slate-300 mt-1">{inc.description || `${inc.type} on ${inc.lane}`}</p>
            </div>

            <button
              onClick={() => resolveAccident && resolveAccident(inc.id)}
              className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-emerald-600/30 hover:text-emerald-300 text-slate-300 text-[10px] font-bold border border-slate-700 transition"
            >
              Resolve
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
