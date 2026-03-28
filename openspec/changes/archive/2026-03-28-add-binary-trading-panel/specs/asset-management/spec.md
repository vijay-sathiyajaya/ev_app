## ADDED Requirements

### Requirement: Display asset metadata
The system SHALL display each asset with the following information: symbol (e.g., EUR/USD), full name (e.g., "Euro / US Dollar"), current price, and percentage change.

#### Scenario: Asset row displays all data
- **WHEN** the asset list loads
- **THEN** each asset row shows: symbol, full name, current price (formatted appropriately), and percentage change badge

#### Scenario: Price formatting per asset type
- **WHEN** asset "EUR/USD" (Major pair) is displayed
- **THEN** price shows 4 decimal places (e.g., 1.0843)
- **WHEN** asset "USD/JPY" is displayed
- **THEN** price shows 2 decimal places (e.g., 149.84)
- **WHEN** asset "EUR/AUD" is displayed
- **THEN** price shows 4 decimal places (e.g., 1.6643)

### Requirement: Display percentage change with color coding
The system SHALL show the 24-hour percentage change as a colored badge: green for positive (UP), red for negative (DOWN).

#### Scenario: Positive price movement
- **WHEN** an asset's percentage change is +0.45%
- **THEN** the badge displays "+0.45%" in green with a light green background

#### Scenario: Negative price movement
- **WHEN** an asset's percentage change is -0.23%
- **THEN** the badge displays "-0.23%" in red with a light red background

### Requirement: Search and filter assets
The system SHALL provide a text input that filters the asset list in real-time by symbol (e.g., "EUR") or full name (e.g., "Euro").

#### Scenario: Filter by symbol
- **WHEN** user types "EUR" in the search box
- **THEN** the asset list shows only pairs containing EUR: EUR/USD, EUR/GBP, EUR/JPY, EUR/AUD, EUR/NOK
- **AND** all other pairs are hidden

#### Scenario: Filter by name
- **WHEN** user types "Dollar" in the search box
- **THEN** the asset list shows: EUR/USD, GBP/USD, AUD/USD, USD/JPY, USD/CHF, USD/CAD, NZD/USD, USD/SGD, USD/HKD, USD/MXN, USD/ZAR

#### Scenario: Clear filter
- **WHEN** user clears the search box (deletes all text)
- **THEN** the complete asset list reappears

### Requirement: Asset list categories
The system SHALL organize the 18 supported Forex pairs into three categories for easier browsing: Major pairs (7), Minor pairs (6), and Exotic pairs (5).

#### Scenario: Category organization
- **WHEN** the panel loads
- **THEN** assets are grouped as: Major (EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD, NZD/USD), Minor (EUR/GBP, EUR/JPY, GBP/JPY, EUR/AUD, GBP/CHF, AUD/JPY), Exotic (USD/SGD, USD/HKD, USD/MXN, USD/ZAR, EUR/NOK)

#### Scenario: Filter hides empty categories
- **WHEN** user filters to show only "JPY" pairs
- **THEN** the Major category is hidden (no matches)
- **AND** Minor category shows 2 pairs (EUR/JPY, GBP/JPY, AUD/JPY)
- **AND** Exotic category is hidden

### Requirement: Responsive asset panel width
The system SHALL maintain a fixed 300px width for the asset panel on desktop (900px+). On narrower displays, the panel adapts to approximately 100% width with a max-height constraint.

#### Scenario: Desktop layout
- **WHEN** viewport width is 1200px
- **THEN** asset panel occupies 300px width
- **AND** trade area occupies remaining 900px width

#### Scenario: Mobile layout
- **WHEN** viewport width is 768px
- **THEN** asset panel displays above trade area
- **AND** trade area displays below in full width
