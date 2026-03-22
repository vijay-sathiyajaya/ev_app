<template>
  <div id="app">
    <!-- Show Login Form if Not Authenticated -->
    <LoginForm
      v-if="!isAuthenticated"
      @login="handleLogin"
      :apiUrl="apiUrl"
    />

    <!-- Show Account Dashboard if Authenticated -->
    <AccountDashboard
      v-else
      :sessionId="sessionId"
      :userEmail="userEmail"
      :apiUrl="apiUrl"
      @logout="handleLogout"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { tradingAPI, brokerAPI } from './services/api'
import LoginForm from './components/LoginForm.vue'
import AccountDashboard from './components/AccountDashboard.vue'

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

// Authentication state
const isAuthenticated = ref(false)
const sessionId = ref(null)
const userEmail = ref(null)
const apiUrl = ref('http://localhost:5000')

// Theme Management
const THEME_STORAGE_KEY = 'app-theme-preference'
const theme = ref('light')

// Initialize theme with preference priority: localStorage → system preference → light default
const initializeTheme = () => {
  const storedTheme = localStorage.getItem(THEME_STORAGE_KEY)
  
  if (storedTheme) {
    theme.value = storedTheme
  } else {
    // Check system preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    theme.value = prefersDark ? 'dark' : 'light'
  }
}

// Toggle theme and persist to localStorage
const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  localStorage.setItem(THEME_STORAGE_KEY, theme.value)
}

// CSS variables for theme colors
const colorVars = computed(() => {
  const isDark = theme.value === 'dark'
  
  return {
    '--color-bg-primary': isDark ? '#121212' : 'white',
    '--color-bg-secondary': isDark ? '#1e1e1e' : '#f5f5f5',
    '--color-bg-gradient-start': isDark ? '#1a1a2e' : '#667eea',
    '--color-bg-gradient-end': isDark ? '#16213e' : '#764ba2',
    '--color-text-primary': isDark ? '#e0e0e0' : '#333',
    '--color-text-secondary': isDark ? '#bbb' : '#555',
    '--color-text-tertiary': isDark ? '#888' : '#999',
    '--color-primary': isDark ? '#667eea' : '#667eea',
    '--color-primary-light': isDark ? '#7b9dff' : '#667eea',
    '--color-success': isDark ? '#66bb6a' : '#4caf50',
    '--color-success-light': isDark ? '#81c784' : '#c8e6c9',
    '--color-danger': isDark ? '#ef5350' : '#f44336',
    '--color-danger-light': isDark ? '#e57373' : '#ffcdd2',
    '--color-shadow': isDark ? 'rgba(0, 0, 0, 0.3)' : 'rgba(0, 0, 0, 0.1)',
    '--color-border': isDark ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.1)',
    '--color-overlay': isDark ? 'rgba(0, 0, 0, 0.5)' : 'rgba(255, 255, 255, 0.5)',
  }
})

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

// Handle login from LoginForm component
const handleLogin = (loginData) => {
  sessionId.value = loginData.sessionId
  userEmail.value = loginData.email
  isAuthenticated.value = true
}

// Handle logout from AccountDashboard component
const handleLogout = () => {
  sessionId.value = null
  userEmail.value = null
  isAuthenticated.value = false
  // Clear other state
  isConnected.value = false
  balance.value = 0
}

// Check for existing session on mount
const checkExistingSession = () => {
  const storedSessionId = localStorage.getItem('sessionId')
  const storedEmail = localStorage.getItem('userEmail')
  
  if (storedSessionId && storedEmail) {
    sessionId.value = storedSessionId
    userEmail.value = storedEmail
    isAuthenticated.value = true
  }
}

onMounted(() => {
  initializeTheme()
  checkExistingSession()
  if (isAuthenticated.value) {
    fetchStatus()
  }
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
  background: linear-gradient(135deg, var(--color-bg-gradient-start) 0%, var(--color-bg-gradient-end) 100%);
  padding: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: var(--color-text-primary);
  transition: background-color 0.3s ease, color 0.3s ease;
}

.container.dark-mode {
  background: linear-gradient(135deg, var(--color-bg-gradient-start) 0%, var(--color-bg-gradient-end) 100%);
}

/* Toolbar Styles */
.toolbar {
  background: rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--color-border);
  padding: 12px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  box-shadow: 0 4px 6px var(--color-shadow);
  position: sticky;
  top: 0;
  z-index: 100;
  flex-wrap: wrap;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
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
  transition: background 0.3s ease, color 0.3s ease;
}

.status-indicator-toolbar.connected {
  background: rgba(76, 175, 80, 0.3);
  color: var(--color-success-light);
}

.status-indicator-toolbar.disconnected {
  background: rgba(244, 67, 54, 0.3);
  color: var(--color-danger-light);
}

.status-dot-toolbar {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.status-indicator-toolbar.connected .status-dot-toolbar {
  background-color: var(--color-success);
}

.status-indicator-toolbar.disconnected .status-dot-toolbar {
  background-color: var(--color-danger);
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
  color: var(--color-success-light);
}

.btn-connect:hover:not(:disabled) {
  background: rgba(76, 175, 80, 0.5);
  border-color: rgba(76, 175, 80, 0.8);
}

.btn-disconnect {
  background: rgba(244, 67, 54, 0.3);
  border-color: rgba(244, 67, 54, 0.5);
  color: var(--color-danger-light);
}

.btn-disconnect:hover:not(:disabled) {
  background: rgba(244, 67, 54, 0.5);
  border-color: rgba(244, 67, 54, 0.8);
}

/* Theme Toggle Button */
.btn-theme-toggle {
  padding: 8px 12px;
  min-width: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-theme-toggle:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: scale(1.1);
}

.btn-theme-toggle.theme-dark {
  background: rgba(255, 255, 255, 0.2);
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
  background: var(--color-primary);
  border-color: var(--color-primary);
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
  transition: background 0.3s ease, border-color 0.3s ease;
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
  background-color: var(--color-danger);
  color: white;
  padding: 12px 20px;
  margin: 10px;
  border-radius: 6px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(244, 67, 54, 0.3);
  transition: background-color 0.3s ease;
}

/* Sections */
.section {
  background: var(--color-bg-primary);
  border-radius: 12px;
  padding: 30px;
  margin: 20px auto;
  max-width: 600px;
  box-shadow: 0 10px 40px var(--color-shadow);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.section h2 {
  color: var(--color-text-primary);
  margin-bottom: 25px;
  font-size: 1.5rem;
  border-bottom: 2px solid var(--color-primary);
  padding-bottom: 10px;
}

/* Balance Section */
.balance-section {
  background: var(--color-bg-primary);
}

.balance-card-main {
  background: linear-gradient(135deg, var(--color-bg-gradient-start) 0%, var(--color-bg-gradient-end) 100%);
  color: white;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  transition: background 0.3s ease;
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
  background: var(--color-bg-primary);
}

.status-info {
  background-color: var(--color-bg-secondary);
  border-radius: 8px;
  padding: 20px;
  transition: background-color 0.3s ease;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid var(--color-border);
  transition: border-color 0.3s ease;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 600;
  color: var(--color-text-secondary);
}

.text-success {
  color: var(--color-success);
  font-weight: 600;
}

.text-danger {
  color: var(--color-danger);
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
