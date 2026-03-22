## ADDED Requirements

### Requirement: System retrieves current account balance
The system SHALL fetch the current account balance from iqOption broker for the authenticated user and display it in the frontend.

#### Scenario: Balance is retrieved for logged-in user
- **WHEN** user is authenticated and views the account panel
- **THEN** system displays current account balance from iqOption broker

#### Scenario: Balance updates when account is accessed
- **WHEN** user refreshes the page or triggers balance sync
- **THEN** system fetches fresh balance from broker and displays updated value

#### Scenario: Balance retrieval fails gracefully with broker error
- **WHEN** iqOption broker returns an error fetching balance
- **THEN** system displays a cached balance (if available) with a "last updated" timestamp or error message

### Requirement: REST API endpoint for balance retrieval
The system SHALL expose a `/api/broker/balance` endpoint that returns current account balance and account information.

#### Scenario: GET /api/broker/balance returns current balance
- **WHEN** frontend GETs `/api/broker/balance` with valid session
- **THEN** backend returns `{balance: 5000.50, currency: "USD", mode: "demo", lastUpdated: "2026-03-23T10:30:00Z"}`

#### Scenario: Balance endpoint validates session
- **WHEN** frontend requests balance with invalid or expired session
- **THEN** backend returns HTTP 401 Unauthorized

### Requirement: Balance is mode-specific
The system SHALL maintain separate balance values for demo and live trading modes.

#### Scenario: Balance changes when switching trading modes
- **WHEN** user switches from demo mode to live mode
- **THEN** system displays the balance for live account (different from demo balance)

#### Scenario: Balance display reflects current mode
- **WHEN** balance is retrieved
- **THEN** returned data includes which mode (demo/live) the balance represents

### Requirement: Frontend displays balance prominently
The system SHALL show account balance in the user interface with currency information.

#### Scenario: Balance is visible in account dashboard
- **WHEN** user is authenticated
- **THEN** account balance is displayed in a prominent location (e.g., header or account panel)

#### Scenario: Balance includes currency information
- **WHEN** balance is displayed
- **THEN** currency symbol or code is shown alongside the numeric value (e.g., "$5,000.50" or "5000.50 USD")
