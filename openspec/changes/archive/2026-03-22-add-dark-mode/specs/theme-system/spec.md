## ADDED Requirements

### Requirement: Theme Toggle Control
The application SHALL provide a user interface control that allows users to switch between light and dark themes.

#### Scenario: User toggles from light to dark
- **WHEN** user clicks the theme toggle button while in light mode
- **THEN** the application immediately switches to dark theme and saves preference to browser storage

#### Scenario: User toggles from dark to light
- **WHEN** user clicks the theme toggle button while in dark mode
- **THEN** the application immediately switches to light theme and saves preference to browser storage

#### Scenario: Toggle button displays correct state
- **WHEN** application loads
- **THEN** the theme toggle button visually indicates the currently active theme (e.g., moon icon for dark mode, sun icon for light mode)

### Requirement: Theme Persistence
The application SHALL persist the user's theme preference across sessions and browser restarts.

#### Scenario: Preference persists after browser restart
- **WHEN** user selects dark theme and closes the browser
- **THEN** when user reopens the application in the same browser, dark theme is automatically applied

#### Scenario: Preference persists across multiple tabs
- **WHEN** user has multiple tabs of the application open and toggles theme in one tab
- **THEN** the preference is saved and available if user opens a new tab (though existing tabs may not sync automatically)

### Requirement: System Preference Detection
The application SHALL automatically detect and apply the user's system (OS-level) dark mode preference on the first visit.

#### Scenario: First visit matches system dark mode
- **WHEN** user visits the application for the first time with system dark mode enabled
- **THEN** the application applies dark theme automatically without user action

#### Scenario: First visit matches system light mode
- **WHEN** user visits the application for the first time with system light mode enabled (or no preference)
- **THEN** the application applies light theme as default

#### Scenario: User changes system preference after explicit theme choice
- **WHEN** user has already selected a theme manually and then changes OS-level dark mode setting
- **THEN** the user's explicit choice takes precedence over system preference (system setting is not auto-applied)

### Requirement: Dark Mode Color Palette
The application SHALL provide a complete dark mode color palette for all UI elements with adequate contrast and legibility.

#### Scenario: Backgrounds are dark in dark mode
- **WHEN** dark theme is active
- **THEN** main backgrounds use dark colors (near-black or dark gray) and text uses light gray or white for readability

#### Scenario: Accent colors remain visible in dark mode
- **WHEN** dark theme is active
- **THEN** accent colors (purple gradient, green success state, red error state) remain visible and distinguishable from background

#### Scenario: Cards and containers contrast with background
- **WHEN** dark theme is active
- **THEN** card elements and containers have sufficient contrast against the dark background while maintaining visual hierarchy
