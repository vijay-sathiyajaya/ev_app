## ADDED Requirements

### Requirement: Simulate live price movement
The system SHALL update all asset prices on a ~900ms interval with realistic random drift, simulating live market movement.

#### Scenario: Price tick updates
- **WHEN** the panel is active
- **THEN** approximately every 900ms, each asset price is updated by a small random amount (drift ±0.04% per tick)

#### Scenario: Price drift calculation
- **WHEN** EUR/USD price is 1.0843 and a tick occurs
- **THEN** the new price is 1.0843 ± (1.0843 * random(±0.0004)) ≈ range of 1.0831 to 1.0855
- **AND** the change is realistic and not explosive

### Requirement: Update selected asset price in trade header
The system SHALL continuously update the selected asset's price in the trade header with each tick, reflecting live market movement.

#### Scenario: Live price display for selected asset
- **WHEN** EUR/USD is selected and a price tick occurs
- **THEN** the price displayed in the trade header updates immediately
- **AND** the new price reflects the tick's drift calculation

#### Scenario: Price updates every 900ms
- **WHEN** user observes the trade header for 5 seconds
- **THEN** the price updates approximately 5-6 times (one update per ~900ms)

### Requirement: Format prices appropriately per asset
The system SHALL adapt price formatting (decimal places) based on the asset type, showing 3–5 decimal places depending on the pair's typical range.

#### Scenario: Major pair formatting (4 decimals)
- **WHEN** EUR/USD price is 1.08432
- **THEN** the display shows "1.0843" (4 decimals)

#### Scenario: JPY pair formatting (2 decimals)
- **WHEN** USD/JPY price is 149.842
- **THEN** the display shows "149.84" (2 decimals)

#### Scenario: Exotic pair formatting (5 decimals)
- **WHEN** EUR/AUD price is 1.66430
- **THEN** the display shows "1.66430" (5 decimals)

### Requirement: Maintain price state across all assets
The system SHALL keep track of current prices for all 18 assets simultaneously, enabling accurate order resolution even if the user switches assets during a trade's execution period.

#### Scenario: Price state consistency
- **WHEN** user places a trade on EUR/USD
- **AND** immediately switches to GBP/USD and places another trade
- **THEN** both orders retain their entry prices from the moment of placement
- **AND** resolution resolves each order against the correct asset's current price

#### Scenario: Asset price independence
- **WHEN** EUR/USD price increases to 1.0900
- **THEN** other asset prices (GBP/USD, USD/JPY, etc.) are unaffected by this change

### Requirement: Realistic price bounds
The system SHALL prevent prices from dropping below zero and maintain reasonable price ranges based on historical data for each asset.

#### Scenario: Price floor
- **WHEN** a price tick calculation would produce a negative price
- **THEN** the system prevents it and keeps price >= 0.0001

#### Scenario: Stable price range
- **WHEN** observing price movement over 30+ ticks
- **THEN** the price remains within ±2% of its initial value (realistic drift)

### Requirement: Price updates visible in asset list
The system SHALL update each asset's displayed price and percentage change in the asset list with each tick, keeping the list current without requiring a manual refresh.

#### Scenario: Asset list prices update
- **WHEN** viewing the asset list while price ticks occur
- **THEN** each asset's price updates every ~900ms
- **AND** the percentage change badge color updates (green for positive, red for negative)
