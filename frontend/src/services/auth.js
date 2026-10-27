export const authService = {
  getToken: () => localStorage.getItem('traffic_jwt_token'),
  getUser: () => {
    const userStr = localStorage.getItem('traffic_user');
    return userStr ? JSON.parse(userStr) : null;
  },
  setSession: (token, user) => {
    localStorage.setItem('traffic_jwt_token', token);
    localStorage.setItem('traffic_user', JSON.stringify(user));
  },
  clearSession: () => {
    localStorage.removeItem('traffic_jwt_token');
    localStorage.removeItem('traffic_user');
  },
  isAuthenticated: () => !!localStorage.getItem('traffic_jwt_token'),
};
