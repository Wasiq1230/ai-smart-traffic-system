import React, { useState } from 'react';
import { TrafficProvider } from './context/TrafficContext';
import { Navbar } from './components/Navbar';
import { DashboardPage } from './pages/DashboardPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { SettingsPage } from './pages/SettingsPage';

const AppContent = () => {
  const [currentPage, setCurrentPage] = useState('dashboard');

  return (
    <div className="min-h-screen bg-[#050811] text-slate-100 flex flex-col font-sans selection:bg-cyan-500 selection:text-slate-950">
      {/* 1. Mission Control Header Bar */}
      <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />

      {/* 2. Main Mission Control Command Center */}
      <main className="flex-1 max-w-[1680px] w-full mx-auto p-4 sm:p-6 lg:p-8">
        {currentPage === 'dashboard' && <DashboardPage />}
        {currentPage === 'analytics' && <AnalyticsPage />}
        {currentPage === 'settings' && <SettingsPage />}
      </main>

      {/* 3. Enterprise Footer */}
      <footer className="py-4 border-t border-slate-900 bg-[#03060d] text-center text-xs text-slate-500 font-mono">
        NEURALTRAFFIC OS™ • Urban Mobility AI Command Center • Autonomous Signal Control & Vision Radar
      </footer>
    </div>
  );
};

export default function App() {
  return (
    <TrafficProvider>
      <AppContent />
    </TrafficProvider>
  );
}
