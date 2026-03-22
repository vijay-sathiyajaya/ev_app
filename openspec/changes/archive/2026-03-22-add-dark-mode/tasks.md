## 1. Theme State Management

- [x] 1.1 Create `useTheme()` composable in App.vue to manage theme state
- [x] 1.2 Implement localStorage read/write for theme preference persistence
- [x] 1.3 Implement system dark mode detection using `window.matchMedia('(prefers-color-scheme: dark)')`
- [x] 1.4 Initialize theme on component mount with preference priority: localStorage → system preference → light default
- [x] 1.5 Test theme state initialization with various scenarios (first visit, returning user, etc.)

## 2. CSS Variable Architecture

- [x] 2.1 Define light mode color variables in App.vue (--color-bg-primary, --color-bg-secondary, --color-text-primary, --color-text-secondary, --color-primary, --color-success, --color-danger, --color-shadow)
- [x] 2.2 Define dark mode color variable values with appropriate dark theme colors
- [x] 2.3 Apply computed style object that toggles CSS variables based on active theme
- [x] 2.4 Verify CSS variables are properly scoped to App.vue component

## 3. Update App.vue Styles for Theme Support

- [x] 3.1 Replace hardcoded color values in toolbar styles with CSS variables (backgrounds, text, borders)
- [x] 3.2 Replace hardcoded colors in status indicator styles with CSS variables (connected green, disconnected red)
- [x] 3.3 Replace hardcoded colors in balance card gradient with CSS variables while maintaining visual impact
- [x] 3.4 Update card/container background colors to use CSS variables
- [x] 3.5 Update all text color values to use CSS variables (primary, secondary, error text)
- [x] 3.6 Update box-shadow colors to use CSS variables for theme-appropriate depth
- [x] 3.7 Update error banner styling to use theme-appropriate colors

## 4. Implement Theme Toggle Control

- [x] 4.1 Add theme toggle button HTML to toolbar (position near existing controls)
- [x] 4.2 Add icon or label to toggle button (e.g., sun icon for light, moon icon for dark)
- [x] 4.3 Implement click handler to call toggleTheme() function
- [x] 4.4 Add visual indicator to show currently active theme (button state, color, or icon change)
- [x] 4.5 Style toggle button to be visible in both light and dark modes with appropriate hover states

## 5. Testing and Validation

- [x] 5.1 Test theme toggle switches theme immediately
- [x] 5.2 Test theme preference persists after page refresh
- [x] 5.3 Test theme preference persists after browser close/reopen
- [x] 5.4 Test system dark mode is applied on first visit (when no localStorage preference exists)
- [x] 5.5 Test manual theme choice overrides system preference
- [x] 5.6 Verify all UI elements are legible in light theme (text contrast, colors visible)
- [x] 5.7 Verify all UI elements are legible in dark theme (consistent with WCAG AA standards)
- [x] 5.8 Test balance card gradient and styling in both themes
- [x] 5.9 Test toolbar buttons and status indicators in both themes
- [x] 5.10 Test error messages and status info display correctly in both themes
- [x] 5.11 Test theme toggle appearance matches current active theme
- [x] 5.12 Test in Chrome, Firefox, Safari, and Edge browsers

## 6. Finalization

- [x] 6.1 Review all CSS variables to ensure comprehensive theme coverage (no hardcoded colors remain)
- [x] 6.2 Create or update documentation for the dark mode feature
- [x] 6.3 Test with users (if applicable) for accessibility feedback
- [x] 6.4 Prepare for deployment and verify no breaking changes to existing light mode
