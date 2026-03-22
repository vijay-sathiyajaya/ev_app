## ADDED Requirements

### Requirement: User can switch between demo and live trading modes
The system SHALL allow authenticated users to toggle between demo and live trading accounts, with the active mode persisted across sessions.

#### Scenario: User switches from demo to live mode
- **WHEN** user selects live mode from the mode selector
- **THEN** system switches active account to live trading mode and updates the balance accordingly

#### Scenario: User switches from live to demo mode
- **WHEN** user selects demo mode from the mode selector
- **THEN** system switches active account to demo trading mode and refreshes balance display

#### Scenario: Mode switch is confirmed before execution
- **WHEN** user attempts to switch modes
- **THEN** system may display confirmation dialog warning about real money (live mode)

#### Scenario: Current mode is displayed in UI
- **WHEN** user views the application
- **THEN** current trading mode (demo or live) is clearly visible and selectable

### Requirement: REST API endpoint for mode switching
The system SHALL expose a `/api/broker/mode/switch` endpoint that changes the active trading mode.

#### Scenario: POST /api/broker/mode/switch changes mode
- **WHEN** frontend POSTs `{mode: "live"}` to `/api/broker/mode/switch`
- **THEN** backend switches iqOption session to live mode and returns updated account state

#### Scenario: Mode switch validates requested mode
- **WHEN** frontend submits invalid mode value
- **THEN** backend returns HTTP 400 with error message (valid modes: "demo", "live")

#### Scenario: Mode switch requires valid session
- **WHEN** frontend requests mode switch with invalid or expired session
- **THEN** backend returns HTTP 401 Unauthorized

### Requirement: Mode preference is persisted
The system SHALL store the user's preferred trading mode and restore it on next login.

#### Scenario: Mode selection is saved after switch
- **WHEN** user switches to live mode
- **THEN** system saves this preference associated with user session

#### Scenario: Preferred mode is restored on next login
- **WHEN** user logs in again
- **THEN** system restores the previously selected trading mode

### Requirement: Balance updates reflect active mode
The system SHALL fetch and display balance specific to the currently active trading mode.

#### Scenario: Balance reflects demo mode account
- **WHEN** demo mode is active
- **THEN** displayed balance is from the demo trading account

#### Scenario: Balance reflects live mode account
- **WHEN** live mode is active
- **THEN** displayed balance is from the live trading account

#### Scenario: Mode-specific balance is cached appropriately
- **WHEN** user switches between modes
- **THEN** system caches balances for both modes to avoid repeated API calls

### Requirement: Frontend displays mode selector
The system SHALL provide a clear interface element for switching between demo and live modes.

#### Scenario: Mode selector is accessible to authenticated users
- **WHEN** user is logged in
- **THEN** mode selector (dropdown or toggle) is visible and enabled

#### Scenario: Mode selector shows current active mode
- **WHEN** user views the mode selector
- **THEN** current mode selection is highlighted or indicated as active

#### Scenario: Live mode is visually distinguished
- **WHEN** mode selector is available
- **THEN** live mode option is clearly marked (e.g., warning icon or red highlight) to indicate real money usage
