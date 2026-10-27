import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Inject JWT token if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('traffic_jwt_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const api = {
  // Traffic
  getCurrentTraffic: (id = 'INT_001') => apiClient.get(`/traffic/current/${id}`),
  updateTrafficCounts: (id, payload) => apiClient.post(`/traffic/counts/${id}`, payload),
  getTrafficHistory: (id = 'INT_001') => apiClient.get(`/traffic/history/${id}`),

  // Signals
  getSignalStatus: (id = 'INT_001') => apiClient.get(`/signals/status/${id}`),
  calculateSignals: (payload) => apiClient.post('/signals/calculate', payload),
  advanceSignalPhase: () => apiClient.post('/signals/advance-phase'),

  // Emergency
  getActiveEmergency: () => apiClient.get('/emergency/active'),
  triggerEmergency: (payload) => apiClient.post('/emergency/override', payload),
  clearEmergency: () => apiClient.post('/emergency/clear'),

  // Accidents
  getActiveAccidents: () => apiClient.get('/accidents/active'),
  getAccidentHistory: () => apiClient.get('/accidents/history'),
  reportAccident: (payload) => apiClient.post('/accidents/report', payload),
  resolveAccident: (id) => apiClient.post(`/accidents/resolve/${id}`),

  // Violations
  getViolations: (params) => apiClient.get('/violations/list', { params }),
  reportViolation: (payload) => apiClient.post('/violations/detect', payload),

  // Forecast & Analytics
  getForecast: (id = 'INT_001') => apiClient.get(`/forecast/${id}`),
  getAnalyticsSummary: () => apiClient.get('/analytics/summary'),
  getEnvironmentalImpact: () => apiClient.get('/analytics/impact'),
  getDQNComparison: () => apiClient.get('/analytics/dqn/comparison'),

  // Auth
  login: (credentials) => apiClient.post('/auth/login', credentials),
  getMe: () => apiClient.get('/auth/me'),

  // Health
  getHealth: () => axios.get('http://localhost:8000/health'),
};
