## ADDED Requirements

### Requirement: User can authenticate with iqOption credentials
The system SHALL authenticate users by accepting their iqOption email/username and password, establishing a valid session token with the iqOption broker.

#### Scenario: Successful login with valid credentials
- **WHEN** user submits valid iqOption email and password through the login form
- **THEN** system establishes connection to iqOption broker and returns a valid session token

#### Scenario: Login fails with invalid credentials
- **WHEN** user submits incorrect email or password
- **THEN** system returns an authentication failure message without creating a session

#### Scenario: Login fails due to broker unavailability
- **WHEN** iqOption broker service is temporarily unavailable
- **THEN** system returns a service unavailability error message and suggests retry

### Requirement: Backend validates and stores session credentials
The system SHALL securely store iqOption session tokens on the backend server and validate token freshness before executing broker operations.

#### Scenario: Session token is stored after successful authentication
- **WHEN** user authenticates successfully
- **THEN** backend stores encrypted session token with expiration timestamp

#### Scenario: Invalid or expired token is rejected
- **WHEN** frontend requests an operation with an expired session token
- **THEN** system returns 401 Unauthorized and prompts user to re-authenticate

### Requirement: Frontend displays login form
The system SHALL provide a user-friendly login form on the frontend for entering iqOption credentials.

#### Scenario: Login form is accessible on application load
- **WHEN** application loads without active session
- **THEN** login form is displayed with email and password input fields

#### Scenario: Login in progress indicator
- **WHEN** user submits credentials
- **THEN** system displays loading indicator until authentication completes

#### Scenario: User is redirected after successful login
- **WHEN** authentication succeeds
- **THEN** login form is hidden and user is logged into the application

### Requirement: REST API endpoint for login
The system SHALL expose a `/api/broker/login` endpoint that accepts credentials and returns session information.

#### Scenario: POST /api/broker/login with valid credentials
- **WHEN** frontend POSTs `{email: "user@example.com", password: "pass"}` to `/api/broker/login`
- **THEN** backend returns `{status: "authenticated", sessionId: "token123", mode: "demo"}`

#### Scenario: POST /api/broker/login returns error on invalid input
- **WHEN** frontend submits empty or malformed credentials
- **THEN** backend returns HTTP 400 with error message
