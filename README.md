# Trading Application

A full-stack trading application with real-time broker connection management and account switching capabilities.

## Project Structure

```
ev_app/
├── frontend/              # Vue 3 + Vite frontend application
│   ├── src/
│   │   ├── services/      # API service for backend communication
│   │   │   └── api.js     # Trading API client
│   │   ├── App.vue        # Main trading dashboard
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
│
└── backend/               # Python Flask backend service
    ├── main.py           # Flask app with trading APIs
    ├── requirements.txt
    └── .env              # Environment variables
```

## Getting Started

### Step 1: Backend Setup (Python)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python main.py
```

The Flask server will start at `http://localhost:5000`

### Step 2: Frontend Setup (Vue 3)

In a **new terminal window**:

```bash
cd frontend
npm install
npm run dev
```

The Vue development server will start at `http://localhost:3000`

### Step 3: Access the Application

Open your browser and navigate to `http://localhost:3000`

## Features

### 1. Broker Connection Management
- **Connect/Disconnect Button**: Establish or terminate connection to a trading broker
- **Connection Status Indicator**: Real-time visual indicator showing connection status
- Dummy API for immediate testing - ready for real broker implementation

### 2. Account Type Switching
- **Switch Between Account Types**: Toggle between Demo and Real accounts
- **Persistent Account State**: Account selection persists across operations
- Safe switching with proper validation

### 3. Available Balance Display
- **Real-time Balance Updates**: Display balance based on selected account type
- **Demo Account**: $10,000.00 (default)
- **Real Account**: $50,000.00 (default)
- Beautiful balance card with account information

### 4. iqOption Broker Integration (NEW)
- **Secure Login**: Authenticate with iqOption broker credentials
- **Demo & Live Mode**: Switch between demo trading (virtual money) and live trading (real money)
- **Account Balance**: Real-time balance display for current account
- **Session Management**: Secure session tokens with automatic expiration
- **Encrypted Credentials**: Credentials stored securely on backend

## iqOption Setup Guide

### Prerequisites
- Active iqOption trading account (https://iqoption.com)
- iqOption credentials (email/password)

### Backend Configuration

1. **Set Environment Variables** (`backend/.env`):

```env
# iqOption Configuration
IQOPTION_API_ENDPOINT=https://api.iqoption.com
IQOPTION_WS_ENDPOINT=wss://wsapi.iqoption.com
SESSION_TIMEOUT_MINUTES=30

# Credential Encryption (Generate a new key)
CREDENTIAL_ENCRYPTION_KEY=<your-generated-key>
```

2. **Generate Encryption Key**:

```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())  # Copy this to CREDENTIAL_ENCRYPTION_KEY in .env
```

3. **Install Dependencies**:

```bash
cd backend
pip install -r requirements.txt
```

### Frontend Features
- **Login Form**: Email and password input with validation
- **Account Dashboard**: 
  - Display current account balance
  - Switch between demo and live trading modes
  - Logout button for session management
- **Auto-session Restore**: Automatically restores session from localStorage on page reload

### Usage Flow

1. **Start Backend** (port 5000):
   ```bash
   cd backend
   python main.py
   ```

2. **Start Frontend** (port 3000):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Login**:
   - Enter your iqOption email and password
   - Click "Sign In"
   - Session ID is automatically stored

4. **Manage Account**:
   - View balance for current trading mode (demo or live)
   - Click refresh button to update balance
   - Switch between modes using the mode selector
   - **WARNING**: Live mode uses real money!

5. **Logout**:
   - Click logout button
   - Session is cleared and you return to login form

## Backend API Endpoints

### Health & Status
- `GET /api/health` - Check backend health status
- `GET /api/data` - Get sample data

### Trading Endpoints
All trading endpoints are under `/api/trading`

#### Connection Management
- **GET** `/api/trading/status`
  - Returns: Current connection status, account type, broker name
  - Response: `{ connected, account_type, broker, timestamp }`

- **POST** `/api/trading/connect`
  - Request: `{ broker: "Broker Name" }`
  - Returns: `{ success, message, connected, broker, timestamp }`

- **POST** `/api/trading/disconnect`
  - Returns: `{ success, message, connected, timestamp }`

#### Account Management
- **GET** `/api/trading/account?type=demo`
  - Query Params: `type` (demo or real)
  - Returns: `{ account_type, balance, currency, connected, timestamp }`

- **POST** `/api/trading/account/switch`
  - Request: `{ account_type: "demo" or "real" }`
  - Returns: `{ success, message, account_type, balance, timestamp }`

## API Service (Frontend)

The `src/services/api.js` includes a `tradingAPI` client with methods:

```javascript
// Get current trading status
tradingAPI.getStatus()

// Connect to broker
tradingAPI.connectBroker(brokerName)

// Disconnect from broker
tradingAPI.disconnectBroker()

// Get account information
tradingAPI.getAccount(accountType)

// Switch account type
tradingAPI.switchAccount(accountType)
```

## Configuration

### Backend (.env)
```
PORT=5000
```

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:5000
```

## Current State

- ✅ Full UI for trading dashboard
- ✅ Dummy backend APIs (ready for real implementation)
- ✅ Account switching functionality
- ✅ Balance display system
- ✅ Connection management UI
- ✅ Error handling and loading states
- ✅ Responsive design

## Next Steps for Implementation

1. Replace dummy backend with real broker API integration
2. Add real account verification
3. Implement real balance feeds
4. Add trading order functionality
5. Implement price charts and market data
6. Add user authentication
7. Implement transaction history

## Technology Stack

- **Frontend**: Vue 3, Vite, JavaScript
- **Backend**: Flask (Python), Flask-CORS
- **API Communication**: Fetch API
- **Styling**: CSS3 with Flexbox and Gradients
