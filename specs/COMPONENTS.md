# Trading Platform Component Specifications - iQOption Integration

## Overview
Component specifications for the Trading Platform UI using Vue 3 with Composition API and iQOption broker integration.

---

## LoginForm Component

### Specification
- **File**: `src/components/LoginForm.vue`
- **Type**: Authentication Form
- **Scope**: Initial app state when user is not authenticated

### Features
- **Email Input Field**
  - Type: email
  - Placeholder: "Enter your iQOption email"
  - Validation: Required, valid email format
  - Error message: "Please enter a valid email"

- **Password Input Field**
  - Type: password
  - Placeholder: "Enter your password"
  - Validation: Required, minimum 6 characters
  - Error message: "Password is required"

- **Submit Button**
  - Label: "Login" or "Sign In"
  - State: Enabled when form is valid
  - Loading state: Shows spinner and disabled label "Logging in..."
  - Disabled: While form is invalid or loading

- **Form Validation**
  - Real-time validation on input change
  - Visual error indicators (red text)
  - Green checkmark on valid fields
  - Submit button enables only when all fields valid

- **Error Display**
  - Error banner above form for API errors
  - Displays: "Invalid email or password" or network errors
  - Auto-dismisses after 5 seconds or on new input

### Props
```typescript
interface LoginFormProps {
  loading: boolean
}
```

### Events/Methods
- `submitLogin(email, password)` - Submit login credentials
- `validateEmail(email)` - Validate email format
- `validatePassword(password)` - Validate password requirements
- `clearForm()` - Clear input fields after successful login

### Styling
- Background: White or light background
- Form width: 400px max-width on desktop
- Padding: 40px
- Border radius: 8px
- Input spacing: 20px vertical gap
- Button: Full width, primary color (#667eea)
- Button hover: Darker shade (#5568d3)

### Data Flow
1. User enters email and password
2. Live validation provides feedback
3. User clicks Submit
4. Form emits `submitLogin` event with credentials
5. Parent component calls `/api/broker/login` API
6. On success: AccountDashboard displays
7. On error: Error banner shown, form preserved for retry

---

## AccountDashboard Component

### Specification
- **File**: `src/components/AccountDashboard.vue`
- **Type**: Account Information & Controls Dashboard
- **Scope**: Displays after successful login

### Sections

#### Header Section
- **Greeting**: "Welcome, [email]"
- **Status**: "Connected to iQOption"
- Connected indicator: Green pulsing dot

#### Balance Display Section
```
Available Balance
$X,XXX.XX USD

Trading Mode: DEMO / LIVE
```
- Balance format: $X,XXX.XX
- Currency: USD
- Mode indicator with different colors
  - Demo: Blue background
  - Live: Red background with warning icon ⚠️

#### Mode Selector Section
- **Mode Toggle**: Demo / Live buttons
- **Current Selection**: Highlighted with background color
- **Confirmation Dialog** (for switching to live):
  - Title: "Switch to Live Trading?"
  - Message: "You will be trading with real money. Are you sure?"
  - Buttons: Cancel, Confirm
- **Loading State**: Spinner during mode switch

#### Logout Section
- **Logout Button**: Red/danger color
- **Label**: "Logout"
- **Position**: Bottom of dashboard
- **Confirmation**: Optional confirmation before logout

### Props
```typescript
interface AccountDashboardProps {
  sessionId: string
  email: string
  balance: number
  currency: string
  mode: 'demo' | 'live'
  loading: boolean
}
```

### Events/Methods
- `switchMode(newMode)` - Switch between demo/live
- `logout()` - Logout user
- `refreshBalance()` - Manually refresh balance
- `confirmModeSwitch(newMode)` - Confirm live mode switch

### Data Fetching
- On mount: Get balance for current mode
- On mode switch: Fetch balance for new mode
- Polling: Update balance every 30 seconds (optional cache)

### Styling
- Background: Gradient or solid light color
- Card width: 600px max-width on desktop
- Padding: 40px
- Border radius: 12px
- Sections separated with 30px margins
- Demo badge: Blue (#2196f3)
- Live badge: Red (#f44336)

### Responsive Design
- **Desktop (1024px+)**: Full width layout
- **Tablet (768px)**: Reduced padding
- **Mobile (480px)**: Stack vertically, reduce font sizes

---

## App.vue Root Component

### Specification
- **Type**: Root Application Component
- **Scope**: Global state management and routing

### State Management
```typescript
interface AppState {
  isAuthenticated: boolean
  sessionId: string | null
  email: string
  balance: number
  mode: 'demo' | 'live'
  loading: boolean
  error: string | null
}
```

### Features
- **Route Decision**: Show LoginForm or AccountDashboard
- **Session Persistence**: Check localStorage on mount
- **Auto-login**: Validate session token on page load
- **Error Banner**: Global error display
- **Loading Overlay**: Global loading indicator (optional)

### Conditional Rendering
```javascript
if (isAuthenticated && sessionId) {
  show: AccountDashboard
} else {
  show: LoginForm
}
```

### Methods
- `handleLogin(email, password)` - Process login
- `handleLogout()` - Process logout
- `handleModeSwitch(mode)` - Process mode switch
- `validateSession()` - Validate stored session token
- `refreshBalance()` - Refresh balance data

### API Integration
- `POST /api/broker/login` - Login
- `POST /api/broker/logout` - Logout
- `GET /api/broker/balance` - Fetch balance
- `POST /api/broker/mode/switch` - Switch mode

### Error Handling
- 401 errors: Trigger logout and return to LoginForm
- Network errors: Display error banner
- API errors: Parse and display error message
- Session errors: Auto-logout if session invalid

### Local Storage
- **Key**: `sessionId` - Store session token
- **Persistence**: Survive page reload
- **Cleanup**: Remove on logout
- **Validation**: Validate on app load

---

## Error Banner Component

### Specification
- **Type**: Alert/Notification
- **Visibility**: Conditional (show when error exists)
- **Position**: Top of dashboard or centered

### States
- **Authentication Error**: Red background (#f44336)
- **API Error**: Orange background (#ff9800)
- **Success Message**: Green background (#4caf50)

### Behavior
- Auto-dismiss: Yes (5 seconds)
- Manual dismiss: X button to close immediately
- Multiple errors: Show one at a time, queue if needed
- Persistence: Clear on component unmount

### Styling
- Padding: 16px 24px
- Border radius: 4px
- Font size: 14px
- Icon: Left aligned (⚠️, ✓, ✗)

---

## Loading States

### Global Loading State
```typescript
loading: boolean
```

### Button States During Loading
- LoginForm Submit: Disabled, shows "Logging in..."
- Mode Switch: Disabled, shows "Switching..."
- Logout: Disabled, shows "Logging out..."

### Visual Feedback
- Spinner animation on buttons
- Overlay on interactive elements
- Opacity: 0.6 when disabled
- Cursor: not-allowed when disabled

---

## Accessibility Requirements

- **ARIA Labels**: All buttons have aria-label
- **Role Attributes**: form, button, alert roles used correctly
- **Error Messages**: Associated with form fields (aria-describedby)
- **Color Contrast**: WCAG AA compliant
- **Keyboard Navigation**: All controls accessible via Tab
- **Focus Management**: Focus moved to error on form submission fail
- **Loading States**: Announced via aria-busy attribute

---

## Security Considerations

- **Passwords**: Never logged to console
- **Session Tokens**: Stored in localStorage only (consider httpOnly limitations)
- **HTTPS**: All API calls use HTTPS in production
- **CORS**: Configured for trusted origins only
- **Input Validation**: Client-side and server-side validation
- **XSS Protection**: Vue's default template escaping used
- **CSRF**: Token included in session (if applicable)

---

## Performance Requirements

- Component load time: < 200ms
- API call response: < 1 second
- Form submission: < 3 seconds
- Mode switch: < 1 second
- Balance refresh: < 1 second
- Page transitions: Smooth (60fps)
