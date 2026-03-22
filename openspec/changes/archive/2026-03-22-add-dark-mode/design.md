## Context

The application currently uses Vue 3 with Vite and has all styling defined inline in App.vue using scoped styles. The design uses a light-mode-only color palette (purple gradient, green for success, red for danger) with white cards on light backgrounds. No theme system currently exists. Users cannot adjust the interface for low-light environments or accessibility preferences.

## Goals / Non-Goals

**Goals:**
- Enable users to toggle between light and dark theme with a single control
- Detect and apply system dark mode preference automatically on first visit
- Persist theme preference across sessions using browser storage
- Ensure all UI elements are legible and aesthetically consistent in both themes
- Maintain current light mode as the default for existing users

**Non-Goals:**
- Creating a theme customization system or theme marketplace
- Supporting more than two themes (light/dark)
- Migrating App.vue to external stylesheet files
- Creating a reusable theme plugin for other projects

## Decisions

1. **Theme State Management**
   - **Decision**: Use Vue ref with localStorage persistence + browser `prefers-color-scheme` media query detection
   - **Rationale**: Simple, no external dependencies, works without Vuex/Pinia given project's current state management approach
   - **Alternative considered**: Pinia store (overkill given single component), localStorage alone (misses system preference sync)

2. **CSS Variable Architecture**
   - **Decision**: Define CSS color variables (--color-bg-primary, --color-text-primary, etc.) that toggle between light and dark values based on theme state
   - **Rationale**: Minimal changes to existing inline styles, variables apply automatically without duplicating style blocks
   - **Alternative considered**: Duplicate all style properties in separate dark mode blocks (verbose, maintenance risk), Tailwind classes (requires build config change)

3. **Theme Detection Logic**
   - **Decision**: On first visit, check localStorage → if not set, check `window.matchMedia('(prefers-color-scheme: dark)').matches` → default to light
   - **Rationale**: Respects user choice first, then system preference, with safe fallback
   - **Alternative considered**: Always default to light (ignores system preference), always force dark based on system (overrides user choice)

4. **Dark Mode Color Palette**
   - **Decision**: Create complementary dark palette: dark grays/blacks for backgrounds (#121212, #1e1e1e), light grays for text (#e0e0e0, #f5f5f5), maintain accent colors (purple, green, red) but adjust saturation/brightness
   - **Rationale**: WCAG AA contrast compliance, maintains visual hierarchy and brand colors
   - **Alternative considered**: Invert all colors (poor readability), single gray palette (loses design identity)

5. **Theme Toggle Control**
   - **Decision**: Add moon/sun icon toggle button in the toolbar next to existing controls
   - **Rationale**: Non-intrusive, visible, familiar UI pattern for theme switching
   - **Alternative considered**: Settings menu (extra navigation), right-click context menu (not discoverable)

## Risks / Trade-offs

- **Browser Storage Limit**: localStorage has ~5-10MB limit per domain; theme preference uses ~50 bytes so negligible risk. Mitigation: None needed, but avoid storing large objects when expanding this subsystem.
- **CSS Variable Support**: CSS custom properties require modern browser support; all targets (Chrome, Firefox, Safari, Edge) support this. Mitigation: Test in target browsers, fallback values are not needed for our use case.
- **System Preference Sync**: Once user manually toggles theme, system preference changes won't auto-apply. Mitigation: Document that manual theme choice takes priority; consider adding "Use system preference" reset button in future.
- **Accessibility**: Some users with color sensitivity may need adjustment. Mitigation: Ensure transitions are disabled for users with `prefers-reduced-motion`, test with WCAG color contrast tools.

## Migration Plan

1. Add theme state composable to App.vue (localStorage + system preference detection)
2. Define CSS color variables in component scope with light/dark value pairs
3. Replace hardcoded color values in existing inline styles with CSS variable references
4. Add theme toggle button to toolbar with conditional styling
5. Test theme switching, localStorage persistence, initial system preference detection in major browsers
6. Deploy to production; existing users will see light mode initially, can toggle to dark

## Open Questions

- Should theme preference be synced across multiple tabs/windows open in the same browser? (Requires storage event listener)
- Are there specific dark mode colors preferred for brand consistency, or should we derive from light palette?
