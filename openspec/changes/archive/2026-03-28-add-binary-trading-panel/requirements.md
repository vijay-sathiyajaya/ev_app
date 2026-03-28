# Binary Options Trading Panel — Requirements

## 1. Project Overview

A browser-based Binary Options Trading Panel for Forex currency pairs. Users can browse assets, place UP or DOWN trades with a defined investment and expiry, and track order results in real time.

---

## 2. Functional Requirements

### 2.1 Asset Management

| ID | Requirement |
|----|-------------|
| F-01 | Display a list of Forex currency pairs grouped into **Major**, **Minor**, and **Exotic** categories |
| F-02 | Each asset entry must show: symbol (e.g. EUR/USD), full name, live price, and percentage change |
| F-03 | Provide a **search/filter** input to filter assets by symbol or name in real time |
| F-04 | User must be able to **select any asset** from the list to load it into the trade panel |
| F-05 | The active/selected asset must be visually highlighted in the list |

---

### 2.2 Live Price Simulation

| ID | Requirement |
|----|-------------|
| F-06 | All asset prices must simulate live market movement with a random drift applied every ~900ms |
| F-07 | The selected asset's live price must update continuously in the trade header |
| F-08 | Price formatting must adapt to the asset (e.g. 5 decimals for major pairs, 3 for JPY pairs) |

---

### 2.3 Trade Placement

| ID | Requirement |
|----|-------------|
| F-09 | Display the selected asset name, full description, and live price in the trade header |
| F-10 | User must be able to input an **investment amount** (minimum: $10, maximum: $5,000) |
| F-11 | User must be able to select an **expiry time** from: 30s, 1m, 2m, 5m, 10m, 15m |
| F-12 | Display a fixed **payout return rate** of 85% |
| F-13 | Provide two trade direction buttons: **▲ CALL / UP** and **▼ PUT / DOWN** |
| F-14 | On order placement, **deduct the investment amount** from the user's account balance immediately |
| F-15 | Prevent order placement if the investment amount exceeds the current balance |
| F-16 | Prevent order placement if the investment amount is below $10 |

---

### 2.4 Order Management

| ID | Requirement |
|----|-------------|
| F-17 | All placed orders must be listed in an **order history table** |
| F-18 | Each order row must display: Order ID, Asset, Direction, Entry Price, Close Price, Amount, Expiry, Status, P&L |
| F-19 | New orders must appear at the **top** of the order list |
| F-20 | Pending orders must display a **live countdown timer** showing remaining seconds |
| F-21 | Orders must **auto-resolve** when the expiry time elapses |
| F-22 | Resolution logic: if direction is UP and close price > entry price → **WON**; otherwise → **LOST** (and vice versa for DOWN) |
| F-23 | Won trades credit the user balance with: **original amount + (amount × 85%)** |
| F-24 | Display P&L per order: positive in green (e.g. +$85.00), negative in red (e.g. -$100.00) |
| F-25 | Provide a **Clear All** button to remove completed (non-pending) orders |

---

### 2.5 Account Balance

| ID | Requirement |
|----|-------------|
| F-26 | Display the current account balance persistently in the **header** |
| F-27 | Starting balance is **$10,000.00** |
| F-28 | Balance must update instantly on trade placement and on trade resolution |

---

### 2.6 Statistics Summary

| ID | Requirement |
|----|-------------|
| F-29 | Display a stats bar with: **Total Trades**, **Won**, **Lost**, **Win Rate (%)**, **Net P&L** |
| F-30 | Stats must update dynamically as orders are placed and resolved |
| F-31 | Net P&L must be color-coded: green for positive, red for negative |

---

## 3. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NF-01 | The UI must be a **single self-contained HTML file** (no external dependencies except Google Fonts) |
| NF-02 | The panel must be **responsive** and usable on screen widths down to 900px |
| NF-03 | All price ticks and order resolutions must occur **client-side** with no backend required |
| NF-04 | New order rows must animate in smoothly (slide + fade) |
| NF-05 | Pending order status badges must pulse to indicate active state |
| NF-06 | The interface must use a **dark terminal/trading aesthetic** with a clear color language |

---

## 4. UI / Design Requirements

| ID | Requirement |
|----|-------------|
| D-01 | Color language: **Green** = UP / WIN, **Red** = DOWN / LOSS, **Gold** = stats/payout, **Cyan** = accent/live price |
| D-02 | Use monospace font (`Share Tech Mono`) for all price and numeric values |
| D-03 | Use `Rajdhani` display font for labels, buttons, and headings |
| D-04 | Asset panel is fixed on the left with independent scrolling |
| D-05 | Trade controls and order history occupy the right pane |
| D-06 | Stats bar is pinned to the bottom of the order history panel |
| D-07 | Live indicator dot in the header must pulse continuously |

---

## 5. Asset Data

### Major Pairs
EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD, NZD/USD

### Minor Pairs
EUR/GBP, EUR/JPY, GBP/JPY, EUR/AUD, GBP/CHF, AUD/JPY

### Exotic Pairs
USD/SGD, USD/HKD, USD/MXN, USD/ZAR, EUR/NOK

---

## 6. Order Status Definitions

| Status | Description |
|--------|-------------|
| PENDING | Order placed, expiry timer is running |
| WON | Expiry elapsed, price moved in predicted direction |
| LOST | Expiry elapsed, price moved against predicted direction |

---

## 7. Payout Calculation

| Outcome | Formula |
|---------|---------|
| Win | `Balance += Amount + (Amount × 0.85)` |
| Loss | `Balance` unchanged (amount already deducted at placement) |
| Net P&L (Win) | `+Amount × 0.85` |
| Net P&L (Loss) | `-Amount` |
