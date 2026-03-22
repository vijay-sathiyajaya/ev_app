## ADDED Requirements

### Requirement: User can logout from iqOption broker
The system SHALL terminate the iqOption session when user initiates logout, clearing all stored session tokens and resetting the application state.

#### Scenario: Successful logout from logged-in state
- **WHEN** user clicks logout button in the application
- **THEN** system terminates iqOption broker session and clears frontend session storage

#### Scenario: Login form is displayed after logout
- **WHEN** logout completes successfully
- **THEN** application returns to login form state

#### Scenario: Logout handles already-expired sessions gracefully
- **WHEN** user attempts logout but session is already expired on broker
- **THEN** system clears local session state without throwing errors

### Requirement: REST API endpoint for logout
The system SHALL expose a `/api/broker/logout` endpoint that properly terminates the broker session.

#### Scenario: POST /api/broker/logout invalidates session
- **WHEN** frontend POSTs to `/api/broker/logout` with valid sessionId
- **THEN** backend terminates broker connection and returns `{status: "logged_out"}`

#### Scenario: Logout endpoint validates session before terminating
- **WHEN** frontend submits logout with invalid or missing sessionId
- **THEN** backend returns HTTP 401 and user remains logged out

### Requirement: Session cleanup on server
The system SHALL clean up session data on the backend after logout, removing cached credentials and tokens.

#### Scenario: Server-side session data is removed after logout
- **WHEN** logout request is processed
- **THEN** backend removes stored session token and clears any cached broker data

#### Scenario: Subsequent requests use new session after logout
- **WHEN** user logs in again after logout
- **THEN** a new session token is generated and broker connection is re-established
