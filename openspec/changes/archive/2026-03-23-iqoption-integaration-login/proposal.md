## Why

The iqOption broker integration requires robust login and account management functionality to enable users to connect their trading accounts, seamlessly switch between demo and live trading modes, and manage account balance information. This foundational capability is essential for the broker integration to be functional and user-friendly.

## What Changes

- **Login/Connection**: Add support for connecting to iqOption broker with user credentials
- **Logout/Disconnection**: Add support for disconnecting from iqOption broker sessions
- **Balance Display**: Fetch and display account balance for the currently connected account
- **Demo/Live Mode Switching**: Enable users to switch between demo and live trading accounts with associated balance updates
- **Session Management**: Maintain broker connection state and handle reconnection scenarios

## Capabilities

### New Capabilities
- `iqoption-login`: User authentication and connection to iqOption broker accounts
- `iqoption-logout`: Session cleanup and disconnection from iqOption broker
- `account-balance-management`: Fetch, display, and manage account balance information
- `demo-live-mode-switching`: Toggle between demo trading and live trading account modes

### Modified Capabilities
<!-- None at this time -->

## Impact

- **Backend**: Python backend (main.py) will need iqOption SDK integration, credential management, and API endpoints for login/logout/balance operations
- **Frontend**: Vue.js frontend (App.vue, services/api.js) will need UI components for login form, account selector, balance display, and demo/live mode toggle
- **APIs**: New REST endpoints for iqOption broker operations (connect, disconnect, get balance, switch mode)
- **Dependencies**: iqOption Python SDK or API wrapper library will need to be added to requirements.txt
