## Context

The application currently has:
- Vue 3 frontend with Vite build setup
- Flask backend with iqOption broker integration
- Account balance management and demo/live mode switching
- A complete, production-ready HTML UI for binary trading (binary-options-panel.html)

We need to integrate the HTML UI into the Vue component hierarchy and implement price/order logic using client-side simulation initially, with a path to real-time backend integration later.

## Goals / Non-Goals

**Goals:**
- Deliver a fully-functional binary trading panel using the provided HTML UI
- Implement all 6 capabilities (asset selection, management, trading, quotes, execution, history)
- Support real-time price simulation on the client
- Enable instant order placement, auto-resolution, and P&L calculation
- Provide responsive UI down to 900px width
- Create modular components for potential backend integration in Phase 2

**Non-Goals:**
- Backend integration (save orders to DB, process with iqOption API) — Phase 2 only
- WebSocket live quotes from backend — Phase 2 only
- Advanced charting or technical analysis tools
- Mobile optimization below 900px
- Order modification or cancellation after placement

## Decisions

### 1. Component Architecture: Single-File Component vs. Sub-components
**Decision:** Initially deliver as a single `BinaryTradingPanel.vue` component with all logic embedded. Refactor into sub-components (AssetPanel, TradeForm, OrderHistory) if component grows beyond 400 lines or during Phase 2 backend integration.

**Rationale:** Faster initial delivery without over-engineering. The provided HTML is self-contained; minimal refactoring needed to move to Vue.

**Alternatives Considered:**
- Split into sub-components now: adds complexity upfront; deferred to Phase 2 when backend calls create clear separation boundaries.

---

### 2. Price Data & Simulation
**Decision:** Implement client-side price simulation using JavaScript `setInterval()` (~900ms ticks) with random drift (±0.04% per tick). No backend calls for quotes.

**Rationale:** 18 assets + 900ms update frequency = manageable JavaScript workload. Provides instant visual feedback without network latency. Easy to swap for WebSocket later.

**Alternatives Considered:**
- Poll backend every 900ms: adds server load, network latency defeats purpose of binary trading UI responsiveness.
- Static prices: poor UX, breaks expiry resolution logic.

---

### 3. Order State Management
**Decision:** Use Vue's reactive `data()` object for orders array, prices object, and balance. No Vuex/Pinia needed at this scale.

**Rationale:** Single-panel scope, <100 orders typical per session. Direct state binding sufficient.

**Alternatives Considered:**
- Global store: overkill for Phase 1; add if UI expands to multiple trading panels.

---

### 4. Order Auto-Resolution
**Decision:** Use `setTimeout()` to fire resolution at expiry time. Resolve against live (simulated) price at that moment.

**Rationale:** Simple, immediate visual feedback. Browser handles timing reliably for <10-minute windows (within binary trade expiry range).

**Alternatives Considered:**
- Server-side resolution: requires persistent backend, adds Phase 2 scope.

---

### 5. UI Integration: HTML → Vue
**Decision:** Port the provided HTML directly into Vue template. Keep all CSS and JavaScript logic, adapt event handlers to Vue syntax (`@click`, `v-for`, etc.).

**Rationale:** HTML already tested and complete. Minimal translation layer. Vue reactivity will auto-update DOM on data changes.

**Alternatives Considered:**
- Rebuild from scratch using Vue component patterns: unnecessary rework, higher risk of UI divergence.

---

### 6. Payout & P&L Calculation
**Decision:** Fixed 85% payout ratio. On win: `balance += amount + (amount * 0.85)`. On loss: amount already deducted, no credit.

**Rationale:** Simple, matches business model in requirements. Configurable in backend Phase 2.

**Alternatives Considered:**
- Variable payout based on asset volatility: adds complexity; defer to Phase 2 if required.

---

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Client-side price simulation unrealistic** | Users may not trust trading signal | Phase 2: swap `tickPrices()` for WebSocket updates from iqOption; logic remains unchanged |
| **Order state lost on page refresh** | Negative UX; users lose order history | Phase 2: persist orders to backend DB; sessionStorage fallback for MVP |
| **No validation on backend** | Malicious clients could manipulate balance | Phase 2: re-validate all orders on backend; use JWT/session tokens |
| **Component scaling** | Single 500+ line component becomes hard to maintain | Plan refactoring to sub-components during Phase 2 backend integration |
| **Timezone issues with expiry** | User's local time ≠ server's time (Phase 2) | Phase 2: all expirations driven by server timestamp, not client clock |

---

## Migration Plan

### Phase 1 (Current): Client-Side MVP
1. Port binary-options-panel.html to `src/components/BinaryTradingPanel.vue`
2. Implement price simulation, order placement, auto-resolution
3. Test all 6 capabilities locally
4. Deploy as standalone route (e.g., `/trading/binary`)

### Phase 2 (Future): Backend Integration
1. Create Flask endpoints: `/api/trading/binary/quotes`, `/api/trading/binary/execute`, `/api/trading/binary/history`
2. Replace `tickPrices()` with WebSocket subscription to real quotes
3. Replace `placeOrder()` & `resolveOrder()` with API calls
4. Persist orders to database; implement settlement logic
5. Refactor component into sub-components if needed

### Rollback Strategy
- Phase 1 rollback: remove route from navigation; keep code in git history for reference.
- Phase 2 rollback: if backend integration has bugs, revert to client-side simulation by uncommenting Phase 1 logic.

---

## Open Questions

1. **Account mode context:** Should demo/live mode affect this panel, or is binary trading only in one mode?
   - *Assumption for now:* Panel works in both modes; balance switches with account type.
   
2. **Order history persistence:** Phase 1 loses orders on refresh. Acceptable for MVP?
   - *Assumption for now:* Yes; add sessionStorage backup if needed.

3. **Integration point:** Where in the dashboard does the binary trading panel appear?
   - *Assumption for now:* New route `/trading/binary`, accessible from main nav.

4. **Real iqOption integration timeline:** Can Phase 2 wait, or is there pressure to integrate sooner?
   - *Assumption for now:* Can defer; Phase 1 is feature-complete for testing.
