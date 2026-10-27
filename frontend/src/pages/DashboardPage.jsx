import React from 'react';
import { useTraffic } from '../context/TrafficContext';
import { IntersectionView } from '../components/Dashboard/IntersectionView';
import { SignalTimer } from '../components/Dashboard/SignalTimer';
import { VehicleCounter } from '../components/Dashboard/VehicleCounter';
import { VisionLivePlayer } from '../components/Dashboard/VisionLivePlayer';
import { ScenarioSwitcher } from '../components/Dashboard/ScenarioSwitcher';
import { TrafficChart } from '../components/Charts/TrafficChart';
import { PredictionChart } from '../components/Charts/PredictionChart';
import { ImpactChart } from '../components/Charts/ImpactChart';
import { VehicleTypePie } from '../components/Charts/VehicleTypePie';
import { DQNSimChart } from '../components/Charts/DQNSimChart';
import { AlertBanner } from '../components/Alerts/AlertBanner';
import { AccidentLog } from '../components/Alerts/AccidentLog';
import { ViolationTable } from '../components/Violations/ViolationTable';

export const DashboardPage = () => {
  return (
    <div className="space-y-6 pb-16">
      {/* 1. Alert Ribbon */}
      <AlertBanner />

      {/* 2. 1-Click Interactive 5-Scenario Studio */}
      <ScenarioSwitcher />

      {/* 3. Hero Telemetry Statistics (Vehicles, Density, Speed, Queue) */}
      <VehicleCounter />

      {/* 4. Primary Live Command Center Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left 6 Cols: 4-Way SVG Interactive Intersection & Phase Timer */}
        <div className="lg:col-span-6 space-y-6">
          <IntersectionView />
          <SignalTimer />
        </div>

        {/* Right 6 Cols: YOLOv8 Computer Vision Radar + AI Forecasting Curves */}
        <div className="lg:col-span-6 space-y-6">
          <VisionLivePlayer />
          <PredictionChart />
        </div>
      </div>

      {/* 5. Flow Streams & Real-Time Density Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-12">
          <TrafficChart />
        </div>
      </div>

      {/* 6. Environmental ESG Analytics & DQN RL Benchmark */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <VehicleTypePie />
        <ImpactChart />
        <DQNSimChart />
      </div>

      {/* 7. Bottom Incident Management & ANPR Violations Audit Logs */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-5">
          <AccidentLog />
        </div>
        <div className="lg:col-span-7">
          <ViolationTable />
        </div>
      </div>
    </div>
  );
};
