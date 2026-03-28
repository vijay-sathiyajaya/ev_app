## ADDED Requirements

### Requirement: Deduct investment from balance on order placement
The system SHALL immediately deduct the investment amount from the user's account balance when an order is placed, before any resolution occurs.

#### Scenario: Balance deduction on UP order
- **WHEN** balance is $5,000 and user places a $100 UP order
- **THEN** the balance immediately updates to $4,900
- **AND** the balance display in the header updates instantly

#### Scenario: Balance deduction on DOWN order
- **WHEN** balance is $4,900 and user places a $200 DOWN order
- **THEN** the balance immediately updates to $4,700

#### Scenario: Multiple orders deduct sequentially
- **WHEN** user places three $100 orders in succession
- **THEN** the balance decreases: $5,000 → $4,900 → $4,800 → $4,700

### Requirement: Validate investment amount before placement
The system SHALL reject orders that have an investment amount below $10, above $5,000, or exceeding the current account balance.

#### Scenario: Reject order below minimum
- **WHEN** user enters $5 and clicks UP
- **THEN** an error message "Minimum investment is $10" appears
- **AND** the balance remains unchanged
- **AND** the order is not placed

#### Scenario: Reject insufficient balance
- **WHEN** balance is $500 and user enters $600 and clicks DOWN
- **THEN** an error message "Insufficient balance" appears
- **AND** the order is not created

#### Scenario: Accept valid amount
- **WHEN** balance is $5,000, user enters $100, and clicks UP
- **THEN** the order is created and balance updates to $4,900

### Requirement: Store order details at placement
The system SHALL record the order with: ID, asset, direction, entry price, investment amount, expiry time, placement timestamp, and status = PENDING.

#### Scenario: Order data captured
- **WHEN** user places an order for EUR/USD, $100, 5 minutes, UP direction at price 1.0843
- **THEN** the system creates an order with:
  - ID = auto-incremented (e.g., #001)
  - Asset = EUR/USD
  - Direction = UP
  - Entry Price = 1.0843
  - Amount = $100
  - Expiry = 300 seconds (5 min)
  - Status = PENDING
  - Timestamp = current time

### Requirement: Set order auto-resolution timer
The system SHALL automatically schedule order resolution for the expiry time specified at placement (30s, 1m, 2m, 5m, 10m, or 15m).

#### Scenario: 30-second expiry
- **WHEN** user places an order with 30-second expiry
- **THEN** the system schedules resolution to occur in 30 seconds

#### Scenario: 15-minute expiry
- **WHEN** user places an order with 15-minute expiry
- **THEN** the system schedules resolution to occur in 900 seconds

### Requirement: Prevent race conditions on balance
The system SHALL process all balance updates atomically, ensuring no order can reduce balance below zero even if multiple orders are placed rapidly.

#### Scenario: Prevent overdraft
- **WHEN** balance is $100 and user rapidly clicks UP twice with $75 each
- **THEN** the first order is placed (balance → $25)
- **AND** the second order is rejected because balance remaining ($25) < investment ($75)

### Requirement: Provide order placement feedback
The system SHALL display a confirmation or visual indicator that the order was successfully placed (e.g., new row appears in order table, balance updates visibly).

#### Scenario: Order appears in table
- **WHEN** user places an order
- **THEN** a new row immediately appears at the top of the order history table
- **AND** the order shows PENDING status with a countdown timer

#### Scenario: Balance updated visibly
- **WHEN** user places an order for $100
- **THEN** the balance in the header decreases by $100 and the change is visually apparent

### Requirement: Error handling and user feedback
The system SHALL display clear error messages for: insufficient balance, amount below minimum, amount above maximum, and invalid inputs.

#### Scenario: Clear error message
- **WHEN** user tries to place an order with insufficient balance
- **THEN** an alert or error message displays "Insufficient balance"
- **AND** the user can dismiss the error and correct the input
