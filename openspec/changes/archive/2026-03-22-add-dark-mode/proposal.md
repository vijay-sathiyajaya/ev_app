## Why

The application currently has a light-mode-only interface with high contrast that can cause eye strain during extended use or in low-light environments. Implementing dark mode will improve user experience, accessibility, and provide a more modern, professional appearance. This change addresses user comfort and aligns with modern web application standards.

## What Changes

- Add a theme toggle control to the application toolbar
- Implement dark color palette for all UI elements (backgrounds, text, accents)
- Persist theme preference to browser localStorage
- Automatically detect and apply system dark mode preference on first visit
- Update all inline styles in App.vue to support both light and dark themes
- Ensure card backgrounds, status indicators, and accent colors work well in both themes

## Capabilities

### New Capabilities

- `theme-system`: User ability to switch between light and dark themes with automatic persistence and system preference detection

### Modified Capabilities

- `ui-styling`: Update existing UI component styling to support dark mode variant while maintaining the current light mode defaults and design system consistency

## Impact

- **Frontend Components**: App.vue styling and theme toggle control
- **Storage**: Browser localStorage for theme preference persistence
- **CSS/Styling**: All inline styles require dark mode color variants
- **User Experience**: Theme preference persists across sessions and syncs with system preferences
