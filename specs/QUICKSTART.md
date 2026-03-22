# OpenSpec Quick Start Guide - iQOption Trading Platform

## What is OpenSpec?
OpenSpec is a lightweight spec-driven framework for building software with clear specifications and requirements.

## Project Setup Complete ✅

Your trading application with iQOption broker integration is now configured with OpenSpec specifications.

## Directory Structure

```
d:\app\ev_app/
├── openspec.config.json          # OpenSpec configuration
├── specs/                         # All specifications
│   ├── api.openapi.yml           # API specification (OpenAPI 3.0) - iQOption endpoints
│   ├── COMPONENTS.md             # UI component specs (LoginForm, AccountDashboard)
│   ├── FEATURES.md               # Feature specifications (Login, Logout, Balance, Mode)
│   └── QUICKSTART.md             # This file
├── backend/
│   ├── main.py                   # Flask app with iQOption endpoints
│   ├── iqoption_client.py        # iQOption SDK wrapper
│   ├── session_manager.py        # Session management
│   ├── credential_store.py       # Secure credential handling
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.vue               # Root component with auth state
│   │   ├── components/
│   │   │   ├── LoginForm.vue     # iQOption login form
│   │   │   └── AccountDashboard.vue # Account & balance display
│   │   └── services/
│   │       └── api.js            # API client for broker endpoints
│   ├── package.json              # Frontend dependencies
│   └── vite.config.js            # Vite configuration
├── openspec/changes/archive/     # Archived completed changes
└── README.md                     # Project documentation
```

## Key Features Implemented

### 1. iQOption Broker Authentication ✅
- **Endpoint**: `POST /api/broker/login`
- **Component**: `LoginForm.vue`
- **Functionality**: User authenticates with iQOption email/password
- **Session Management**: 30-minute session tokens, httpOnly cookies

### 2. Account Logout ✅
- **Endpoint**: `POST /api/broker/logout`
- **Functionality**: Secure session termination
- **Cleanup**: Session tokens cleared, localStorage cleaned

### 3. Balance Management ✅
- **Endpoint**: `GET /api/broker/balance`
- **Component**: `AccountDashboard.vue`
- **Functionality**: Real-time balance display in USD
- **Features**: Balances for both demo and live modes

### 4. Demo/Live Mode Switching ✅
- **Endpoint**: `POST /api/broker/mode/switch`
- **Functionality**: Switch between demo (practice) and live (real money) trading
- **Confirmation**: Dialog confirmation before switching to live
- **Balance Update**: Automatic balance refresh after mode switch

## Configuration Files

### 1. `specs/api.openapi.yml`
Complete API specification following OpenAPI 3.0.0 standard.

**Endpoints Documented:**
- `POST /api/broker/login` - Authenticate with iQOption
- `POST /api/broker/logout` - Terminate session
- `GET /api/broker/balance` - Fetch account balance
- `POST /api/broker/mode/switch` - Switch trading mode

**Request/Response Examples:**
```json
LOGIN:
POST /api/broker/login
{
  "email": "user@example.com",
  "password": "password"
}

RESPONSE:
{
  "success": true,
  "sessionId": "token_xyz",
  "broker": "iQOption",
  "mode": "demo"
}
```

### 2. `specs/FEATURES.md`
Complete feature specifications including:
- Feature 1: iQOption Broker Login (Auth, Session, Validation)
- Feature 2: iQOption Broker Logout (Session Cleanup)
- Feature 3: Account Balance Display (Real-time updates)
- Feature 4: Demo/Live Mode Switching (Confirmation, Balance refresh)
- Integration workflows (App Launch, Login, Mode Switch, Logout, Session Expiry)
- Error handling for all scenarios
- Performance and security requirements

### 3. `specs/COMPONENTS.md`
UI component specifications:
- **LoginForm.vue**: Email/password inputs, validation, error display
- **AccountDashboard.vue**: Balance display, mode selector, logout button
- **App.vue**: Root component with auth state management
- **Error Banner**: Global error notifications
- Accessibility requirements (ARIA labels, WCAG compliance)
- Security considerations (no password logging, HTTPS, input validation)

### 4. Backend Implementation

#### `backend/main.py`
Flask application with endpoints:
```python
@app.route('/api/broker/login', methods=['POST'])
@app.route('/api/broker/logout', methods=['POST'])
@app.route('/api/broker/balance', methods=['GET'])
@app.route('/api/broker/mode/switch', methods=['POST'])
```

#### `backend/iqoption_client.py`
iQOption SDK wrapper with methods:
- `connect()` - Authenticate with broker
- `get_balance()` - Fetch current balance
- `switch_mode(mode)` - Switch demo/live
- `disconnect()` - Close broker connection

#### `backend/session_manager.py`
Session management with features:
- Session token generation
- Session storage and retrieval
- Session expiration (30 minutes)
- Session cleanup

#### `backend/credential_store.py`
Secure credential handling:
- Secure credential storage
- Credential retrieval
- Encryption for sensitive data

## Environment Setup

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (.env file)
IQOPTION_KEY=your_api_key
SESSION_TIMEOUT=1800
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## API Usage Examples

### 1. Login
```javascript
// frontend/src/services/api.js
const response = await fetch('/api/broker/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password'
  })
});
const data = await response.json();
localStorage.setItem('sessionId', data.sessionId);
```

### 2. Get Balance
```javascript
const response = await fetch('/api/broker/balance', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${sessionId}`
  }
});
const { balance, mode, currency } = await response.json();
```

### 3. Switch Mode
```javascript
const response = await fetch('/api/broker/mode/switch', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ mode: 'live' })
});
const { balance, mode } = await response.json();
```

### 4. Logout
```javascript
await fetch('/api/broker/logout', { method: 'POST' });
localStorage.removeItem('sessionId');
```

## Running Tests

### Backend Tests
```bash
cd backend
pytest test_iqoption_api.py -v
```

### Frontend Development
```bash
cd frontend
npm run dev
```

## Next Steps

1. **Environment Variables**: Configure `.env` file with iQOption credentials
2. **Database Setup**: Set up session storage (in-memory or database)
3. **Testing**: Run comprehensive tests (login, balance, mode switching)
4. **Deployment**: Deploy to staging/production with proper SSL/HTTPS

## Documentation References

- **OpenAPI Spec**: `specs/api.openapi.yml` - Full API documentation
- **Features**: `specs/FEATURES.md` - Business requirements and acceptance criteria
- **Components**: `specs/COMPONENTS.md` - UI component specifications
- **README**: `README.md` - Project overview and setup instructions

## Change History

### Archived Changes
- ✅ **iqoption-integaration-login** (2026-03-23): Login, logout, balance, and mode switching implementation
- ✅ **add-iqoption-broker-integration** (2026-03-23): Broker integration setup
Vue component specifications with:
- Component structure
- Props definition
- Event/method specifications
- Responsive breakpoints
- Accessibility requirements

**Components Documented:**
- Toolbar (Navigation & Quick Actions)
- Balance Card (Display)
- Status Information (Details)
- Error Banner (Alerts)

### 4. `specs/FEATURES.md`
Feature requirements with:
- Acceptance criteria (checkboxes)
- Workflows
- Integration points
- Error handling
- Performance/Security requirements

## OpenSpec Commands

```bash
# Check project status
openspec status

# Create a new spec-based change
openspec new change <feature-name>

# View specification
openspec view <spec-file>

# Validate specifications
openspec validate

# Generate documentation
openspec docs
```

## How to Use

### 1. Define Specifications First
Before implementing features:
- Write acceptance criteria in `specs/FEATURES.md`
- Define API in `specs/api.openapi.yml`
- Document components in `specs/COMPONENTS.md`

### 2. Track Changes
```bash
openspec new change "Add two-factor authentication"
```

### 3. Implement According to Specs
- Follow component specifications
- Implement only what's specified
- Test against acceptance criteria

### 4. Validate Implementation
- All acceptance criteria met
- Code follows specified style
- API matches OpenAPI spec

## Continuous Development Workflow

```
1. Request Feature
   ↓
2. Write Specification (FEATURES.md)
   ↓
3. Create Change Tracking (openspec new change)
   ↓
4. Implement Code
   ↓
5. Test Against Spec
   ↓
6. Update API Spec if needed
   ↓
7. Document in Changelog
```

## Current Implementation Status

### Implemented Features
- ✅ Broker Connection (Connect/Disconnect)
- ✅ Account Switching (Demo/Real)
- ✅ Balance Display (Toolbar + Card)
- ✅ Status Indicator (Visual feedback)
- ✅ Top Toolbar (Navigation & Actions)

### Specification Coverage
- ✅ API Endpoints (OpenAPI 3.0)
- ✅ Component Structure
- ✅ Feature Requirements
- ✅ Error Handling
- ✅ Responsive Design

## Next Steps

1. **Review Specifications**
   - Read FEATURES.md for all acceptance criteria
   - Check COMPONENTS.md for UI specifications
   - Review api.openapi.yml for API contracts

2. **Run Tests Against Spec**
   ```bash
   npm test
   ```

3. **Add New Features**
   ```bash
   openspec new change "Feature name"
   ```

4. **Generate API Documentation**
   ```bash
   openspec docs
   ```

## Tips & Best Practices

### ✅ Do
- Write specs before implementation
- Use acceptance criteria as test cases
- Update specs when requirements change
- Reference specs in code comments
- Keep specs version-controlled

### ❌ Don't
- Implement features without specs
- Leave specs outdated
- Deviate from specifications without updating docs
- Skip error scenarios
- Ignore accessibility requirements

## Resources

- **OpenSpec Documentation**: https://openspec.dev
- **OpenAPI Documentation**: https://spec.openapis.org/
- **Vue 3 Guide**: https://vuejs.org/
- **Project README**: See root README.md

## Configuration Details

- **Framework**: OpenSpec 1.0.0
- **API Standard**: OpenAPI 3.0.0
- **Frontend**: Vue 3 with Composition API
- **Backend**: Flask with REST
- **Testing**: Spec-based acceptance testing
- **Styling**: Spec-defined CSS standards

## Support

For issues or clarifications:
1. Check `openspec.config.json` for project settings
2. Review relevant spec file (FEATURES.md, COMPONENTS.md, api.openapi.yml)
3. Check error messages in banners
4. Review console logs for debugging info
