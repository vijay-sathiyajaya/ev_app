# Trading Platform Component Specifications

## Overview
Component specifications for the Trading Platform UI using Vue 3 with Composition API.

---

## Toolbar Component

### Specification
- **File**: `src/App.vue` (Integrated within main app)
- **Type**: Navigation & Quick Actions Bar
- **Scope**: Global application toolbar

### Features
- **Connection Status Indicator**
  - Visual indicator showing "Connected" or "Not Connected"
  - Pulsing animation when connected (2s interval)
  - Color: Green (#4caf50) when connected, Red (#f44336) when disconnected

- **Connect/Disconnect Buttons**
  - Button: Connect (⚡) - Initiates broker connection
  - Button: Disconnect (⊗) - Terminates broker connection
  - States: Enabled/Disabled based on connection status
  - Loading state: Shows spinner (⟳) during operation

- **Account Type Toggle**
  - Demo (D) Button - Switch to demo account
  - Real (R) Button - Switch to real account
  - Active indicator: Background highlight on selected type
  - Disabled during loading operations

- **Balance Display**
  - Format: `$X,XXX.XX`
  - Shows current account balance
  - Updates when account type changes
  - Account type label (DEMO/REAL)

### Props
```typescript
interface ToolbarProps {
  isConnected: boolean
  broker: string | null
  currentAccountType: 'demo' | 'real'
  balance: number
  loading: boolean
}
```

### Events/Methods
- `connectToBroker()` - Connect to broker
- `disconnectFromBroker()` - Disconnect from broker
- `switchAccountType(type)` - Switch account type

---

## Balance Card Component

### Specification
- **File**: `src/App.vue` (balance-section)
- **Type**: Display Card
- **Visibility**: Only shown when connected

### Structure
```
Available Balance
$X,XXX.XX
USD
Account: DEMO/REAL
```

### Styling
- Background: Gradient (Purple #667eea to Purple #764ba2)
- Text Color: White
- Border Radius: 12px
- Padding: 40px

### Props
```typescript
interface BalanceCardProps {
  balance: number
  accountType: 'demo' | 'real'
  currency: string
}
```

---

## Status Information Component

### Specification
- **File**: `src/App.vue` (status-section)
- **Type**: Information Display
- **Always Visible**: True

### Information Rows
1. **Connection Status**: Connected/Disconnected
   - Color: Green if connected, Red if disconnected
2. **Current Broker**: Broker name or "None"
3. **Account Type**: DEMO or REAL
4. **Last Updated**: HH:MM:SS format

### Styling
- Background: Light gray (#f5f5f5)
- Border Radius: 8px
- Two-column layout with label and value

---

## Error Banner Component

### Specification
- **Type**: Alert/Notification
- **Visibility**: Conditional (show when error exists)
- **Position**: Below toolbar, above main content

### States
- **Connection Error**: Red background (#f44336)
- **Account Error**: Red background (#f44336)
- **Message**: Clear error description

### Behavior
- Auto-dismiss: No (user must take action to fix)
- Multiple errors: Can show multiple banners

---

## Loading States

### Global Loading State
```typescript
loading: boolean
```

### Disabled States
- Connect button: Disabled when `isConnected || loading`
- Disconnect button: Disabled when `!isConnected || loading`
- Account toggle: Disabled when `loading`

### Visual Feedback
- Loading buttons: Show spinner icon (⟳)
- Opacity: 0.6 when disabled

---

## Responsive Breakpoints

### Desktop (1024px+)
- Toolbar: Horizontal, all controls visible
- Balance card: 600px max-width, centered

### Tablet (768px - 1023px)
- Toolbar: Wraps to 2-3 rows
- Controls rearrange for better fit
- Balance card: Responsive padding

### Mobile (480px - 767px)
- Toolbar: Vertical stack
- Font sizes: Reduced
- Button widths: Full width where possible

### Small Mobile (< 480px)
- Toolbar: Minimal spacing
- Font sizes: Very small
- Balance display: Compact

---

## Accessibility Requirements

- **ARIA Labels**: All buttons have title attributes
- **Color Contrast**: All text meets WCAG AA standards
- **Keyboard Navigation**: All buttons accessible via Tab
- **Focus States**: Visible focus indicators on buttons
- **Error Messages**: Clear, readable text

---

## API Integration

### Data Flow
1. **On Mount**: `fetchStatus()` called
2. **Status Update**: Fetches from `/api/trading/status`
3. **Balance Update**: Fetches from `/api/trading/account?type={type}`
4. **Connection Action**: Posts to `/api/trading/connect` or `/api/trading/disconnect`
5. **Account Switch**: Posts to `/api/trading/account/switch`

### Error Handling
- Try/catch blocks on all API calls
- Error messages displayed in banners
- Console logging for debugging
