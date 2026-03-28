## 1. Project Setup & Directory Structure

- [x] 1.1 Create `src/components/BinaryTradingPanel.vue` Vue component file
- [x] 1.2 Create `src/services/binaryApi.js` service module for API calls
- [x] 1.3 Verify Vite build includes Vue 3 and necessary dev dependencies
- [x] 1.4 Add route for `/trading/binary` in router configuration
- [x] 1.5 Add navigation link to Binary Trading Panel in main dashboard

## 2. Component Scaffolding & HTML Structure

- [x] 2.1 Port HTML from binary-options-panel.html into BinaryTradingPanel.vue template
- [x] 2.2 Preserve all CSS styles in component's `<style scoped>` block
- [x] 2.3 Set up Vue data properties: assets, prices, selectedAsset, balance, orders, orderCounter
- [x] 2.4 Initialize default asset (EUR/USD) and starting balance ($10,000)
- [x] 2.5 Extract JavaScript logic from HTML and organize into Vue methods

## 3. Asset Management Implementation

- [x] 3.1 Define 18 Forex pairs in ASSETS array with metadata (symbol, name, category, initial price)
- [x] 3.2 Implement `renderAssets()` method to display assets grouped by category
- [x] 3.3 Implement `filterAssets()` method to search/filter by symbol or name in real-time
- [x] 3.4 Implement `selectAsset()` method to update selected asset and trade header
- [x] 3.5 Add CSS styling for active asset highlighting (cyan border, darker background)
- [x] 3.6 Test asset selection updates trade header with correct symbol and price

## 4. Real-Time Price Simulation

- [x] 4.1 Implement `tickPrices()` method to update all prices every 900ms
- [x] 4.2 Calculate realistic price drift: ±0.04% per tick per asset
- [x] 4.3 Add price floor validation (prevent prices below 0.0001)
- [x] 4.4 Implement `formatPrice()` method for adaptive decimal formatting (2–5 places)
- [x] 4.5 Set up `setInterval(tickPrices, 900)` on component mount
- [x] 4.6 Clear interval on component unmount to prevent memory leaks
- [x] 4.7 Update selected asset price in trade header at each tick
- [x] 4.8 Update asset list prices and percentage change badges at each tick
- [x] 4.9 Test price movement stays within realistic bounds (±2% over 30+ ticks)

## 5. Trade Execution & Balance Management

- [x] 5.1 Implement `placeOrder()` method triggered by UP/DOWN button clicks
- [x] 5.2 Add input validation: amount >= $10, amount <= $5,000, amount <= balance
- [x] 5.3 Display error alerts for invalid inputs (min/max/insufficient balance)
- [x] 5.4 Deduct investment amount from balance immediately on order placement
- [x] 5.5 Create order object with ID, asset, direction, entry price, amount, expiry, status
- [x] 5.6 Increment orderCounter for unique order IDs (#001, #002, etc.)
- [x] 5.7 Add to orders array at front (newest first)
- [x] 5.8 Update balance display in header after deduction
- [x] 5.9 Prevent multiple rapid orders from overdrafting (atomic balance updates)
- [x] 5.10 Test order placement with valid and invalid amounts

## 6. Order Auto-Resolution & Resolution Logic

- [x] 6.1 Implement `resolveOrder()` method called via setTimeout
- [x] 6.2 Calculate order resolution timing based on expiry seconds
- [x] 6.3 Implement resolution logic for UP orders: close price > entry price = WON else LOST
- [x] 6.4 Implement resolution logic for DOWN orders: close price < entry price = WON else LOST
- [x] 6.5 On WIN: credit balance with amount + (amount × 0.85), set order.pnl = +amount × 0.85
- [x] 6.6 On LOSS: do not credit balance (already deducted), set order.pnl = −amount
- [x] 6.7 Set order status to WON or LOST based on outcome
- [x] 6.8 Populate order.closePrice with actual price at resolution
- [x] 6.9 Test resolution with multiple concurrent orders
- [x] 6.10 Verify balance updates correctly for wins and losses

## 7. Order Display & Order History Table

- [x] 7.1 Implement `renderOrders()` method to build order history table HTML
- [x] 7.2 Display column headers: Order ID, Asset, Direction, Entry Price, Close Price, Amount, Expiry, Status, P&L
- [x] 7.3 Format order ID with leading zeros (#001, #002, etc.)
- [x] 7.4 Implement direction badge styling (UP in green with ▲, DOWN in red with ▼)
- [x] 7.5 Format prices with adaptive decimal places (using `formatPrice()`)
- [x] 7.6 Display "—" for close price on pending orders
- [x] 7.7 Implement live countdown timer display for PENDING orders
- [x] 7.8 Update countdown every 1 second by calling `renderOrders()` if pending orders exist
- [x] 7.9 Implement status badges (PENDING in gold with pulsing dot, WON in green, LOST in red)
- [x] 7.10 Display P&L as "+$85.00" (green) for wins, "−$100.00" (red) for losses
- [x] 7.11 Test order table updates correctly as trades execute and resolve

## 8. Statistics Summary & Aggregation

- [x] 8.1 Implement `updateStats()` method to calculate aggregated metrics
- [x] 8.2 Calculate Total Trades: count of all orders (pending + completed)
- [x] 8.3 Calculate Won: count of orders with status = WON
- [x] 8.4 Calculate Lost: count of orders with status = LOST
- [x] 8.5 Calculate Win Rate: (Won / (Won + Lost) × 100) % when completed > 0
- [x] 8.6 Calculate Net P&L: sum of all order.pnl values for completed orders
- [x] 8.7 Apply color coding to Net P&L (green for positive, red for negative)
- [x] 8.8 Update stats bar at bottom of order table after each order resolution
- [x] 8.9 Display stats with monospace font for numeric values
- [x] 8.10 Test stats calculations with various order outcomes

## 9. Order List Management & Clearing

- [x] 9.1 Implement `clearOrders()` method
- [x] 9.2 Add confirmation dialog: "Clear all completed orders?"
- [x] 9.3 Filter and remove only non-PENDING orders (WON/LOST)
- [x] 9.4 Keep PENDING orders in the table
- [x] 9.5 Display empty state message when order table is empty
- [x] 9.6 Test clear functionality with mixed pending/completed orders

## 10. UI Refinements & Styling

- [x] 10.1 Verify dark theme aesthetic (dark backgrounds, accent colors match requirements)
- [x] 10.2 Implement button hover effects (brightness +15%, translateY -1px)
- [x] 10.3 Implement button active states (no translation)
- [x] 10.4 Add pulsing animation to live indicator dot in header
- [x] 10.5 Add smooth row animations for order table (slide + fade on entry)
- [x] 10.6 Test responsive layout at 900px viewport width
- [x] 10.7 Verify all color blindness considerations (don't rely on color alone for status)
- [x] 10.8 Test font sizes and readability at various zoom levels

## 11. Event Handling & Vue Integration

- [x] 11.1 Bind asset click events to `selectAsset()` method
- [x] 11.2 Bind search input to `filterAssets()` with `@input` event
- [x] 11.3 Bind UP/DOWN buttons to `placeOrder()` with correct direction parameter
- [x] 11.4 Bind "Clear All" button to `clearOrders()` method
- [x] 11.5 Use v-for to render assets and orders from reactive arrays
- [x] 11.6 Use v-if/v-show for conditional rendering (empty states, badges, etc.)
- [x] 11.7 Use class binding for dynamic styling (active asset, status badges, P&L color)
- [x] 11.8 Test all event handlers work correctly

## 12. Component Lifecycle & Memory Management

- [x] 12.1 Initialize price ticker in `mounted()` hook
- [x] 12.2 Clear price ticker interval in `unmounted()` hook
- [x] 12.3 Clear any pending setTimeout timeouts on component unmount
- [x] 12.4 Test component mount/unmount cycles don't leak memory
- [x] 12.5 Test navigating away from panel stops price updates

## 13. Data Validation & Error Handling

- [x] 13.1 Validate investment amount is a number
- [x] 13.2 Validate expiry time is in allowed list
- [x] 13.3 Handle division by zero in Win Rate calculation
- [x] 13.4 Handle empty order array in stats calculations
- [x] 13.5 Test edge cases (zero balance, single order, rapid order placement)

## 14. Testing & Quality Assurance

- [x] 14.1 Test all 6 capabilities meet spec requirements
- [x] 14.2 Place 10+ orders and verify balance tracking accuracy
- [x] 14.3 Test order resolution with various entry/close price relationships
- [x] 14.4 Test win rate calculation with mixed outcomes (5 won, 3 lost, 2 pending)
- [x] 14.5 Verify P&L calculations match 85% payout ratio
- [x] 14.6 Test price formatting for Major/Minor/Exotic pairs
- [x] 14.7 Test asset search/filter with partial matches
- [x] 14.8 Test order table countdown timers update correctly every second
- [x] 14.9 Test responsive design at 900px, 768px, and mobile widths
- [x] 14.10 Cross-browser test (Chrome, Firefox, Safari, Edge)

## 15. Documentation & Handoff

- [ ] 15.1 Add inline JSDoc comments to key methods
- [ ] 15.2 Document component props, data, and methods in code comments
- [ ] 15.3 Create README section explaining Binary Trading Panel architecture
- [ ] 15.4 Document Phase 2 integration points (backend API endpoints, WebSocket)
- [ ] 15.5 List known limitations and future improvements
- [ ] 15.6 Prepare for code review with commit messages

## 16. Phase 2 Preparation

- [ ] 16.1 Identify backend API endpoints needed (quotes, execute, history)
- [ ] 16.2 Plan WebSocket integration for real quote updates
- [ ] 16.3 Design order persistence schema for database
- [ ] 16.4 Document migration path from client-side to server-side resolution
- [ ] 16.5 Plan sub-component refactoring (AssetPanel, TradeForm, OrderHistory)
