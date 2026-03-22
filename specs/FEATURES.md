# Trading Platform Feature Specifications - iQOption Integration

## Feature 1: iQOption Broker Login

### Requirement
User can authenticate with their iQOption account credentials and establish a broker session.

### Acceptance Criteria
- [x] User can enter email and password in LoginForm component
- [x] Form validates email format and password requirements
- [x] User can submit login form
- [x] LoginForm shows loading indicator during authentication
- [x] On successful login, session token is stored in localStorage
- [x] On successful login, user is shown AccountDashboard
- [x] Error messages display on authentication failure
- [x] Form fields are cleared on successful submission
- [x] Session expiration handled (30-minute default)

### API Endpoints
- `POST /api/broker/login` - Authenticate with iQOption broker

### Request/Response
```json
LOGIN REQUEST:
{
  "email": "user@example.com",
  "password": "password123"
}

LOGIN RESPONSE (200):
{
  "success": true,
  "sessionId": "session_token_xyz",
  "broker": "iQOption",
  "mode": "demo",
  "timestamp": "2026-03-23T10:30:00Z"
}
```

### UI Components Affected
- LoginForm.vue (Input fields and submission)
- App.vue (Auth state management)

### Testing Scenarios
1. **Happy Path**: Valid credentials → Successful login → Dashboard shown
2. **Invalid Email**: Invalid format → Validation error before submission
3. **Wrong Password**: Valid email, wrong password → 401 error displayed
4. **Missing Fields**: Empty email/password → Form validation error
5. **Network Error**: API unavailable → Error message displayed

---

## Feature 2: iQOption Broker Logout

### Requirement
User can safely disconnect from their iQOption session and clear all broker data.

### Acceptance Criteria
- [x] Logout button available in AccountDashboard
- [x] On logout click, session is terminated with broker
- [x] Session token removed from localStorage
- [x] User returned to LoginForm
- [x] Balance and mode data cleared
- [x] Logout completes within 2 seconds

### API Endpoints
- `POST /api/broker/logout` - Terminate broker session

### Response
```json
{
  "success": true,
  "message": "Successfully logged out",
  "timestamp": "2026-03-23T10:35:00Z"
}
```

### UI Components Affected
- AccountDashboard.vue (Logout button)
- App.vue (Auth state reset)

### Testing Scenarios
1. **Standard Logout**: Click logout → Session cleared → LoginForm shown
2. **Session Expired**: Auto-logout on expired session → LoginForm shown
3. **Logout Error**: Broker API fails → Error displayed but state cleared locally

---

## Feature 3: Account Balance Display

### Requirement
System displays current iQOption account balance based on trading mode in real-time.

### Acceptance Criteria
- [x] Balance displays in AccountDashboard after login
- [x] Balance reflects current trading mode (demo/live)
- [x] Currency symbol (USD) displayed
- [x] Format: $X,XXX.XX (with proper decimal places)
- [x] Balance updates when mode is switched
- [x] Last-updated timestamp included in response
- [x] Handles missing/null balance gracefully
- [x] Balance auto-refreshes on page load for authenticated users

### API Endpoints
- `GET /api/broker/balance` - Fetch account balance

### Response
```json
{
  "success": true,
  "balance": 10000.50,
  "currency": "USD",
  "mode": "demo",
  "lastUpdated": "2026-03-23T10:30:45Z",
  "timestamp": "2026-03-23T10:30:50Z"
}
```

### UI Components Affected
- AccountDashboard.vue (Balance display)
- App.vue (Balance state management)

### Business Rules
- Demo mode balance: Starting from $10,000
- Live mode balance: User's actual account balance
- Updates on every mode switch
- Cached for performance (with TTL)

### Testing Scenarios
1. **Connect and Check**: Login → Balance displays
2. **Mode Switch**: Switch modes → Balance updates immediately
3. **Page Reload**: Refresh page → Balance persists from localStorage
4. **API Failure**: Balance fetch fails → Error shown, balance stays visible
5. **Real-time Updates**: Multiple rapid fetches work correctly

---

## Feature 4: Demo/Live Mode Switching

### Requirement
User can switch between demo (practice) and live (real money) trading modes.

### Acceptance Criteria
- [x] Mode selector (demo/live toggle or dropdown) in AccountDashboard
- [x] Current mode prominently displayed
- [x] User can click to switch modes
- [x] Confirmation dialog shown before switching to live mode
- [x] Balance updates to reflect new mode balance after switch
- [x] Mode preference stored in backend session
- [x] Mode persists across page reloads
- [x] Switching completes within 1 second
- [x] Live mode has warning/visual distinction

### API Endpoints
- `POST /api/broker/mode/switch` - Change trading mode

### Request/Response
```json
SWITCH REQUEST:
{
  "mode": "live"
}

SWITCH RESPONSE (200):
{
  "success": true,
  "mode": "live",
  "balance": 50000.00,
  "currency": "USD",
  "timestamp": "2026-03-23T10:35:00Z"
}
```

### UI Components Affected
- AccountDashboard.vue (Mode selector and display)
- App.vue (Mode state management)

### Business Rules
- Demo mode: Safe practice environment
- Live mode: Real trading with actual money
- Confirmation required before live mode
- Mode stored in session (backend session storage)

### Testing Scenarios
1. **Demo to Live**: Switch demo → live → Confirmation shown → Balance updates
2. **Live to Demo**: Switch live → demo → No confirmation needed → Balance updates
3. **Rapid Switching**: Quick mode switches handled gracefully
4. **Persistence**: Switch mode → Reload page → Mode persists
5. **Error Recovery**: Mode switch fails → State reverts to previous mode

---

## Integration Workflows

### Workflow 1: App Launch
1. App mounts (App.vue)
2. Check localStorage for sessionId
3. If sessionId exists: Auto-login (validate session)
4. If no sessionId: Show LoginForm
5. Fetch balance and mode for authenticated user

### Workflow 2: User Login
1. User enters email and password in LoginForm
2. Form validates input
3. POST /api/broker/login with credentials
4. Backend returns sessionId
5. sessionId stored in localStorage
6. App state updated with auth=true
7. AccountDashboard displays with balance and mode

### Workflow 3: User Switches Mode
1. User clicks mode toggle in AccountDashboard
2. If switching to live: Confirmation dialog shown
3. POST /api/broker/mode/switch with new mode
4. Backend updates session mode
5. GET /api/broker/balance called automatically
6. Balance updates in UI
7. Mode updates in all components

### Workflow 4: User Logout
1. User clicks Logout button
2. POST /api/broker/logout called
3. Backend clears session
4. sessionId removed from localStorage
5. App state reset to auth=false
6. LoginForm displayed

### Workflow 5: Session Expiration
1. API request returns 401 (Not authenticated)
2. Backend session expired (default: 30 minutes)
3. Frontend detects 401 and calls logout
4. User returned to LoginForm
5. Error message: "Session expired. Please login again."

---

## Error Handling

### Authentication Errors
- **Invalid Credentials**: 401 response → Show "Invalid email or password"
- **Missing Fields**: 400 response → Show form validation errors
- **Network Error**: Connection failed → Show "Unable to connect to broker"

### Balance Fetch Errors
- **Not Authenticated**: 401 response → Auto-logout triggered
- **Broker Error**: 500 response → Show "Failed to fetch balance, please try again"
- **Timeout**: Request timeout → Show cached balance or error

### Mode Switch Errors
- **Invalid Mode**: 400 response → Show "Invalid trading mode"
- **Not Authenticated**: 401 response → Auto-logout triggered
- **Broker Error**: 500 response → Show "Failed to switch mode, please try again"
- **Already in Mode**: User tries to switch to current mode → No action needed

### Session Expiration
- **Expired Session**: Any 401 response → Auto-logout to LoginForm
- **Default Timeout**: 30 minutes of inactivity
- **Clear Message**: "Your session has expired. Please login again."

---

## Performance Requirements

- Login: < 3 seconds response time
- Logout: < 1 second response time
- Balance Fetch: < 1 second response time
- Mode Switch: < 1 second response time
- Page Load (authenticated): < 2 seconds to show account dashboard
- Session Validation: < 500ms on app load

---

## Security Requirements

- Passwords transmitted over HTTPS only
- Session tokens stored securely in localStorage (httpOnly not possible in SPA)
- CORS configured for trusted origins only
- Session expiration: 30 minutes default
- Rate limiting on login attempts (max 5 attempts per minute)
- Credentials never logged or exposed in console
- UI Update: Immediate (client-side)
- Animation Smoothness: 60 FPS (CSS animations)

---

## Security Requirements

- No sensitive data stored in browser localStorage
- Connection state managed in-memory only
- Account type transmitted over HTTPS in production
- Input validation on account type (only 'demo' or 'real')
