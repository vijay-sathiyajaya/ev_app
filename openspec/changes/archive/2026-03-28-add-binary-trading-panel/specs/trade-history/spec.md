## ADDED Requirements

### Requirement: Display order history table
The system SHALL display all placed orders in a table with columns: Order ID, Asset, Direction, Entry Price, Close Price, Amount, Expiry, Status, and P&L.

#### Scenario: Table displays order data
- **WHEN** a user places an order
- **THEN** the order appears immediately in the order history table
- **AND** the table shows all nine columns with correct data for that order

#### Scenario: New orders appear at top
- **WHEN** user places orders #001, then #002, then #003
- **THEN** the table displays them in reverse chronological order: #003, #002, #001 (newest first)

### Requirement: Order ID generation and display
The system SHALL auto-generate a unique, incrementing order ID for each order (e.g., #001, #002, #003) and display it with leading zeros.

#### Scenario: Order IDs auto-increment
- **WHEN** the first order is placed
- **THEN** it receives ID #001
- **WHEN** the second order is placed
- **THEN** it receives ID #002
- **AND** IDs are formatted with three digits (001, 002, etc.)

### Requirement: Display order direction with visual badges
The system SHALL display order direction (UP or DOWN) as a colored badge: UP in green with up arrow (▲ UP), DOWN in red with down arrow (▼ DOWN).

#### Scenario: UP badge styling
- **WHEN** order direction is UP
- **THEN** the badge displays "▲ UP" in green with light green background

#### Scenario: DOWN badge styling
- **WHEN** order direction is DOWN
- **THEN** the badge displays "▼ DOWN" in red with light red background

### Requirement: Display prices with appropriate formatting
The system SHALL format entry and close prices to match the asset's decimal place convention (3–5 decimals depending on pair type).

#### Scenario: EUR/USD price formatting
- **WHEN** order for EUR/USD has entry price 1.08432
- **THEN** the table displays "1.0843" (4 decimals)

#### Scenario: USD/JPY price formatting
- **WHEN** order for USD/JPY has entry price 149.842
- **THEN** the table displays "149.84" (2 decimals)

### Requirement: Display close price as "—" for pending orders
The system SHALL show a dash or placeholder ("—") for the close price of pending orders until resolution.

#### Scenario: Pending order close price
- **WHEN** an order is PENDING
- **THEN** the Close Price column displays "—"
- **WHEN** the order resolves
- **THEN** the Close Price is populated with the actual resolved price

### Requirement: Display live countdown timer for pending orders
The system SHALL show the remaining seconds on each pending order, updating every second as the expiry approaches.

#### Scenario: Countdown display
- **WHEN** an order is placed with 60-second expiry
- **THEN** the Status column displays "PENDING 60s"
- **WHEN** 10 seconds have passed
- **THEN** the Status updates to "PENDING 50s"
- **AND** it continues counting down every second

#### Scenario: Multi-minute expiry display
- **WHEN** an order has 300 seconds (5 minutes) expiry
- **THEN** the Status displays "PENDING 300s" initially
- **WHEN** 60 seconds pass
- **THEN** the Status shows "PENDING 240s"

### Requirement: Auto-resolve orders at expiry
The system SHALL automatically resolve each order when its expiry time elapses, comparing entry and close prices to determine WIN or LOSS.

#### Scenario: Order resolves to WIN
- **WHEN** an UP order is placed at price 1.0843 with 30-second expiry
- **AND** the price at expiry is 1.0865 (higher)
- **THEN** the order status changes to WON
- **AND** the Close Price is populated with 1.0865

#### Scenario: Order resolves to LOSS
- **WHEN** a DOWN order is placed at price 1.0843 with 30-second expiry
- **AND** the price at expiry is 1.0865 (higher, opposite of DOWN prediction)
- **THEN** the order status changes to LOST
- **AND** the Close Price is populated with 1.0865

#### Scenario: UP wins when price rises
- **WHEN** UP order entry price 100.00, close price 100.50
- **THEN** status = WON

#### Scenario: UP loses when price falls
- **WHEN** UP order entry price 100.00, close price 99.50
- **THEN** status = LOST

#### Scenario: DOWN wins when price falls
- **WHEN** DOWN order entry price 100.00, close price 99.50
- **THEN** status = WON

#### Scenario: DOWN loses when price rises
- **WHEN** DOWN order entry price 100.00, close price 100.50
- **THEN** status = LOST

### Requirement: Display order status with visual indicators
The system SHALL show status badges with color coding and pulsing dot indicators: PENDING in gold (pulsing), WON in green (steady), LOST in red (steady).

#### Scenario: PENDING status badge
- **WHEN** order status is PENDING
- **THEN** the badge displays "PENDING" with gold color and a pulsing dot
- **AND** the pulsing animation continues until resolution

#### Scenario: WON status badge
- **WHEN** order status is WON
- **THEN** the badge displays "WON" with green color and a steady dot

#### Scenario: LOST status badge
- **WHEN** order status is LOST
- **THEN** the badge displays "LOST" with red color and a steady dot

### Requirement: Calculate and display P&L
The system SHALL calculate P&L per order: +amount × 0.85 for wins, −amount for losses. Display as colored text: green for positive, red for negative.

#### Scenario: Win P&L calculation and display
- **WHEN** order amount is $100 and result is WON
- **THEN** P&L = +$85.00 (amount × 0.85)
- **AND** the P&L column displays "+$85.00" in green

#### Scenario: Loss P&L calculation and display
- **WHEN** order amount is $100 and result is LOST
- **THEN** P&L = −$100.00
- **AND** the P&L column displays "−$100.00" in red

#### Scenario: P&L formatting
- **WHEN** displaying P&L
- **THEN** values show with two decimal places (e.g., +$85.00, −$200.00)

### Requirement: Credit balance on winning orders
The system SHALL add the win amount (original amount + 85% profit) to the user's balance immediately upon order resolution.

#### Scenario: Balance credit on win
- **WHEN** an order with $100 investment WON
- **THEN** the system credits $100 + ($100 × 0.85) = $185 to the balance
- **AND** balance increases by $185

#### Scenario: Balance unchanged on loss
- **WHEN** an order with $100 investment LOST
- **THEN** the balance is NOT increased (amount was already deducted at placement)

### Requirement: Aggregate statistics
The system SHALL display a stats bar showing: Total Trades, Won, Lost, Win Rate (%), and Net P&L, updated dynamically as orders resolve.

#### Scenario: Stats update on resolution
- **WHEN** user has placed 10 orders and 6 have resolved (4 WON, 2 LOST)
- **THEN** the stats display:
  - Total Trades: 10
  - Won: 4
  - Lost: 2
  - Win Rate: 67% (4/6 = 0.667)
  - Net P&L: +$140 (4 × 85 − 2 × 100 = 340 − 200)

#### Scenario: Win rate calculation
- **WHEN** 0 orders have resolved
- **THEN** Win Rate displays 0% (no data)
- **WHEN** 1 order WON and 1 order LOST
- **THEN** Win Rate displays 50%

#### Scenario: Net P&L color coding
- **WHEN** Net P&L is positive
- **THEN** it displays in green color
- **WHEN** Net P&L is negative
- **THEN** it displays in red color

### Requirement: Clear completed orders
The system SHALL provide a "Clear All" button that removes all non-pending (WON/LOST) orders from the table, with a confirmation dialog.

#### Scenario: Clear button functionality
- **WHEN** user clicks the "Clear All" button
- **THEN** a confirmation dialog appears asking "Clear all completed orders?"

#### Scenario: Confirm clear
- **WHEN** user confirms the clear action
- **THEN** all WON and LOST orders are removed from the table
- **AND** only PENDING orders remain

#### Scenario: Cancel clear
- **WHEN** user clicks Cancel on the confirmation dialog
- **THEN** no orders are removed

### Requirement: Empty state message
The system SHALL display a helpful empty state message when the order table is empty, instructing the user to select an asset and place a trade.

#### Scenario: Empty table display
- **WHEN** no orders have been placed
- **THEN** the order table displays "No orders yet. Select an asset and place a trade." with an icon
