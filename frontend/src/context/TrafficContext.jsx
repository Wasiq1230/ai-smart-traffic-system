import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { connectWebSocket } from '../services/websocket';
import { api } from '../services/api';

const TrafficContext = createContext(null);

export const TrafficProvider = ({ children }) => {
  // Live State
  const [traffic, setTraffic] = useState({
    intersection_id: 'INT_001',
    lanes: {
      north: { count: 14, density: 0.70, level: 'HIGH', avg_speed_kmh: 22.0, queue_length: 6 },
      south: { count: 12, density: 0.60, level: 'MEDIUM', avg_speed_kmh: 26.5, queue_length: 4 },
      east: { count: 6, density: 0.30, level: 'LOW', avg_speed_kmh: 44.0, queue_length: 1 },
      west: { count: 5, density: 0.25, level: 'LOW', avg_speed_kmh: 46.0, queue_length: 1 },
    },
    total_vehicles: 37,
    pedestrian_count: 3,
    cyclist_count: 2,
    average_speed_kmh: 34.6,
    overall_congestion: 'MEDIUM',
  });

  const [signals, setSignals] = useState({
    intersection_id: 'INT_001',
    current_phase: 1,
    phase_name: 'North-South Arterial Green',
    signals: { north: 'GREEN', south: 'GREEN', east: 'RED', west: 'RED' },
    remaining_seconds: 24,
    current_phase_duration: 35,
    timings: { north_green: 35, south_green: 35, east_green: 20, west_green: 20, yellow: 5, all_red: 2 },
    override_active: false,
  });

  const [emergency, setEmergency] = useState({
    active: false,
    type: null,
    lane: null,
    priority: 5,
  });

  const [alerts, setAlerts] = useState([]);
  const [accidents, setAccidents] = useState([]);
  const [violations, setViolations] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('connecting'); // connecting, live, reconnecting, offline
  const [trafficHistory, setTrafficHistory] = useState([]);

  // Fetch initial REST data
  const loadInitialData = useCallback(async () => {
    try {
      const [trafRes, sigRes, emergRes, accRes, violRes] = await Promise.all([
        api.getCurrentTraffic(),
        api.getSignalStatus(),
        api.getActiveEmergency(),
        api.getActiveAccidents(),
        api.getViolations({ limit: 10 }),
      ]);

      if (trafRes.data) setTraffic(trafRes.data);
      if (sigRes.data) setSignals(sigRes.data);
      if (emergRes.data) setEmergency(emergRes.data);
      if (accRes.data) setAccidents(accRes.data);
      if (violRes.data) setViolations(violRes.data);
    } catch (err) {
      console.warn('[TrafficContext] Error loading initial REST data:', err);
    }
  }, []);

  useEffect(() => {
    loadInitialData();

    // Connect WebSocket
    const wsClient = connectWebSocket({
      onConnect: () => {
        setConnectionStatus('live');
      },
      onDisconnect: () => {
        setConnectionStatus('reconnecting');
      },
      onError: () => {
        setConnectionStatus('reconnecting');
      },
      onMessage: (data) => {
        if (data.type === 'TRAFFIC_STATE_UPDATE' || data.type === 'INITIAL_STATE') {
          if (data.traffic) {
            setTraffic(data.traffic);
            // Append to rolling history
            setTrafficHistory((prev) => {
              const item = {
                time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
                north: data.traffic.lanes.north.count,
                south: data.traffic.lanes.south.count,
                east: data.traffic.lanes.east.count,
                west: data.traffic.lanes.west.count,
                total: data.traffic.total_vehicles,
              };
              const updated = [...prev, item];
              return updated.length > 25 ? updated.slice(updated.length - 25) : updated;
            });
          }
          if (data.signals) setSignals(data.signals);
          if (data.emergency) setEmergency(data.emergency);
        }
      },
    });

    return () => {
      wsClient.close();
    };
  }, [loadInitialData]);

  // Actions
  const triggerEmergencyCorridor = async (lane = 'north', type = 'ambulance') => {
    try {
      const res = await api.triggerEmergency({ lane, emergency_type: type, priority: 5 });
      if (res.data?.emergency) setEmergency(res.data.emergency);
      if (res.data?.signal_state) setSignals(res.data.signal_state);
      setAlerts((prev) => [
        {
          id: Date.now(),
          type: 'EMERGENCY',
          severity: 'CRITICAL',
          title: `Emergency Corridor (${type.toUpperCase()})`,
          message: `Priority green granted for ${lane.toUpperCase()} approach.`,
        },
        ...prev,
      ]);
    } catch (e) {
      console.error('Trigger emergency error:', e);
    }
  };

  const clearEmergencyCorridor = async () => {
    try {
      const res = await api.clearEmergency();
      setEmergency({ active: false, type: null, lane: null, priority: 5 });
      if (res.data?.signal_state) setSignals(res.data.signal_state);
      setAlerts((prev) => prev.filter((a) => a.type !== 'EMERGENCY'));
    } catch (e) {
      console.error('Clear emergency error:', e);
    }
  };

  const simulateAccident = async (lane = 'east') => {
    try {
      const res = await api.reportAccident({
        intersection_id: 'INT_001',
        accident_type: 'collision',
        lane,
        severity: 'HIGH',
        vehicles_involved: 2,
        message: `Collision detected on ${lane.toUpperCase()} approach. Lane partially blocked.`,
      });
      const accList = await api.getActiveAccidents();
      setAccidents(accList.data);
      setAlerts((prev) => [
        {
          id: Date.now(),
          type: 'ACCIDENT',
          severity: 'HIGH',
          title: 'Accident Reported',
          message: `Vehicle collision confirmed on ${lane.toUpperCase()} lane. Dispatching recovery team.`,
        },
        ...prev,
      ]);
    } catch (e) {
      console.error('Simulate accident error:', e);
    }
  };

  const resolveAccident = async (id) => {
    try {
      await api.resolveAccident(id);
      const accList = await api.getActiveAccidents();
      setAccidents(accList.data);
      setAlerts((prev) => prev.filter((a) => a.type !== 'ACCIDENT'));
    } catch (e) {
      console.error('Resolve accident error:', e);
    }
  };

  const simulateViolation = async (lane = 'north') => {
    try {
      const plates = ['LEA-24-9102', 'ISB-22-4412', 'KHI-23-7781', 'RWP-21-3914'];
      const plate = plates[Math.floor(Math.random() * plates.length)];
      await api.reportViolation({
        intersection_id: 'INT_001',
        plate_number: plate,
        violation_type: 'red_light',
        lane,
        speed_recorded: 58.4,
        speed_limit: 50.0,
        fine_amount: 2500.0,
      });
      const violRes = await api.getViolations({ limit: 10 });
      setViolations(violRes.data);
    } catch (e) {
      console.error('Simulate violation error:', e);
    }
  };

  const advancePhase = async () => {
    try {
      const res = await api.advanceSignalPhase();
      if (res.data) setSignals(res.data);
    } catch (e) {
      console.error('Advance phase error:', e);
    }
  };

  const dismissAlert = (id) => {
    setAlerts((prev) => prev.filter((a) => a.id !== id));
  };

  return (
    <TrafficContext.Provider
      value={{
        traffic,
        signals,
        emergency,
        alerts,
        accidents,
        violations,
        connectionStatus,
        trafficHistory,
        triggerEmergencyCorridor,
        clearEmergencyCorridor,
        simulateAccident,
        resolveAccident,
        simulateViolation,
        advancePhase,
        dismissAlert,
      }}
    >
      {children}
    </TrafficContext.Provider>
  );
};

export const useTraffic = () => {
  const context = useContext(TrafficContext);
  if (!context) throw new Error('useTraffic must be used within a TrafficProvider');
  return context;
};
