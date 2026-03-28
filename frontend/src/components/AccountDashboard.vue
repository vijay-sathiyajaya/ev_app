<template>
  <div class="account-dashboard">
    <div class="dashboard-container">
      <!-- Header -->
      <div class="dashboard-header">
        <h1 class="dashboard-title">Account Dashboard</h1>
        <div class="header-buttons">
          <button
            @click="toggleTheme"
            class="btn-theme-toggle"
            :title="`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`"
          >
            {{ theme === 'light' ? '🌙' : '☀️' }}
          </button>
          <button
            @click="handleLogout"
            class="btn-logout"
            :disabled="isLoading"
          >
            {{ isLoading ? '⟳' : '⊗' }} Logout
          </button>
        </div>
      </div>

      <!-- Account Info Card -->
      <div class="card account-info-card">
        <div class="card-icon">👤</div>
        <div class="card-content">
          <h2 class="card-title">Account</h2>
          <p class="account-email">{{ userEmail }}</p>
        </div>
      </div>

      <!-- Balance Card -->
      <div class="card balance-card">
        <div class="card-icon">💰</div>
        <div class="card-content">
          <h2 class="card-title">Balance</h2>
          <p class="balance-amount">${{ formatBalance(balance) }}</p>
          <p class="balance-info">{{ tradingMode.toUpperCase() }} Account</p>
          <p class="last-updated">Updated: {{ lastUpdated }}</p>
        </div>
        <button
          @click="refreshBalance"
          class="btn-refresh"
          :disabled="isLoading"
          title="Refresh balance"
        >
          🔄
        </button>
      </div>

      <!-- Mode Switcher Card -->
      <div class="card mode-switcher-card">
        <div class="card-icon">⚙️</div>
        <div class="card-content">
          <h2 class="card-title">Trading Mode</h2>
          <p class="mode-label">Current Mode: <strong>{{ tradingMode.toUpperCase() }}</strong></p>
          
          <div class="mode-buttons">
            <button
              v-for="mode in tradingModes"
              :key="mode"
              @click="switchMode(mode)"
              class="btn-mode"
              :class="{ 'active': tradingMode === mode, 'warning': mode === 'live' }"
              :disabled="isLoading || tradingMode === mode"
            >
              {{ mode === 'demo' ? '🎮 Demo' : '💵 Live' }}
            </button>
          </div>

          <div v-if="tradingMode === 'live'" class="warning-banner">
            <span class="warning-icon">⚠️</span>
            <span>Live mode uses real money!</span>
          </div>
        </div>
      </div>

      <!-- Binary Trading Panel Card -->
      <div class="card trading-panel-card">
        <div class="card-icon">💱</div>
        <div class="card-content">
          <h2 class="card-title">Binary Options Trading</h2>
          <p class="card-description">Fast-paced Forex binary options trading with real-time quotes and instant execution.</p>
          <button
            @click="navigateToBinaryTrading"
            class="btn-trade"
            :disabled="isLoading"
          >
            📊 Open Trading Panel
          </button>
        </div>
      </div>

      <!-- Status Messages -->
      <div v-if="successMessage" class="success-message">
        <span class="success-icon">✓</span>
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="error-message">
        <span class="error-icon">⚠</span>
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AccountDashboard',
  props: {
    sessionId: {
      type: String,
      required: true
    },
    userEmail: {
      type: String,
      required: true
    },
    apiUrl: {
      type: String,
      default: 'http://localhost:5000'
    },
    theme: {
      type: String,
      default: 'light'
    }
  },
  data() {
    return {
      balance: 0,
      tradingMode: 'demo',
      tradingModes: ['demo', 'live'],
      isLoading: false,
      errorMessage: '',
      successMessage: '',
      lastUpdated: ''
    };
  },
  mounted() {
    // Load initial balance
    this.refreshBalance();
  },
  methods: {
    toggleTheme() {
      this.$emit('toggle-theme');
    },
    async refreshBalance() {
      this.isLoading = true;
      this.errorMessage = '';

      try {
        const response = await fetch(
          `${this.apiUrl}/api/broker/balance?sessionId=${this.sessionId}`,
          {
            method: 'GET',
            headers: {
              'Accept': 'application/json'
            }
          }
        );

        const data = await response.json();

        if (!response.ok) {
          this.errorMessage = data.error || 'Failed to fetch balance';
          return;
        }

        this.balance = data.balance;
        this.tradingMode = data.mode;
        this.lastUpdated = new Date(data.lastUpdated).toLocaleTimeString();

        this.successMessage = 'Balance updated';
        setTimeout(() => { this.successMessage = ''; }, 3000);
      } catch (error) {
        this.errorMessage = `Connection error: ${error.message}`;
      } finally {
        this.isLoading = false;
      }
    },

    async switchMode(newMode) {
      // Show confirmation for live mode
      if (newMode === 'live' && !confirm('Switch to LIVE mode? This uses real money!')) {
        return;
      }

      this.isLoading = true;
      this.errorMessage = '';

      try {
        const response = await fetch(`${this.apiUrl}/api/broker/mode/switch`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            sessionId: this.sessionId,
            mode: newMode
          })
        });

        const data = await response.json();

        if (!response.ok) {
          this.errorMessage = data.error || 'Failed to switch mode';
          return;
        }

        this.balance = data.balance;
        this.tradingMode = data.mode;
        this.lastUpdated = new Date(data.lastUpdated).toLocaleTimeString();

        this.successMessage = data.message || `Switched to ${newMode} mode`;
        setTimeout(() => { this.successMessage = ''; }, 3000);

        // Store preference in localStorage
        localStorage.setItem('tradingMode', newMode);
      } catch (error) {
        this.errorMessage = `Connection error: ${error.message}`;
      } finally {
        this.isLoading = false;
      }
    },

    async handleLogout() {
      if (!confirm('Are you sure you want to logout?')) {
        return;
      }

      this.isLoading = true;
      this.errorMessage = '';

      try {
        const response = await fetch(`${this.apiUrl}/api/broker/logout`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            sessionId: this.sessionId
          })
        });

        const data = await response.json();

        if (!response.ok) {
          this.errorMessage = data.error || 'Logout failed';
          return;
        }

        // Clear localStorage
        localStorage.removeItem('sessionId');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('tradingMode');

        // Emit logout event
        this.$emit('logout');
      } catch (error) {
        this.errorMessage = `Connection error: ${error.message}`;
      } finally {
        this.isLoading = false;
      }
    },

    formatBalance(amount) {
      return amount.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    },

    navigateToBinaryTrading() {
      this.$emit('navigate', 'binary-trading');
    }
  }
};
</script>

<style scoped>
.account-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30px 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.dashboard-container {
  max-width: 600px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  gap: 15px;
}

.dashboard-title {
  color: white;
  font-size: 32px;
  font-weight: 700;
  margin: 0;
}

.header-buttons {
  display: flex;
  gap: 10px;
  align-items: center;
}

.btn-theme-toggle {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 44px;
  min-height: 44px;
}

.btn-theme-toggle:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.btn-logout {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
}

.btn-logout:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.btn-logout:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.card-icon {
  font-size: 40px;
  flex-shrink: 0;
}

.card-content {
  flex: 1;
}

.card-title {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 18px;
  font-weight: 700;
}

.account-email {
  color: #666;
  font-size: 16px;
  margin: 0;
}

.balance-amount {
  font-size: 36px;
  font-weight: 700;
  color: #667eea;
  margin: 10px 0 5px 0;
}

.balance-info {
  color: #666;
  font-size: 14px;
  margin: 0;
}

.last-updated {
  font-size: 12px;
  color: #999;
  margin: 5px 0 0 0;
}

.btn-refresh {
  align-self: center;
  background: #f0f4ff;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.btn-refresh:hover:not(:disabled) {
  background: #667eea;
  color: white;
  transform: rotate(180deg);
}

.btn-refresh:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.mode-label {
  color: #666;
  font-size: 14px;
  margin: 0 0 15px 0;
}

.mode-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.btn-mode {
  flex: 1;
  padding: 12px;
  border: 2px solid #e0e0e0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-mode:hover:not(:disabled) {
  border-color: #667eea;
  background: #f0f4ff;
}

.btn-mode.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.btn-mode.warning {
  border-color: #ff6b6b;
}

.btn-mode.warning.active {
  background: #ff6b6b;
}

.btn-mode:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.warning-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 6px;
  color: #856404;
  font-size: 13px;
  font-weight: 600;
}

.warning-icon {
  font-size: 16px;
}

.success-message,
.error-message {
  padding: 15px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 20px;
}

.success-message {
  background: #d4edda;
  color: #155724;
  border-left: 4px solid #28a745;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  border-left: 4px solid #f5c6cb;
}

.success-icon,
.error-icon {
  font-size: 18px;
}

/* Dark mode support */
.dark-mode .dashboard-title {
  color: #fff;
}

.dark-mode .card {
  background: #1e1e1e;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.dark-mode .card-title {
  color: #fff;
}

.dark-mode .account-email,
.dark-mode .balance-info {
  color: #ccc;
}

.dark-mode .btn-refresh {
  background: #2d2d2d;
}

.dark-mode .mode-label {
  color: #ccc;
}

.dark-mode .btn-mode {
  background: #2d2d2d;
  border-color: #444;
  color: #fff;
}

.dark-mode .btn-mode:hover:not(:disabled) {
  border-color: #667eea;
  background: #1a1a1a;
}

.trading-panel-card {
  flex-direction: column;
}

.card-description {
  color: #666;
  font-size: 14px;
  margin: 0 0 15px 0;
  line-height: 1.5;
}

.btn-trade {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-trade:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
}

.btn-trade:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.dark-mode .card-description {
  color: #aaa;
}
</style>
