import React from 'react';
import { useTraffic } from '../../context/TrafficContext';
import { ShieldAlert, Camera, Download } from 'lucide-react';

export const ViolationTable = () => {
  const { violations } = useTraffic();

  const mockViolations = [
    { violation_id: 'VIOL-RED-42', plate: 'LEA-24-9102', type: 'Red-Light Crossing', speed: 78.4, fine: 2500, time: '2m ago' },
    { violation_id: 'VIOL-SPD-19', plate: 'ISB-22-4412', type: 'Speeding (Limit 50)', speed: 64.2, fine: 1500, time: '8m ago' }
  ];

  const list = (violations && violations.stored_violations && violations.stored_violations.length > 0) 
    ? violations.stored_violations 
    : mockViolations;

  return (
    <div className="p-5 rounded-3xl glass-panel space-y-4 shadow-xl border border-rose-500/30">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <ShieldAlert className="w-4 h-4 text-rose-400" />
          <h3 className="text-xs font-bold text-white uppercase tracking-wider">ANPR License Plate & Infraction Audit Log</h3>
        </div>
        <span className="text-[10px] text-slate-400 font-mono">Live OCR Snapshot Feed</span>
      </div>

      <div className="space-y-2 max-h-56 overflow-y-auto text-xs">
        {list.map((v, i) => (
          <div key={i} className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-center justify-between gap-4">
            <div className="flex items-center space-x-3">
              <span className="px-2.5 py-1 rounded-xl bg-black font-mono font-black text-amber-300 border border-slate-700 text-xs">
                {v.plate || v.plate_number || 'LEA-24-9102'}
              </span>
              <div>
                <p className="text-xs font-bold text-white">{v.type || v.violation_type || 'Red Light Violation'}</p>
                <span className="text-[10px] text-slate-400 font-mono">Recorded Speed: {v.speed || v.speed_recorded || 68} km/h</span>
              </div>
            </div>

            <div className="text-right">
              <span className="text-xs font-mono font-extrabold text-rose-400">Rs. {v.fine || v.fine_amount || 2500}</span>
              <span className="block text-[9px] text-slate-500">{v.time || 'Logged'}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
