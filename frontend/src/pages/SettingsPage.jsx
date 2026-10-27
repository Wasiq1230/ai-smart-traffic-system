import React, { useState } from 'react';
import { Sliders, Settings2, Shield, Video, Play, Save, Check, RefreshCw } from 'lucide-react';
import { useTraffic } from '../context/TrafficContext';

export const SettingsPage = () => {
  const { triggerEmergencyCorridor, simulateAccident, simulateViolation } = useTraffic();

  const [minGreen, setMinGreen] = useState(15);
  const [maxGreen, setMaxGreen] = useState(90);
  const [yellowTime, setYellowTime] = useState(5);
  const [confThreshold, setConfThreshold] = useState(0.40);
  const [frameSkip, setFrameSkip] = useState(2);
  const [saved, setSaved] = useState(false);

  const handleSave = (e) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto pb-12">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-black text-white">System Configuration & Parameters</h2>
          <p className="text-xs text-slate-400 mt-1">Live tuning of perception engine thresholds, safety constraints, and signal parameters.</p>
        </div>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Signal Timing Bounds */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center gap-2 mb-2">
            <Sliders className="w-5 h-5 text-cyan-400" />
            <h3 className="font-bold text-white text-base">Adaptive Signal Timing Bounds</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Minimum Green Time: <span className="font-mono text-cyan-400">{minGreen}s</span>
              </label>
              <input
                type="range"
                min="10"
                max="30"
                value={minGreen}
                onChange={(e) => setMinGreen(Number(e.target.value))}
                className="w-full accent-cyan-400"
              />
              <p className="text-[10px] text-slate-500 mt-1">Safety lower bound preventing starvation.</p>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Maximum Green Cap: <span className="font-mono text-cyan-400">{maxGreen}s</span>
              </label>
              <input
                type="range"
                min="45"
                max="120"
                value={maxGreen}
                onChange={(e) => setMaxGreen(Number(e.target.value))}
                className="w-full accent-cyan-400"
              />
              <p className="text-[10px] text-slate-500 mt-1">Upper limit under extreme congestion.</p>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Yellow Transition: <span className="font-mono text-cyan-400">{yellowTime}s</span>
              </label>
              <input
                type="range"
                min="3"
                max="8"
                value={yellowTime}
                onChange={(e) => setYellowTime(Number(e.target.value))}
                className="w-full accent-cyan-400"
              />
              <p className="text-[10px] text-slate-500 mt-1">Standard caution phase interval.</p>
            </div>
          </div>
        </div>

        {/* Computer Vision Engine Settings */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center gap-2 mb-2">
            <Video className="w-5 h-5 text-indigo-400" />
            <h3 className="font-bold text-white text-base">Perception Engine & Hardware Tuning</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                YOLOv8 Detection Confidence: <span className="font-mono text-indigo-400">{confThreshold}</span>
              </label>
              <input
                type="range"
                min="0.25"
                max="0.85"
                step="0.05"
                value={confThreshold}
                onChange={(e) => setConfThreshold(Number(e.target.value))}
                className="w-full accent-indigo-400"
              />
              <p className="text-[10px] text-slate-500 mt-1">Filter low-confidence detections.</p>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                CPU Frame Skipping: <span className="font-mono text-indigo-400">Process every {frameSkip}nd frame</span>
              </label>
              <input
                type="range"
                min="1"
                max="4"
                value={frameSkip}
                onChange={(e) => setFrameSkip(Number(e.target.value))}
                className="w-full accent-indigo-400"
              />
              <p className="text-[10px] text-slate-500 mt-1">Optimizes CPU utilization to achieve 30+ FPS.</p>
            </div>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            className="flex items-center gap-2 px-6 py-2.5 bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-sm rounded-xl shadow-lg transition active:scale-95"
          >
            {saved ? (
              <>
                <Check className="w-4 h-4" />
                Parameters Applied
              </>
            ) : (
              <>
                <Save className="w-4 h-4" />
                Save System Configuration
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
