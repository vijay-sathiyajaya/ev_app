<template>
  <div class="binary-trading-panel">
    <header>
      <div style="display: flex; align-items: center; gap: 12px">
        <button @click="$emit('back')" class="btn-back" title="Back to dashboard">
          ← Back
        </button>
        <div class="logo">BINARY<span>FX</span></div>
      </div>
      <div class="header-info">
        <div class="bal-block">
          <div class="bal-label">Balance</div>
          <div class="bal-value" id="balanceDisplay">{{ formatBalance }}</div>
        </div>
        <button 
          @click="toggleTheme" 
          class="btn-theme" 
          :title="`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`"
        >
          {{ theme === 'light' ? '🌙' : '☀️' }}
        </button>
        <div class="live-dot"></div>
      </div>
    </header>

    <div class="main">
      <!-- ASSET PANEL -->
      <div class="asset-panel">
        <div class="panel-title">Forex Assets</div>
        <div class="search-wrap">
          <input
            type="text"
            id="assetSearch"
            placeholder="Search pair..."
            v-model="searchQuery"
            @input="filterAssets"
          />
        </div>
        <div class="asset-list" id="assetList">
          <div v-for="cat in categories" :key="cat" class="asset-category">
            {{ cat }}
          </div>
          <div
            v-for="asset in filteredAssets"
            :key="asset.symbol"
            class="asset-item"
            :class="{ active: asset.symbol === selectedAsset.symbol }"
            @click="selectAsset(asset.symbol)"
          >
            <div>
              <div class="asset-name">{{ asset.symbol }}</div>
              <div class="asset-sub">{{ asset.name }}</div>
            </div>
            <div class="asset-price-wrap">
              <div class="asset-price" v-if="prices[asset.symbol]">
                {{ formatPrice(asset.symbol, prices[asset.symbol]) }}
              </div>
              <div
                class="asset-change"
                :class="getPriceChangeClass(asset.symbol)"
              >
                {{ getPriceChange(asset.symbol) }}%
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT SIDE -->
      <div style="display: flex; flex-direction: column; overflow: hidden">
        <!-- TRADE AREA -->
        <div class="trade-area">
          <div class="trade-header">
            <div class="selected-asset">{{ selectedAsset.symbol }}</div>
            <div class="live-price">
              {{
                formatPrice(
                  selectedAsset.symbol,
                  prices[selectedAsset.symbol] || 0
                )
              }}
            </div>
          </div>

          <div class="trade-controls">
            <div class="control-group">
              <label>Investment Amount ($)</label>
              <input
                v-model.number="tradeAmount"
                type="number"
                min="10"
                max="5000"
                placeholder="100"
              />
            </div>
            <div class="control-group">
              <label>Expiry Time</label>
              <select v-model.number="tradeExpiry">
                <option value="30">30 seconds</option>
                <option value="60">1 minute</option>
                <option value="120">2 minutes</option>
                <option value="300">5 minutes</option>
                <option value="600">10 minutes</option>
                <option value="900">15 minutes</option>
              </select>
            </div>
            <div class="payout-badge">
              <div class="payout-label">Payout</div>
              <div class="payout-val">85%</div>
            </div>
          </div>

          <div style="margin-top: 14px">
            <div class="btn-group">
              <button class="btn-up" @click="placeOrder('UP')">
                <span class="btn-arrow">▲</span>CALL
              </button>
              <button class="btn-dn" @click="placeOrder('DOWN')">
                <span class="btn-arrow">▼</span>PUT
              </button>
            </div>
          </div>
        </div>

        <!-- ORDERS -->
        <div class="orders-area">
          <div class="orders-header">
            <div class="orders-title">
              Trade History
              <span class="order-count">{{ orders.length }}</span>
            </div>
            <button class="clear-btn" @click="clearOrders">Clear All</button>
          </div>

          <div class="orders-table-wrap">
            <table v-if="orders.length > 0">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Asset</th>
                  <th>Direction</th>
                  <th>Entry</th>
                  <th>Close</th>
                  <th>Amount</th>
                  <th>Expiry</th>
                  <th>Status</th>
                  <th>P&L</th>
                </tr>
              </thead>
              <tbody id="ordersBody">
                <tr v-for="order in orders" :key="order.id">
                  <td class="mono" style="color: var(--muted)">
                    #{{ String(order.id).padStart(3, "0") }}
                  </td>
                  <td>
                    <strong style="color: #e0ecff">{{ order.asset }}</strong>
                  </td>
                  <td>
                    <span
                      class="dir-badge"
                      :class="order.dir === 'UP' ? 'dir-up' : 'dir-dn'"
                    >
                      {{ order.dir === "UP" ? "▲ UP" : "▼ DOWN" }}
                    </span>
                  </td>
                  <td class="mono">
                    {{ formatPrice(order.asset, order.entryPrice) }}
                  </td>
                  <td class="mono">
                    {{
                      order.closePrice
                        ? formatPrice(order.asset, order.closePrice)
                        : "—"
                    }}
                  </td>
                  <td class="mono">${{ order.amount.toFixed(2) }}</td>
                  <td style="color: var(--muted)">
                    {{ order.expiry >= 60 ? (order.expiry / 60) | 0 + "m" : order.expiry + "s" }}
                  </td>
                  <td>
                    <span
                      v-if="order.status === 'PENDING'"
                      class="status-badge status-pending"
                    >
                      <span class="status-dot"></span>
                      PENDING {{ remainingSeconds(order) }}s
                    </span>
                    <span v-else-if="order.status === 'WON'" class="status-badge status-won">
                      <span class="status-dot"></span>WON
                    </span>
                    <span v-else class="status-badge status-lost">
                      <span class="status-dot"></span>LOST
                    </span>
                  </td>
                  <td>
                    <span
                      v-if="order.pnl === null"
                      style="color: var(--muted)"
                    >
                      —
                    </span>
                    <span v-else-if="order.pnl > 0" class="mono profit-pos">
                      +${{ order.pnl.toFixed(2) }}
                    </span>
                    <span v-else class="mono profit-neg">
                      −${{ Math.abs(order.pnl).toFixed(2) }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-else class="empty-state">
              <div class="icon">📊</div>
              <p>No orders yet. Select an asset and place a trade.</p>
            </div>
          </div>

          <div class="stats-row">
            <div class="stat-cell">
              <div class="stat-label">Total Trades</div>
              <div class="stat-value s-blue" id="statTotal">
                {{ orders.length }}
              </div>
            </div>
            <div class="stat-cell">
              <div class="stat-label">Won</div>
              <div class="stat-value s-green" id="statWon">
                {{ wonCount }}
              </div>
            </div>
            <div class="stat-cell">
              <div class="stat-label">Lost</div>
              <div class="stat-value s-red" id="statLost">
                {{ lostCount }}
              </div>
            </div>
            <div class="stat-cell">
              <div class="stat-label">Win Rate</div>
              <div class="stat-value s-gold" id="statRate">{{ winRate }}%</div>
            </div>
            <div class="stat-cell">
              <div class="stat-label">Net P&L</div>
              <div class="stat-value" :class="netPnlClass" id="statPnl">
                {{ netPnlDisplay }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";

// Theme props from App.vue
const props = defineProps({
  theme: {
    type: String,
    default: 'light'
  },
  colorVars: {
    type: Object,
    default: () => ({})
  }
});

// Emit theme toggle
const emit = defineEmits(['back', 'toggle-theme']);

// Theme toggle shortcut
const toggleTheme = () => {
  emit('toggle-theme');
};

// ─── FOREX DATA ─────────────────────────────────────────────
const ASSETS = [
  {
    symbol: "EUR/USD",
    name: "Euro / US Dollar",
    price: 1.08432,
    cat: "Major",
  },
  {
    symbol: "GBP/USD",
    name: "British Pound / USD",
    price: 1.27165,
    cat: "Major",
  },
  {
    symbol: "USD/JPY",
    name: "US Dollar / Japanese Yen",
    price: 149.842,
    cat: "Major",
  },
  {
    symbol: "USD/CHF",
    name: "US Dollar / Swiss Franc",
    price: 0.90321,
    cat: "Major",
  },
  {
    symbol: "AUD/USD",
    name: "Australian Dollar / USD",
    price: 0.65112,
    cat: "Major",
  },
  { symbol: "USD/CAD", name: "US Dollar / Canadian $", price: 1.3578, cat: "Major" },
  {
    symbol: "NZD/USD",
    name: "New Zealand Dollar / USD",
    price: 0.60455,
    cat: "Major",
  },
  {
    symbol: "EUR/GBP",
    name: "Euro / British Pound",
    price: 0.8527,
    cat: "Minor",
  },
  {
    symbol: "EUR/JPY",
    name: "Euro / Japanese Yen",
    price: 162.54,
    cat: "Minor",
  },
  {
    symbol: "GBP/JPY",
    name: "British Pound / Yen",
    price: 190.82,
    cat: "Minor",
  },
  {
    symbol: "EUR/AUD",
    name: "Euro / Australian Dollar",
    price: 1.6643,
    cat: "Minor",
  },
  {
    symbol: "GBP/CHF",
    name: "British Pound / CHF",
    price: 1.1514,
    cat: "Minor",
  },
  {
    symbol: "AUD/JPY",
    name: "Australian Dollar / Yen",
    price: 97.65,
    cat: "Minor",
  },
  {
    symbol: "USD/SGD",
    name: "US Dollar / Singapore $",
    price: 1.3453,
    cat: "Exotic",
  },
  {
    symbol: "USD/HKD",
    name: "US Dollar / HK Dollar",
    price: 7.8214,
    cat: "Exotic",
  },
  {
    symbol: "USD/MXN",
    name: "US Dollar / Mex Peso",
    price: 17.043,
    cat: "Exotic",
  },
  {
    symbol: "USD/ZAR",
    name: "US Dollar / South Afr Rand",
    price: 18.62,
    cat: "Exotic",
  },
  {
    symbol: "EUR/NOK",
    name: "Euro / Norwegian Krone",
    price: 11.643,
    cat: "Exotic",
  },
];

const categories = ["Major", "Minor", "Exotic"];
const prices = ref({});
const searchQuery = ref("");
const selectedAsset = ref(ASSETS[0]);
const balance = ref(10000);
const orders = ref([]);
const orderCounter = ref(0);
const tradeAmount = ref(100);
const tradeExpiry = ref(300);
let priceTickerInterval = null;
let orderResolutionTimeouts = [];

// ─── INITIALIZATION ─────────────────────────────────────────
const initPrices = () => {
  ASSETS.forEach((a) => {
    prices.value[a.symbol] = a.price;
  });
};

// ─── COMPUTED ───────────────────────────────────────────────
const filteredAssets = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return ASSETS.filter(
    (a) =>
      a.symbol.toLowerCase().includes(query) ||
      a.name.toLowerCase().includes(query)
  );
});

const formatBalance = computed(() =>
  "$" +
  balance.value.toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
);

const wonCount = computed(() =>
  orders.value.filter((o) => o.status === "WON").length
);

const lostCount = computed(() =>
  orders.value.filter((o) => o.status === "LOST").length
);

const completedCount = computed(() => wonCount.value + lostCount.value);

const winRate = computed(() => {
  if (completedCount.value === 0) return 0;
  return Math.round((wonCount.value / completedCount.value) * 100);
});

const netPnl = computed(() => {
  const completed = orders.value.filter((o) => o.status !== "PENDING");
  return completed.reduce((s, o) => s + (o.pnl || 0), 0);
});

const netPnlDisplay = computed(() => {
  const pnl = netPnl.value;
  return (pnl >= 0 ? "+" : "") + "$" + pnl.toFixed(2);
});

const netPnlClass = computed(() =>
  netPnl.value >= 0 ? "s-green" : "s-red"
);

// ─── METHODS ────────────────────────────────────────────────
const formatPrice = (symbol, price) => {
  if (!price) return "0.00";
  if (price > 100) return price.toFixed(3);
  if (price > 10) return price.toFixed(4);
  return price.toFixed(5);
};

const getPriceChange = (symbol) => {
  // Simplified: random change for demo
  return (Math.random() - 0.48).toFixed(2);
};

const getPriceChangeClass = (symbol) => {
  const change = getPriceChange(symbol);
  return parseFloat(change) >= 0 ? "up" : "dn";
};

const filterAssets = () => {
  // Vue reactivity handles this via computed
};

const selectAsset = (symbol) => {
  selectedAsset.value = ASSETS.find((a) => a.symbol === symbol);
};

const tickPrices = () => {
  ASSETS.forEach((a) => {
    const drift = (Math.random() - 0.499) * a.price * 0.0004;
    prices.value[a.symbol] = Math.max(0.0001, prices.value[a.symbol] + drift);
  });
};

const placeOrder = (dir) => {
  const amount = tradeAmount.value;
  const expiry = tradeExpiry.value;

  // Validation
  if (isNaN(amount) || amount < 10) {
    alert("Minimum investment is $10");
    return;
  }
  if (amount > balance.value) {
    alert("Insufficient balance");
    return;
  }

  // Deduct balance
  balance.value -= amount;

  // Create order
  orderCounter.value++;
  const entryPrice = prices.value[selectedAsset.value.symbol];
  const order = {
    id: orderCounter.value,
    asset: selectedAsset.value.symbol,
    dir,
    entryPrice,
    closePrice: null,
    amount,
    expiry,
    status: "PENDING",
    pnl: null,
    placedAt: Date.now(),
  };

  orders.value.unshift(order);

  // Schedule resolution
  const timeout = setTimeout(() => resolveOrder(order.id), expiry * 1000);
  orderResolutionTimeouts.push(timeout);
};

const resolveOrder = (id) => {
  const order = orders.value.find((o) => o.id === id);
  if (!order) return;

  order.closePrice = prices.value[order.asset];
  const priceUp = order.closePrice > order.entryPrice;
  const won =
    (order.dir === "UP" && priceUp) || (order.dir === "DOWN" && !priceUp);

  order.status = won ? "WON" : "LOST";
  order.pnl = won ? order.amount * 0.85 : -order.amount;

  if (won) {
    balance.value += order.amount + order.amount * 0.85;
  }
};

const remainingSeconds = (order) => {
  const elapsed = Date.now() - order.placedAt;
  const remaining = Math.max(0, Math.ceil((order.expiry * 1000 - elapsed) / 1000));
  return remaining;
};

const clearOrders = () => {
  if (!orders.value.length) return;
  if (confirm("Clear all completed orders?")) {
    orders.value = orders.value.filter((o) => o.status === "PENDING");
  }
};

// ─── LIFECYCLE ──────────────────────────────────────────────
onMounted(() => {
  initPrices();
  priceTickerInterval = setInterval(tickPrices, 900);

  // Re-render pending orders every 1 second for countdown
  const countdownInterval = setInterval(() => {
    if (orders.value.some((o) => o.status === "PENDING")) {
      // Force re-render
      orders.value = [...orders.value];
    }
  }, 1000);

  return () => {
    clearInterval(countdownInterval);
  };
});

onUnmounted(() => {
  if (priceTickerInterval) clearInterval(priceTickerInterval);
  orderResolutionTimeouts.forEach((timeout) => clearTimeout(timeout));
});
</script>

<style scoped>
:root {
  /* Dark theme (default) - original colors */
  --bg: #080c14;
  --panel: #0d1422;
  --border: #1a2540;
  --accent: #00d4ff;
  --green: #00ff88;
  --red: #ff3b5c;
  --gold: #f0c040;
  --text: #c8d8f0;
  --muted: #4a6080;
  --glow-g: 0 0 16px #00ff8866;
  --glow-r: 0 0 16px #ff3b5c66;
  --glow-a: 0 0 12px #00d4ff55;
}

.binary-trading-panel {
  /* Override with theme colors for light mode */
  --bg: v-bind("theme === 'light' ? '#f9f9fb' : '#080c14'");
  --panel: v-bind("theme === 'light' ? '#ffffff' : '#0d1422'");
  --border: v-bind("theme === 'light' ? '#e0e0e6' : '#1a2540'");
  --accent: v-bind("theme === 'light' ? '#667eea' : '#00d4ff'");
  --green: v-bind("theme === 'light' ? '#4caf50' : '#00ff88'");
  --red: v-bind("theme === 'light' ? '#f44336' : '#ff3b5c'");
  --gold: v-bind("theme === 'light' ? '#ff9800' : '#f0c040'");
  --text: v-bind("theme === 'light' ? '#333333' : '#c8d8f0'");
  --muted: v-bind("theme === 'light' ? '#999999' : '#4a6080'");
  --glow-g: v-bind("theme === 'light' ? '0 0 8px #4caf5044' : '0 0 16px #00ff8866'");
  --glow-r: v-bind("theme === 'light' ? '0 0 8px #f4433644' : '0 0 16px #ff3b5c66'");
  --glow-a: v-bind("theme === 'light' ? '0 0 6px #667eea44' : '0 0 12px #00d4ff55'");
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.binary-trading-panel {
  background: var(--bg);
  color: var(--text);
  font-family: "Rajdhani", sans-serif;
  font-size: 15px;
  min-height: 100vh;
  background-image: radial-gradient(ellipse 80% 40% at 50% 0%, #0a2040 0%,
      transparent 70%),
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 39px,
      #1a254008 39px,
      #1a254008 40px
    ),
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 39px,
      #1a254008 39px,
      #1a254008 40px
    );
  display: flex;
  flex-direction: column;
}

/* HEADER */
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 28px;
  background: #090e1a;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  font-family: "Share Tech Mono", monospace;
  font-size: 20px;
  color: var(--accent);
  letter-spacing: 3px;
  text-shadow: var(--glow-a);
}

.logo span {
  color: var(--gold);
}

.btn-back {
  background: rgba(0, 212, 255, 0.15);
  border: 1px solid var(--accent);
  color: var(--accent);
  font-family: "Rajdhani", sans-serif;
  font-size: 14px;
  font-weight: 600;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  letter-spacing: 1px;
}

.btn-back:hover {
  background: var(--accent);
  color: var(--bg);
  box-shadow: var(--glow-a);
}

.btn-theme {
  background: rgba(102, 126, 234, 0.15);
  border: 1px solid var(--accent);
  color: var(--accent);
  font-size: 18px;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-theme:hover {
  background: var(--accent);
  filter: brightness(1.2);
  box-shadow: var(--glow-a);
}

.header-info {
  display: flex;
  gap: 28px;
  align-items: center;
}

.bal-block {
  text-align: right;
}

.bal-label {
  font-size: 11px;
  color: var(--muted);
  letter-spacing: 2px;
  text-transform: uppercase;
}

.bal-value {
  font-family: "Share Tech Mono", monospace;
  font-size: 20px;
  color: var(--green);
}

.live-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--green);
  box-shadow: var(--glow-g);
  animation: pulse 1.4s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

/* LAYOUT */
.main {
  display: grid;
  grid-template-columns: 300px 1fr;
  grid-template-rows: auto 1fr;
  gap: 0;
  flex: 1;
  min-height: 0;
}

/* ASSET PANEL */
.asset-panel {
  background: var(--panel);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  grid-row: 1 / 3;
  overflow: hidden;
}

.panel-title {
  font-size: 11px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--muted);
  padding: 16px 18px 10px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-title::before {
  content: "";
  width: 3px;
  height: 14px;
  background: var(--accent);
  border-radius: 2px;
  box-shadow: var(--glow-a);
}

.search-wrap {
  padding: 12px 14px;
  border-bottom: 1px solid var(--border);
}

.search-wrap input {
  width: 100%;
  background: #0a1020;
  border: 1px solid var(--border);
  color: var(--text);
  font-family: "Rajdhani", sans-serif;
  font-size: 14px;
  padding: 8px 12px;
  border-radius: 4px;
  outline: none;
  transition: border-color 0.2s;
}

.search-wrap input:focus {
  border-color: var(--accent);
}

.search-wrap input::placeholder {
  color: var(--muted);
}

.asset-list {
  overflow-y: auto;
  flex: 1;
}

.asset-list::-webkit-scrollbar {
  width: 4px;
}

.asset-list::-webkit-scrollbar-track {
  background: transparent;
}

.asset-list::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 2px;
}

.asset-category {
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--muted);
  padding: 10px 18px 4px;
  text-transform: uppercase;
}

.asset-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 18px;
  cursor: pointer;
  border-left: 3px solid transparent;
  transition: all 0.15s;
  border-bottom: 1px solid #0d1422;
  gap: 10px;
}

.asset-item:hover {
  background: #111d30;
  border-left-color: var(--muted);
}

.asset-item.active {
  background: #0e1f36;
  border-left-color: var(--accent);
}

.asset-name {
  font-size: 15px;
  font-weight: 700;
  color: #e0ecff;
}

.asset-sub {
  font-size: 11px;
  color: var(--muted);
}

.asset-price-wrap {
  text-align: right;
}

.asset-price {
  font-family: "Share Tech Mono", monospace;
  font-size: 13px;
  color: var(--text);
}

.asset-change {
  font-size: 11px;
  font-weight: 600;
  margin-left: 4px;
  padding: 1px 5px;
  border-radius: 3px;
}

.asset-change.up {
  color: var(--green);
  background: #00ff8815;
}

.asset-change.dn {
  color: var(--red);
  background: #ff3b5c15;
}

/* TRADE AREA */
.trade-area {
  background: var(--bg);
  padding: 22px 24px;
  border-bottom: 1px solid var(--border);
}

.trade-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 20px;
}

.selected-asset {
  font-size: 26px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 1px;
}

.live-price {
  font-family: "Share Tech Mono", monospace;
  font-size: 24px;
  color: var(--accent);
  text-shadow: var(--glow-a);
  margin-left: auto;
}

.trade-controls {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 14px;
  align-items: end;
}

.control-group label {
  display: block;
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 6px;
}

.control-group input,
.control-group select {
  width: 100%;
  background: #0a1020;
  border: 1px solid var(--border);
  color: var(--text);
  font-family: "Share Tech Mono", monospace;
  font-size: 15px;
  padding: 10px 13px;
  border-radius: 5px;
  outline: none;
  transition: border-color 0.2s;
  appearance: none;
}

.control-group input:focus,
.control-group select:focus {
  border-color: var(--accent);
}

.btn-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.btn-up,
.btn-dn {
  padding: 13px 0;
  border: none;
  border-radius: 6px;
  font-family: "Rajdhani", sans-serif;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 2px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.15s;
  position: relative;
  overflow: hidden;
}

.btn-up {
  background: linear-gradient(135deg, #00c070, #00ff88);
  color: #001a0d;
  box-shadow: var(--glow-g);
}

.btn-up:hover {
  filter: brightness(1.15);
  transform: translateY(-1px);
}

.btn-dn {
  background: linear-gradient(135deg, #cc1e3a, #ff3b5c);
  color: #1a0008;
  box-shadow: var(--glow-r);
}

.btn-dn:hover {
  filter: brightness(1.15);
  transform: translateY(-1px);
}

.btn-up:active,
.btn-dn:active {
  transform: translateY(0);
}

.btn-arrow {
  font-size: 22px;
}

/* PAYOUT BADGE */
.payout-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #0a1020;
  border: 1px solid var(--border);
  padding: 10px 14px;
  border-radius: 5px;
}

.payout-label {
  font-size: 11px;
  letter-spacing: 2px;
  color: var(--muted);
  text-transform: uppercase;
}

.payout-val {
  font-family: "Share Tech Mono", monospace;
  font-size: 22px;
  color: var(--gold);
  margin-left: auto;
}

/* ORDERS */
.orders-area {
  background: var(--panel);
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.orders-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 22px;
  border-bottom: 1px solid var(--border);
}

.orders-title {
  font-size: 11px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--muted);
  display: flex;
  align-items: center;
  gap: 8px;
}

.orders-title::before {
  content: "";
  width: 3px;
  height: 14px;
  background: var(--gold);
  border-radius: 2px;
}

.order-count {
  background: #1a2540;
  color: var(--accent);
  font-family: "Share Tech Mono", monospace;
  font-size: 12px;
  padding: 2px 9px;
  border-radius: 20px;
}

.clear-btn {
  margin-left: auto;
  background: none;
  border: 1px solid var(--border);
  color: var(--muted);
  font-family: "Rajdhani", sans-serif;
  font-size: 12px;
  letter-spacing: 1px;
  padding: 4px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s;
}

.clear-btn:hover {
  border-color: var(--red);
  color: var(--red);
}

.orders-table-wrap {
  overflow-y: auto;
  flex: 1;
  min-height: 0;
}

.orders-table-wrap::-webkit-scrollbar {
  width: 4px;
}

.orders-table-wrap::-webkit-scrollbar-thumb {
  background: var(--border);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead th {
  font-size: 10px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
  text-align: left;
  padding: 10px 18px;
  border-bottom: 1px solid var(--border);
  background: #090e1a;
  position: sticky;
  top: 0;
}

tbody tr {
  border-bottom: 1px solid #0d1422;
  transition: background 0.12s;
  animation: rowIn 0.3s ease;
}

@keyframes rowIn {
  from {
    opacity: 0;
    transform: translateX(-12px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}

tbody tr:hover {
  background: #111d30;
}

tbody td {
  padding: 11px 18px;
  font-size: 14px;
}

.dir-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 10px;
  border-radius: 4px;
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 1px;
}

.dir-up {
  background: #00ff8818;
  color: var(--green);
  border: 1px solid #00ff8830;
}

.dir-dn {
  background: #ff3b5c18;
  color: var(--red);
  border: 1px solid #ff3b5c30;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1px;
}

.status-pending {
  background: #f0c04015;
  color: var(--gold);
  border: 1px solid #f0c04030;
}

.status-won {
  background: #00ff8818;
  color: var(--green);
  border: 1px solid #00ff8830;
}

.status-lost {
  background: #ff3b5c18;
  color: var(--red);
  border: 1px solid #ff3b5c30;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.status-pending .status-dot {
  background: var(--gold);
  animation: pulse 1s infinite;
}

.status-won .status-dot {
  background: var(--green);
}

.status-lost .status-dot {
  background: var(--red);
}

.mono {
  font-family: "Share Tech Mono", monospace;
}

.profit-pos {
  color: var(--green);
}

.profit-neg {
  color: var(--red);
}

.empty-state {
  text-align: center;
  padding: 48px 20px;
  color: var(--muted);
}

.empty-state .icon {
  font-size: 40px;
  margin-bottom: 12px;
  opacity: 0.4;
}

.empty-state p {
  letter-spacing: 1px;
  font-size: 13px;
}

/* STATS ROW */
.stats-row {
  display: flex;
  gap: 0;
  border-top: 1px solid var(--border);
  background: #090e1a;
}

.stat-cell {
  flex: 1;
  padding: 10px 18px;
  text-align: center;
  border-right: 1px solid var(--border);
}

.stat-cell:last-child {
  border-right: none;
}

.stat-label {
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--muted);
  text-transform: uppercase;
}

.stat-value {
  font-family: "Share Tech Mono", monospace;
  font-size: 18px;
  margin-top: 2px;
}

.s-green {
  color: var(--green);
}

.s-red {
  color: var(--red);
}

.s-gold {
  color: var(--gold);
}

.s-blue {
  color: var(--accent);
}

/* RESPONSIVE */
@media (max-width: 900px) {
  .main {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto 1fr;
    height: auto;
  }
  .asset-panel {
    grid-row: auto;
    max-height: 260px;
  }
  .trade-controls {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
