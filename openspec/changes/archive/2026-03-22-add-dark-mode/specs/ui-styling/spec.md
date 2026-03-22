## ADDED Requirements

### Requirement: Light Mode Styling
The application SHALL maintain the current light mode styling as the default visual theme with a defined color palette accessible to other components.

#### Scenario: Light mode uses established color palette
- **WHEN** light theme is active
- **THEN** the application uses the established light palette: purple gradient (#667eea to #764ba2) for primary, green (#4caf50) for success, red (#f44336) for danger, and light backgrounds for cards

#### Scenario: Light mode provides text contrast
- **WHEN** light theme is active
- **THEN** text on light backgrounds is dark (#333 or darker) for sufficient WCAG AA contrast, and text on cards/overlays is white or light gray

### Requirement: Dark Mode Styling
The application SHALL support dark mode styling with a complementary color palette where all light mode colors are inverted or adjusted for dark backgrounds.

#### Scenario: Dark mode backgrounds are dark
- **WHEN** dark theme is active
- **THEN** primary backgrounds use dark colors (#121212 or similar), secondary backgrounds use slightly lighter grays (#1e1e1e), maintaining visual hierarchy

#### Scenario: Dark mode text is light
- **WHEN** dark theme is active
- **THEN** primary text is light gray or off-white (#e0e0e0 or #f5f5f5) and secondary text is lighter gray (#bbb) for visual hierarchy

#### Scenario: Dark mode maintains accent color distinction
- **WHEN** dark theme is active
- **THEN** accent colors remain visually distinct: purple remains saturated/bright, green success state is visible, red error state is clearly distinguishable from background

#### Scenario: Dark mode card styling matches theme
- **WHEN** dark theme is active
- **THEN** card and modal backgrounds use dark theme colors that provide sufficient contrast against the darker main background while maintaining glassmorphism effects

### Requirement: Toolbar Styling Consistency
The application's toolbar controls (buttons, status indicators, labels) SHALL adapt to the active theme.

#### Scenario: Toolbar buttons are visible in light mode
- **WHEN** light theme is active
- **THEN** toolbar buttons (Connect, Demo/Real toggle, theme control) use light mode colors with clear hover/active states

#### Scenario: Toolbar buttons are visible in dark mode
- **WHEN** dark theme is active
- **THEN** toolbar buttons use dark mode colors and contrast appropriately against the dark toolbar background

#### Scenario: Status indicator colors adapt to theme
- **WHEN** theme is switched
- **THEN** the connection status indicator (green for connected, red for disconnected with animated pulse) displays in theme-appropriate colors

### Requirement: Balance Card Styling
The balance card display SHALL adapt its gradient, text colors, and shadow effects to the active theme.

#### Scenario: Balance card gradient in light mode
- **WHEN** light theme is active
- **THEN** balance card displays the purple gradient (#667eea to #764ba2) with white text and appropriate box shadow for light backgrounds

#### Scenario: Balance card styling in dark mode
- **WHEN** dark theme is active
- **THEN** balance card maintains visibility with adjusted colors (gradient intensity or brightness adjusted) and light text with dark theme-appropriate shadow

### Requirement: Error and Status Message Styling
Error banners and status information displays SHALL use theme-appropriate colors for visibility.

#### Scenario: Error messages visible in light mode
- **WHEN** light theme is active and connection error occurs
- **THEN** error banner uses red background (#f44336 or similar) with white text

#### Scenario: Error messages visible in dark mode
- **WHEN** dark theme is active and connection error occurs
- **THEN** error banner uses dark mode red/pink variant with adequate contrast against dark background

#### Scenario: Info messages maintain emphasis in both themes
- **WHEN** status or info messages are displayed
- **THEN** messages are clearly visible and distinguished from error messages in both light and dark themes
