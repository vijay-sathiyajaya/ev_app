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
