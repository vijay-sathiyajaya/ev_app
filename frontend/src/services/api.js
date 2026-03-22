// API service for backend communication
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const apiClient = {
  async get(endpoint) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  },

  async post(endpoint, data) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  },
};

// Trading API client
export const tradingAPI = {
  // Get trading status
  async getStatus() {
    return apiClient.get('/api/trading/status');
  },

  // Connect to broker
  async connectBroker(brokerName = 'Demo Broker') {
    return apiClient.post('/api/trading/connect', { broker: brokerName });
  },

  // Disconnect from broker
  async disconnectBroker() {
    return apiClient.post('/api/trading/disconnect', {});
  },

  // Get account information
  async getAccount(accountType = 'demo') {
    return apiClient.get(`/api/trading/account?type=${accountType}`);
  },

  // Switch account type
  async switchAccount(accountType) {
    return apiClient.post('/api/trading/account/switch', { account_type: accountType });
  },
};

// Broker Authentication API client - iqOption integration
export const brokerAPI = {
  // Login with iqOption credentials
  async login(email, password) {
    return apiClient.post('/api/broker/login', {
      email: email.trim(),
      password: password
    });
  },

  // Logout from iqOption broker
  async logout(sessionId) {
    return apiClient.post('/api/broker/logout', {
      sessionId: sessionId
    });
  },

  // Get account balance
  async getBalance(sessionId) {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/broker/balance?sessionId=${sessionId}`,
        {
          method: 'GET',
          headers: {
            'Accept': 'application/json'
          }
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  },

  // Switch trading mode (demo/live)
  async switchMode(sessionId, mode) {
    return apiClient.post('/api/broker/mode/switch', {
      sessionId: sessionId,
      mode: mode.toLowerCase()
    });
  }
};
