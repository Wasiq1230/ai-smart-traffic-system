import React, { useState } from 'react';
import { ShieldCheck, Lock, User, Key, ArrowRight } from 'lucide-react';
import { api } from '../services/api';
import { authService } from '../services/auth';

export const LoginPage = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('operator');
  const [password, setPassword] = useState('operator123');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e?.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await api.login({ username, password });
      if (res.data?.access_token) {
        authService.setSession(res.data.access_token, {
          username: res.data.username,
          role: res.data.role,
        });
        onLoginSuccess();
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Authentication failed. Please check credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickLogin = (u, p) => {
    setUsername(u);
    setPassword(p);
  };

  return (
    <div className="min-h-screen bg-[#070b14] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Glow Backdrop */}
      <div className="absolute w-[500px] h-[500px] bg-cyan-500/10 rounded-full blur-3xl pointer-events-none -top-20 -left-20" />
      <div className="absolute w-[500px] h-[500px] bg-indigo-500/10 rounded-full blur-3xl pointer-events-none -bottom-20 -right-20" />

      <div className="glass-panel max-w-md w-full rounded-3xl p-8 border border-slate-800 shadow-2xl relative z-10">
        <div className="text-center mb-8">
          <div className="inline-flex p-3 bg-cyan-500/10 border border-cyan-500/30 rounded-2xl text-cyan-400 mb-3 shadow-lg">
            <ShieldCheck className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-black text-white">AI SMART TRAFFIC</h1>
          <p className="text-xs text-slate-400 mt-1">Urban Traffic Operations & Control Center</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-950/50 border border-red-500/50 rounded-xl text-xs text-red-200 text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Operator ID / Username</label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="w-full bg-slate-900 border border-slate-700 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500 transition"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full bg-slate-900 border border-slate-700 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500 transition"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-cyan-600 hover:bg-cyan-500 active:scale-98 text-white font-bold text-sm rounded-xl shadow-lg transition flex items-center justify-center gap-2 mt-2"
          >
            {loading ? 'Authenticating...' : (
              <>
                Enter Command Console
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Quick Demo Logins */}
        <div className="mt-8 pt-6 border-t border-slate-800">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block text-center mb-3">
            Quick Demo Accounts
          </span>
          <div className="grid grid-cols-3 gap-2">
            <button
              onClick={() => handleQuickLogin('admin', 'admin123')}
              className="px-2 py-1.5 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 rounded-lg text-xs font-medium transition"
            >
              Admin
            </button>
            <button
              onClick={() => handleQuickLogin('operator', 'operator123')}
              className="px-2 py-1.5 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-cyan-300 rounded-lg text-xs font-medium transition"
            >
              Operator
            </button>
            <button
              onClick={() => handleQuickLogin('viewer', 'viewer123')}
              className="px-2 py-1.5 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-400 rounded-lg text-xs font-medium transition"
            >
              Viewer
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
