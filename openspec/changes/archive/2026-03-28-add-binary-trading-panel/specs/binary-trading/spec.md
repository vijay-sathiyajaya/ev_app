## ADDED Requirements

### Requirement: Trade header displays selected asset
The system SHALL display the selected asset name, full description, and live price in a prominent trade header above the trading controls.

#### Scenario: Trade header updates on asset selection
- **WHEN** user selects EUR/USD
- **THEN** the trade header shows "EUR/USD" as the selected asset name
- **AND** displays the current live price (e.g., 1.0843)
- **AND** the price updates every ~900ms with market tick movement
- **WHEN** user selects GBP/USD
- **THEN** the trade header updates to show "GBP/USD" and its current price

### Requirement: Input investment amount
The system SHALL allow users to enter a trade investment amount with validation constraints: minimum $10, maximum $5,000, and amount SHALL NOT exceed current account balance.

#### Scenario: Valid investment amount
- **WHEN** user enters $100 in the investment amount field
- **THEN** the amount is accepted and the trade buttons remain enabled

#### Scenario: Minimum investment validation
- **WHEN** user tries to enter $5
- **THEN** the system displays an error message "Minimum investment is $10"
- **AND** the trade buttons remain disabled

#### Scenario: Maximum investment validation
- **WHEN** user tries to enter $6,000
- **THEN** the system accepts the input but limits it to $5,000 or displays a warning

#### Scenario: Insufficient balance
- **WHEN** current balance is $500 and user enters $600
- **THEN** the system displays "Insufficient balance"
- **AND** trade buttons are disabled

### Requirement: Select trade direction
The system SHALL provide two trade direction buttons: UP (Call) and DOWN (Put). User clicks one to specify trade prediction.

#### Scenario: Click UP button
- **WHEN** user sets investment to $100 and clicks the UP (▲ CALL) button
- **THEN** the order is placed with direction=UP

#### Scenario: Click DOWN button
- **WHEN** user sets investment to $100 and clicks the DOWN (▼ PUT) button
- **THEN** the order is placed with direction=DOWN

### Requirement: Select expiry time
The system SHALL provide a dropdown to select order expiry time from: 30 seconds, 1 minute, 2 minutes, 5 minutes, 10 minutes, 15 minutes.

#### Scenario: Select expiry time
- **WHEN** user clicks the expiry time dropdown
- **THEN** six options appear: 30s, 1m, 2m, 5m, 10m, 15m
- **WHEN** user selects "5m"
- **THEN** the selected value shows "5m" in the dropdown

#### Scenario: Default expiry
- **WHEN** the panel loads
- **THEN** a default expiry time is pre-selected (e.g., 5m)

### Requirement: Display payout return rate
The system SHALL display the fixed payout return rate (85%) prominently, showing the potential profit on a winning trade.

#### Scenario: Payout display
- **WHEN** user enters $100 investment
- **THEN** the payout badge displays "85%" to indicate profit ratio
- **WHEN** user enters $200 investment
- **THEN** the payout still shows "85%" (same rate for all trades)

### Requirement: Disable controls during trade processing
The system SHALL disable the investment input and trade buttons immediately after order placement and re-enable them once the new form is ready for the next trade.

#### Scenario: Controls disabled after placement
- **WHEN** user places a trade
- **THEN** the investment field, expiry dropdown, and UP/DOWN buttons are disabled briefly
- **AND** they re-enable within 500ms for the next trade

### Requirement: Visual feedback on button interactions
The system SHALL provide hover effects (brightness increase, slight upward translation) and active states (no translation) on trade buttons to indicate interactivity.

#### Scenario: UP button hover effect
- **WHEN** user hovers over the UP button
- **THEN** the button brightens slightly and translates upward 1px
- **WHEN** user releases the hover
- **THEN** the button returns to normal state

#### Scenario: Button active state
- **WHEN** user clicks the UP button
- **THEN** the button's translation returns to 0px (no upward offset)

### Requirement: Trade controls layout
The system SHALL arrange the investment input, expiry dropdown, and payout display in a clear row layout above the UP/DOWN buttons.

#### Scenario: Controls arrangement on desktop
- **WHEN** viewport width is 1200px
- **THEN** investment input, expiry dropdown, and payout occupy one row
- **AND** UP/DOWN buttons occupy the row below as a 50/50 split
