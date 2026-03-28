## ADDED Requirements

### Requirement: Display asset list with category grouping
The system SHALL display Forex currency pairs in a collapsible/scrollable list organized by category: Major, Minor, and Exotic. Each category contains a set of related pairs.

#### Scenario: User views Major pairs
- **WHEN** the Binary Trading Panel loads
- **THEN** the asset list displays three categories (Major, Minor, Exotic) with all pairs grouped accordingly

#### Scenario: User scrolls through asset list
- **WHEN** user scrolls in the asset panel
- **THEN** the panel scrolls independently without affecting the trade area or orders table

### Requirement: Select an asset from the list
The system SHALL allow the user to click any asset to load it into the active trading area, updating the trade header with the selected asset's symbol and current price.

#### Scenario: User clicks an asset
- **WHEN** user clicks on "EUR/USD" in the asset list
- **THEN** the trade header displays "EUR/USD" and its live price
- **AND** the asset is visually highlighted with a left border and background color in the asset list

#### Scenario: User switches assets
- **WHEN** user has EUR/USD selected and clicks GBP/USD
- **THEN** the active highlight moves from EUR/USD to GBP/USD
- **AND** the trade header updates to show GBP/USD and its price

### Requirement: Visual indication of active selection
The system SHALL highlight the currently selected asset with a distinct visual style (left border accent, background color change) that persists until a different asset is clicked.

#### Scenario: Active asset styling
- **WHEN** EUR/USD is the active selection
- **THEN** it displays a cyan left border (3px) and darker background
- **AND** all other assets display only on hover interactions

#### Scenario: Asset styling on hover
- **WHEN** user hovers over an unselected asset (e.g., GBP/USD)
- **THEN** the asset row highlights with a subtle background color and left border (muted gray)

### Requirement: Asset default selection
The system SHALL load the first asset (EUR/USD - Major pair) as the default selected asset when the panel initializes.

#### Scenario: Panel initialization
- **WHEN** the Binary Trading Panel first loads
- **THEN** EUR/USD is automatically selected and highlighted
- **AND** the trade header displays EUR/USD with its current price
