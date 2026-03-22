## Context

The iqOption broker integration needs a complete login/connection workflow that supports multiple trading modes and account management. The application has a Python backend (main.py) handling broker operations and a Vue.js frontend (App.vue) providing the user interface. The integration must handle credential management, session persistence, and seamless switching between demo and live trading modes.

## Goals / Non-Goals

**Goals:**
- Establish secure authentication with iqOption broker
- Support both demo and live account modes with easy switching
- Display current account balance in real-time
- Maintain session state across frontend reloads
- Handle connection failures and reconnection gracefully
- Provide clear feedback to users on connection status

**Non-Goals:**
- Advanced portfolio analytics (out of scope for login feature)
- Multi-account simultaneous connections (single active account per session)
- Custom credential encryption (use backend session management)
- Trading execution from frontend (backend-only operations)

## Decisions

**1. Backend Architecture - Session-Based Authentication**
- Decision: Store iqOption credentials and session tokens in backend Python server
- Rationale: Credentials should never be exposed to frontend; server-side management is more secure
- Alternative considered: Token passed to frontend - rejected due to security concerns

**2. Frontend-Backend Communication**
- Decision: Use REST API endpoints for login, balance sync, and mode switching
- Rationale: Aligns with existing API infrastructure (services/api.js), simple polling for balance updates
- Endpoints needed: POST /api/broker/login, POST /api/broker/logout, GET /api/broker/balance, POST /api/broker/mode/switch

**3. Session Persistence**
- Decision: Store active session ID in localStorage on frontend, verify validity on backend per request
- Rationale: Survives page reloads; server validates token freshness
- Fallback: Auto-logout if session expires (user re-authenticates)

**4. Demo vs Live Mode Storage**
- Decision: Store current mode preference on backend per session, return in balance/status API calls
- Rationale: Prevents frontend from independently changing modes; single source of truth
- UI: Dropdown or toggle button on frontend querying current mode and allowing switches

**5. iqOption SDK Integration**
- Decision: Use official iqOption Python SDK (python-iqoption) or REST API wrapper
- Rationale: Mature library with authentication, balance, and mode-switching support
- Added to requirements.txt for pip installation

## Risks / Trade-offs

**[Risk] Credential leakage in logs or error messages**
→ Mitigation: Sanitize error responses, never log full credentials, use secure session tokens

**[Risk] Session timeout misalignment between frontend and iqOption**
→ Mitigation: Validate session health before each operation, graceful re-auth on invalidation

**[Risk] Balance data staleness during rapid mode switches**
→ Mitigation: Accept eventual consistency; fetch fresh balance immediately after mode switch API call

**[Risk] Dependency on external iqOption API availability**
→ Mitigation: Implement retry logic with exponential backoff, inform user of service unavailability

## Migration Plan

1. Install iqOption SDK: `pip install python-iqoption`
2. Add backend API endpoints in main.py
3. Add frontend login form component to App.vue
4. Add API service methods to services/api.js
5. Deploy and test with demo account first
6. Update README with setup instructions (iqOption credentials, API endpoint documentation)

## Open Questions

- Should we cache balance data or always fetch fresh? (Currently: always fetch)
- What's the session timeout duration? (Default: 30 minutes suggested)
- Should demo and live mode selections be persisted across sessions? (Default: yes)
