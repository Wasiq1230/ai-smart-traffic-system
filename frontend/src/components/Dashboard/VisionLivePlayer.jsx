import React, { useState, useEffect } from 'react';
import { Camera, Radio, Eye, Video, Sparkles, Shield, Cpu, RefreshCw } from 'lucide-react';

export const VisionLivePlayer = () => {
  const [fps, setFps] = useState(14.8);
  const [latency, setLatency] = useState(68);
  const [showBoxes, setShowBoxes] = useState(true);
  const [activeTab, setActiveTab] = useState('live_feed'); // 'live_feed', 'classes', 'anpr'

  useEffect(() => {
    const interval = setInterval(() => {
      setFps((14.2 + Math.random() * 1.2).toFixed(1));
      setLatency(Math.floor(65 + Math.random() * 8));
    }, 1500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-5 rounded-3xl bg-[#0b1220]/90 border border-cyan-500/30 backdrop-blur-xl shadow-2xl space-y-4 relative overflow-hidden">
      {/* Background ambient glow */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

      {/* Header bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-800/80">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-cyan-500/15 border border-cyan-500/30 text-cyan-400">
            <Camera className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-sm font-extrabold text-white tracking-wide">YOLOv8 AI VISION RADAR</h3>
              <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 text-[10px] font-bold uppercase flex items-center space-x-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
                <span>Live Feed</span>
              </span>
            </div>
            <p className="text-[11px] text-slate-400">Camera CAM-01 • Northbound Approach • PyTorch YOLOv8n</p>
          </div>
        </div>

        {/* Telemetry chips */}
        <div className="flex items-center space-x-2">
          <span className="px-2.5 py-1 rounded-xl bg-slate-900 border border-slate-700/60 text-cyan-300 font-mono text-[11px] font-bold">
            ⚡ {fps} FPS
          </span>
          <span className="px-2.5 py-1 rounded-xl bg-slate-900 border border-slate-700/60 text-slate-300 font-mono text-[11px]">
            {latency}ms
          </span>
        </div>
      </div>

      {/* Main Video & Bounding Box Canvas Simulation */}
      <div className="relative w-full aspect-video rounded-2xl bg-slate-950 border border-slate-800 overflow-hidden group">
        {/* Synthetic Video Canvas Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/40 z-10 pointer-events-none" />

        {/* Simulated Traffic Road Scene */}
        <svg viewBox="0 0 640 360" className="w-full h-full object-cover">
          {/* Road Asphalt */}
          <polygon points="120,360 260,140 380,140 520,360" fill="#1e293b" />
          <line x1="320" y1="140" x2="320" y2="360" stroke="#f59e0b" strokeWidth="3" strokeDasharray="12 10" />

          {/* Pedestrian Crossing Area */}
          <line x1="240" y1="170" x2="400" y2="170" stroke="#94a3b8" strokeWidth="6" strokeDasharray="10 8" />

          {/* YOLO Bounding Boxes (Real-time tracking overlays) */}
          {showBoxes && (
            <>
              {/* Car 1 */}
              <g className="animate-pulse">
                <rect x="270" y="220" width="100" height="70" fill="rgba(6, 182, 212, 0.15)" stroke="#06b6d4" strokeWidth="2" rx="4" />
                <rect x="270" y="202" width="90" height="18" fill="#06b6d4" rx="2" />
                <text x="274" y="215" fill="#020617" fontSize="10" fontWeight="bold" fontFamily="monospace">CAR [98%] #12</text>
                <text x="274" y="305" fill="#06b6d4" fontSize="9" fontFamily="monospace">42 km/h • Lane 1</text>
              </g>

              {/* Bus / Truck */}
              <g>
                <rect x="160" y="250" width="95" height="90" fill="rgba(139, 92, 246, 0.15)" stroke="#8b5cf6" strokeWidth="2" rx="4" />
                <rect x="160" y="232" width="85" height="18" fill="#8b5cf6" rx="2" />
                <text x="164" y="245" fill="#ffffff" fontSize="10" fontWeight="bold" fontFamily="monospace">BUS [96%] #08</text>
              </g>

              {/* Motorcycle */}
              <g>
                <rect x="390" y="240" width="45" height="55" fill="rgba(245, 158, 11, 0.15)" stroke="#f59e0b" strokeWidth="2" rx="4" />
                <rect x="390" y="224" width="70" height="16" fill="#f59e0b" rx="2" />
                <text x="393" y="236" fill="#020617" fontSize="9" fontWeight="bold" fontFamily="monospace">BIKE [94%] #19</text>
              </g>

              {/* Pedestrian (VRU) */}
              <g>
                <rect x="220" y="160" width="22" height="40" fill="rgba(239, 68, 68, 0.15)" stroke="#ef4444" strokeWidth="1.5" rx="3" />
                <rect x="220" y="146" width="60" height="14" fill="#ef4444" rx="2" />
                <text x="222" y="157" fill="#ffffff" fontSize="8" fontWeight="bold" fontFamily="monospace">PED #04</text>
              </g>
            </>
          )}
        </svg>

        {/* Camera HUD Overlay Controls */}
        <div className="absolute bottom-3 left-3 right-3 z-20 flex items-center justify-between text-xs">
          <div className="flex items-center space-x-2">
            <span className="px-2 py-1 rounded bg-black/70 text-cyan-300 font-mono text-[10px] border border-cyan-500/30">
              ● REC 1080p
            </span>
            <span className="px-2 py-1 rounded bg-black/70 text-slate-300 font-mono text-[10px]">
              IOU Tracking Active
            </span>
          </div>

          <button
            onClick={() => setShowBoxes(!showBoxes)}
            className="flex items-center space-x-1.5 px-3 py-1 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-slate-200 border border-slate-700 text-[11px] font-semibold transition"
          >
            <Eye className="w-3.5 h-3.5 text-cyan-400" />
            <span>{showBoxes ? 'Hide BBoxes' : 'Show BBoxes'}</span>
          </button>
        </div>
      </div>

      {/* Class breakdown counts */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 text-xs">
        <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
          <span className="text-[10px] text-slate-400 uppercase font-bold block">Cars Detected</span>
          <span className="text-base font-extrabold text-cyan-300 font-mono">18</span>
        </div>
        <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
          <span className="text-[10px] text-slate-400 uppercase font-bold block">Buses / Trucks</span>
          <span className="text-base font-extrabold text-purple-300 font-mono">4</span>
        </div>
        <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
          <span className="text-[10px] text-slate-400 uppercase font-bold block">Motorcycles</span>
          <span className="text-base font-extrabold text-amber-300 font-mono">5</span>
        </div>
        <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 text-center">
          <span className="text-[10px] text-slate-400 uppercase font-bold block">Pedestrians</span>
          <span className="text-base font-extrabold text-rose-300 font-mono">3</span>
        </div>
      </div>
    </div>
  );
};
