<template>
  <div id="app" class="container">
    <!-- Top Toolbar -->
    <nav class="toolbar">
      <div class="toolbar-left">
        <h1 class="toolbar-title">{{ title }}</h1>
      </div>

      <div class="toolbar-center">
        <div class="status-indicator-toolbar" :class="{ connected: isConnected, disconnected: !isConnected }">
          <span class="status-dot-toolbar"></span>
          <span class="status-text-toolbar">
            {{ isConnected ? 'Connected to ' + broker : 'Not Connected' }}
          </span>
        </div>
      </div>

      <div class="toolbar-right">
        <!-- Connection Buttons -->
        <div class="toolbar-button-group">
          <button 
            @click="connectToBroker" 
            :disabled="isConnected || loading"
            class="btn btn-toolbar btn-connect"
            title="Connect to trading broker"
          >
            {{ loading ? '⟳' : '⚡' }}
          </button>
          <button 
            @click="disconnectFromBroker" 
            :disabled="!isConnected || loading"
            class="btn btn-toolbar btn-disconnect"
            title="Disconnect from broker"
          >
            {{ loading ? '⟳' : '⊗' }}
          </button>
        </div>

        <!-- Account Type Switcher -->
        <div class="toolbar-button-group account-toggle">
          <button 
            v-for="type in accountTypes"
            :key="type"
            @click="switchAccountType(type)"
            :disabled="loading"
            :class="{ active: currentAccountType === type }"
            class="btn btn-toolbar-toggle"
            :title="`Switch to ${type.toUpperCase()} account`"
          >
            {{ type.substring(0, 1).toUpperCase() }}
          </button>
        </div>

        <!-- Balance Display -->
        <div class="balance-display">
          <div class="balance-amount-small">${{ balance.toFixed(2) }}</div>
          <div class="balance-label-small">{{ currentAccountType.toUpperCase() }}</div>
        </div>
      </div>
    </nav>

    <!-- Main Header -->
    <header class="header">
      <p class="subtitle">Trading Application Dashboard</p>
    </header>

    <!-- Error Messages -->
    <div v-if="connectionError" class="error-banner">
      {{ connectionError }}
    </div>
    <div v-if="accountError" class="error-banner">
      {{ accountError }}
    </div>

    <!-- Balance Card (Main Display) -->
    <section class="section balance-section" v-if="isConnected">
      <div class="balance-card-main">
        <div class="balance-label">Available Balance</div>
        <div class="balance-amount-main">${{ balance.toFixed(2) }}</div>
        <div class="balance-currency">USD</div>
        <div class="account-info-main">
          Account: <strong>{{ currentAccountType.toUpperCase() }}</strong>
        </div>
      </div>
    </section>

    <!-- Status Information -->
    <section class="section status-section">
      <h2>Status Information</h2>
      <div class="status-info">
        <div class="info-row">
          <span class="info-label">Connection Status:</span>
          <span :class="{ 'text-success': isConnected, 'text-danger': !isConnected }">
            {{ isConnected ? 'Connected' : 'Disconnected' }}
          </span>
        </div>
        <div class="info-row">
          <span class="info-label">Current Broker:</span>
          <span>{{ broker || 'None' }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Account Type:</span>
          <span>{{ currentAccountType.toUpperCase() }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Last Updated:</span>
          <span>{{ lastUpdated }}</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { tradingAPI } from './services/api'

const title = ref('Trading Platform')
const isConnected = ref(false)
const broker = ref(null)
const currentAccountType = ref('demo')
const balance = ref(0)
const accountTypes = ['demo', 'real']
const loading = ref(false)
const connectionError = ref(null)
const accountError = ref(null)
const lastUpdated = ref('')

// Fetch trading status on mount
const fetchStatus = async () => {
  try {
    const status = await tradingAPI.getStatus()
    isConnected.value = status.connected
    broker.value = status.broker || 'Demo Broker'
    currentAccountType.value = status.account_type
    await fetchBalance()
    updateTimestamp()
  } catch (err) {
    console.error('Failed to fetch status:', err)
  }
}

// Fetch account balance
const fetchBalance = async () => {
  try {
    const account = await tradingAPI.getAccount(currentAccountType.value)
    balance.value = account.balance
    updateTimestamp()
  } catch (err) {
    accountError.value = 'Failed to fetch balance'
    console.error(err)
  }
}

// Connect to broker
const connectToBroker = async () => {
  loading.value = true
  connectionError.value = null
  try {
    await tradingAPI.connectBroker('Demo Broker')
    await fetchStatus()
  } catch (err) {
    connectionError.value = 'Failed to connect to broker'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Disconnect from broker
const disconnectFromBroker = async () => {
  loading.value = true
  connectionError.value = null
  try {
    await tradingAPI.disconnectBroker()
    await fetchStatus()
  } catch (err) {
    connectionError.value = 'Failed to disconnect from broker'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Switch account type
const switchAccountType = async (accountType) => {
  loading.value = true
  accountError.value = null
  try {
    await tradingAPI.switchAccount(accountType)
    currentAccountType.value = accountType
    await fetchBalance()
  } catch (err) {
    accountError.value = 'Failed to switch account'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Update timestamp
const updateTimestamp = () => {
  lastUpdated.value = new Date().toLocaleTimeString()
}

onMounted(() => {
  fetchStatus()
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Toolbar Styles */
.toolbar {
  background: rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 12px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
  flex-wrap: wrap;
}

.toolbar-left {
  flex: 0 0 auto;
  min-width: 200px;
}

.toolbar-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.toolbar-center {
  flex: 1;
  display: flex;
  justify-content: center;
  min-width: 200px;
}

.toolbar-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 15px;
  flex-wrap: wrap;
}

/* Status Indicator in Toolbar */
.status-indicator-toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9rem;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  backdrop-filter: blur(10px);
}

.status-indicator-toolbar.connected {
  background: rgba(76, 175, 80, 0.3);
  color: #c8e6c9;
}

.status-indicator-toolbar.disconnected {
  background: rgba(244, 67, 54, 0.3);
  color: #ffcdd2;
}

.status-dot-toolbar {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.status-indicator-toolbar.connected .status-dot-toolbar {
  background-color: #4caf50;
}

.status-indicator-toolbar.disconnected .status-dot-toolbar {
  background-color: #f44336;
}

.status-text-toolbar {
  white-space: nowrap;
  font-size: 0.85rem;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Toolbar Buttons */
.toolbar-button-group {
  display: flex;
  gap: 8px;
}

.btn-toolbar {
  padding: 8px 14px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.btn-toolbar:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.btn-toolbar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-connect {
  background: rgba(76, 175, 80, 0.3);
  border-color: rgba(76, 175, 80, 0.5);
  color: #c8e6c9;
}

.btn-connect:hover:not(:disabled) {
  background: rgba(76, 175, 80, 0.5);
  border-color: rgba(76, 175, 80, 0.8);
}

.btn-disconnect {
  background: rgba(244, 67, 54, 0.3);
  border-color: rgba(244, 67, 54, 0.5);
  color: #ffcdd2;
}

.btn-disconnect:hover:not(:disabled) {
  background: rgba(244, 67, 54, 0.5);
  border-color: rgba(244, 67, 54, 0.8);
}

/* Account Toggle in Toolbar */
.account-toggle {
  gap: 4px;
}

.btn-toolbar-toggle {
  padding: 8px 12px;
  font-size: 0.9rem;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 700;
  min-width: 36px;
  backdrop-filter: blur(10px);
}

.btn-toolbar-toggle:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-toolbar-toggle.active {
  background: #667eea;
  border-color: #667eea;
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-toolbar-toggle:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Balance Display in Toolbar */
.balance-display {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 6px;
  padding: 6px 14px;
  text-align: right;
  backdrop-filter: blur(10px);
  min-width: 120px;
}

.balance-amount-small {
  font-size: 1.1rem;
  font-weight: 700;
  color: white;
}

.balance-label-small {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.8);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Main Header */
.header {
  text-align: center;
  color: white;
  padding: 30px 20px 20px;
}

.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
}

/* Error Banner */
.error-banner {
  background-color: #f44336;
  color: white;
  padding: 12px 20px;
  margin: 10px;
  border-radius: 6px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(244, 67, 54, 0.3);
}

/* Sections */
.section {
  background: white;
  border-radius: 12px;
  padding: 30px;
  margin: 20px auto;
  max-width: 600px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.section h2 {
  color: #333;
  margin-bottom: 25px;
  font-size: 1.5rem;
  border-bottom: 2px solid #667eea;
  padding-bottom: 10px;
}

/* Balance Section */
.balance-section {
  background: white;
}

.balance-card-main {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
}

.balance-label {
  font-size: 0.9rem;
  opacity: 0.9;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.balance-amount-main {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 5px;
}

.balance-currency {
  font-size: 0.85rem;
  opacity: 0.8;
  margin-bottom: 20px;
}

.account-info-main {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.3);
  font-size: 0.95rem;
}

/* Status Section */
.status-section {
  background: white;
}

.status-info {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 20px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #e0e0e0;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 600;
  color: #555;
}

.text-success {
  color: #4caf50;
  font-weight: 600;
}

.text-danger {
  color: #f44336;
  font-weight: 600;
}

/* Responsive */
@media (max-width: 1024px) {
  .toolbar {
    justify-content: space-around;
  }

  .toolbar-center {
    order: 3;
    flex-basis: 100%;
  }

  .toolbar-right {
    order: 2;
    flex: 0 1 auto;
  }
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    gap: 12px;
    padding: 10px;
  }

  .toolbar-left {
    min-width: auto;
    width: 100%;
    text-align: center;
  }

  .toolbar-title {
    font-size: 1.2rem;
  }

  .toolbar-center {
    order: 2;
    flex-basis: 100%;
    filter: none;
  }

  .toolbar-right {
    order: 3;
    flex-basis: 100%;
    justify-content: center;
    flex-wrap: wrap;
  }

  .balance-display {
    min-width: 100px;
  }

  .header {
    padding: 20px 10px;
  }

  .subtitle {
    font-size: 1rem;
  }

  .section {
    margin: 15px;
    padding: 20px;
  }

  .balance-amount-main {
    font-size: 2.5rem;
  }

  .status-indicator-toolbar {
    font-size: 0.8rem;
  }

  .status-text-toolbar {
    font-size: 0.75rem;
  }
}

@media (max-width: 480px) {
  .toolbar-title {
    font-size: 1rem;
  }

  .toolbar-button-group {
    gap: 6px;
  }

  .btn-toolbar {
    padding: 6px 10px;
    font-size: 0.9rem;
  }

  .balance-display {
    padding: 4px 10px;
  }

  .balance-amount-small {
    font-size: 0.95rem;
  }

  .balance-label-small {
    font-size: 0.65rem;
  }

  .balance-amount-main {
    font-size: 2rem;
  }

  .section {
    margin: 10px;
    padding: 15px;
  }

  .section h2 {
    font-size: 1.2rem;
  }
}
</style>
