## Why

Binary option trading is a core revenue-generating feature for active traders. Our platform currently lacks a dedicated, professional-grade trading interface for Forex binary options. Users need a fast, intuitive panel to browse 18+ currency pairs, place UP/DOWN trades with configurable expiry times (30s–15m), and track real-time P&L. A fully-featured binary trading panel will drive user engagement, increase session duration, and unlock higher-margin revenue streams.

## What Changes

- Add a **Binary Trading Panel** with asset browser (Major/Minor/Exotic Forex pairs)
- Implement **live price simulation** with realistic market tick movement (~900ms updates)
- Enable **rapid trade placement**: select asset → set investment ($10–$5,000) → choose expiry → click UP or DOWN
- Auto-resolve trades at expiry with win/loss logic (85% payout on wins)
- Display **order history table** with P&L, status indicators, and live countdown timers
- Show **real-time account balance** in header and stats summary (total trades, win rate, net P&L)
- Use professional **dark terminal aesthetic** UI (provided in binary-options-panel.html)
- Support responsive design down to 900px width

## Capabilities

### New Capabilities
- `active-asset-selection`: Browse and select from 18 Forex pairs grouped by category (Major/Minor/Exotic); real-time visual highlighting of active selection
- `asset-management`: Display each asset with symbol, full name, live price, and percentage change; searchable by symbol or name
- `binary-trading`: Core trading panel with UP/DOWN direction buttons, configurable investment amount, expiry time selector, and payout display
- `real-time-quotes`: Client-side price simulation with realistic drift (±0.04% per tick) applied every 900ms; adaptive price formatting (3–5 decimals based on pair)
- `trade-execution`: Instant balance deduction on order placement, validation (min $10, max balance), and error messages
- `trade-history`: Order table with live status badges, countdown timers, and resolved P&L; auto-resolve logic & stats aggregation

### Modified Capabilities
*(None — this is a new self-contained panel)*

## Impact

**Frontend**:
- New Vue component: `BinaryTradingPanel.vue` (integrates HTML UI from binary-options-panel.html)
- New API service module: `tradingAPI.js` methods for quotes, trade execution, history retrieval
- State management: active asset, current balance, orders array, live price subscriptions
- Optional: WebSocket integration for backend-driven live quotes (future phase)

**Backend** *(Phase 2 — out of scope for initial UI proposal)*:
- Flask endpoints: `GET /api/trading/binary/quotes`, `POST /api/trading/binary/execute`, `GET /api/trading/binary/history`
- iqOption broker integration for real quotes (currently client-side simulated)
- Order persistence & settlement logic
- WebSocket server for live quote streaming

**Dependencies**:
- Frontend: Vue 3, Vite, Google Fonts (Share Tech Mono, Rajdhani)
- Backend (Phase 2): Flask-SocketIO, iqOption SDK, order database schema
