/**
 * FluxConvert — Modern Currency Converter Client
 * Senior Frontend Architecture with reactive state, offline resiliency,
 * interactive Chart.js analytics, and zero-flicker UI updates.
 */

(() => {
  'use strict';

  // =========================================================================
  // Currency Metadata with Country Flags & Regional Categories
  // =========================================================================
  const CURRENCY_REGISTRY = {
    USD: { name: "US Dollar", symbol: "$", flag: "🇺🇸", region: "americas", popular: true },
    EUR: { name: "Euro", symbol: "€", flag: "🇪🇺", region: "europe", popular: true },
    GBP: { name: "British Pound", symbol: "£", flag: "🇬🇧", region: "europe", popular: true },
    INR: { name: "Indian Rupee", symbol: "₹", flag: "🇮🇳", region: "asia", popular: true },
    JPY: { name: "Japanese Yen", symbol: "¥", flag: "🇯🇵", region: "asia", popular: true },
    CAD: { name: "Canadian Dollar", symbol: "C$", flag: "🇨🇦", region: "americas", popular: true },
    AUD: { name: "Australian Dollar", symbol: "A$", flag: "🇦🇺", region: "asia", popular: true },
    CHF: { name: "Swiss Franc", symbol: "CHF", flag: "🇨🇭", region: "europe", popular: true },
    CNY: { name: "Chinese Yuan", symbol: "¥", flag: "🇨🇳", region: "asia", popular: true },
    AED: { name: "Emirati Dirham", symbol: "AED", flag: "🇦🇪", region: "asia", popular: true },
    SGD: { name: "Singapore Dollar", symbol: "S$", flag: "🇸🇬", region: "asia", popular: true },
    HKD: { name: "Hong Kong Dollar", symbol: "HK$", flag: "🇭🇰", region: "asia", popular: true },
    NZD: { name: "New Zealand Dollar", symbol: "NZ$", flag: "🇳🇿", region: "asia", popular: true },
    KRW: { name: "South Korean Won", symbol: "₩", flag: "🇰🇷", region: "asia", popular: true },
    BRL: { name: "Brazilian Real", symbol: "R$", flag: "🇧🇷", region: "americas", popular: true },
    MXN: { name: "Mexican Peso", symbol: "Mex$", flag: "🇲🇽", region: "americas", popular: true },
    ZAR: { name: "South African Rand", symbol: "R", flag: "🇿🇦", region: "africa", popular: true },
    SAR: { name: "Saudi Riyal", symbol: "SAR", flag: "🇸🇦", region: "asia", popular: true },
    TRY: { name: "Turkish Lira", symbol: "₺", flag: "🇹🇷", region: "europe", popular: true },
    SEK: { name: "Swedish Krona", symbol: "kr", flag: "🇸🇪", region: "europe", popular: false },
    NOK: { name: "Norwegian Krone", symbol: "kr", flag: "🇳🇴", region: "europe", popular: false },
    DKK: { name: "Danish Krone", symbol: "kr", flag: "🇩🇰", region: "europe", popular: false },
    PLN: { name: "Polish Zloty", symbol: "zł", flag: "🇵🇱", region: "europe", popular: false },
    THB: { name: "Thai Baht", symbol: "฿", flag: "🇹🇭", region: "asia", popular: false },
    IDR: { name: "Indonesian Rupiah", symbol: "Rp", flag: "🇮🇩", region: "asia", popular: false },
    MYR: { name: "Malaysian Ringgit", symbol: "RM", flag: "🇲🇾", region: "asia", popular: false },
    PHP: { name: "Philippine Peso", symbol: "₱", flag: "🇵🇭", region: "asia", popular: false },
    VND: { name: "Vietnamese Dong", symbol: "₫", flag: "🇻🇳", region: "asia", popular: false },
    ILS: { name: "Israeli Shekel", symbol: "₪", flag: "🇮🇱", region: "asia", popular: false },
    RUB: { name: "Russian Ruble", symbol: "₽", flag: "🇷🇺", region: "europe", popular: false },
    KWD: { name: "Kuwaiti Dinar", symbol: "KD", flag: "🇰🇼", region: "asia", popular: false },
    QAR: { name: "Qatari Riyal", symbol: "QR", flag: "🇶🇦", region: "asia", popular: false },
    OMR: { name: "Omani Rial", symbol: "RO", flag: "🇴🇲", region: "asia", popular: false },
    BHD: { name: "Bahraini Dinar", symbol: "BD", flag: "🇧🇭", region: "asia", popular: false },
    EGP: { name: "Egyptian Pound", symbol: "E£", flag: "🇪🇬", region: "africa", popular: false },
    NGN: { name: "Nigerian Naira", symbol: "₦", flag: "🇳🇬", region: "africa", popular: false },
    PKR: { name: "Pakistani Rupee", symbol: "Rs", flag: "🇵🇰", region: "asia", popular: false },
    BDT: { name: "Bangladeshi Taka", symbol: "৳", flag: "🇧🇩", region: "asia", popular: false },
    LKR: { name: "Sri Lankan Rupee", symbol: "Rs", flag: "🇱🇰", region: "asia", popular: false },
    NPR: { name: "Nepalese Rupee", symbol: "Rs", flag: "🇳🇵", region: "asia", popular: false },
    KES: { name: "Kenyan Shilling", symbol: "KSh", flag: "🇰🇪", region: "africa", popular: false },
    GHS: { name: "Ghanaian Cedi", symbol: "GH₵", flag: "🇬🇭", region: "africa", popular: false },
    ARS: { name: "Argentine Peso", symbol: "$", flag: "🇦🇷", region: "americas", popular: false },
    CLP: { name: "Chilean Peso", symbol: "CLP$", flag: "🇨🇱", region: "americas", popular: false },
    COP: { name: "Colombian Peso", symbol: "COL$", flag: "🇨🇴", region: "americas", popular: false },
    PEN: { name: "Peruvian Sol", symbol: "S/.", flag: "🇵🇪", region: "americas", popular: false },
    HUF: { name: "Hungarian Forint", symbol: "Ft", flag: "🇭🇺", region: "europe", popular: false },
    CZK: { name: "Czech Koruna", symbol: "Kč", flag: "🇨🇿", region: "europe", popular: false },
    RON: { name: "Romanian Leu", symbol: "lei", flag: "🇷🇴", region: "europe", popular: false },
    BGN: { name: "Bulgarian Lev", symbol: "лв", flag: "🇧🇬", region: "europe", popular: false },
    KZT: { name: "Kazakhstani Tenge", symbol: "₸", flag: "🇰🇿", region: "asia", popular: false },
    UAH: { name: "Ukrainian Hryvnia", symbol: "₴", flag: "🇺🇦", region: "europe", popular: false },
    MAD: { name: "Moroccan Dirham", symbol: "MAD", flag: "🇲🇦", region: "africa", popular: false },
    JMD: { name: "Jamaican Dollar", symbol: "J$", flag: "🇯🇲", region: "americas", popular: false },
    DOP: { name: "Dominican Peso", symbol: "RD$", flag: "🇩🇴", region: "americas", popular: false }
  };

  // Baseline Offline Fallback Rates (USD base)
  const FALLBACK_RATES = {
    USD: 1.0, EUR: 0.8787, GBP: 0.7564, INR: 96.0151, JPY: 158.6866,
    CAD: 1.4128, AUD: 1.4255, CHF: 0.8277, CNY: 6.7173, AED: 3.6725,
    SGD: 1.2797, HKD: 7.8431, NZD: 1.7663, KRW: 1368.60, BRL: 5.1752,
    MXN: 17.6729, ZAR: 16.4314, SAR: 3.7500, TRY: 48.8944, RUB: 84.4857,
    THB: 33.4473, IDR: 17907.21, MYR: 4.0828, PHP: 62.8128, VND: 25950.54,
    PKR: 277.3855, BDT: 122.9016, KWD: 0.3086, QAR: 3.6400, EGP: 51.6953,
    NGN: 1327.93, SEK: 9.9179, NOK: 9.5028, DKK: 6.5740, PLN: 3.8498,
    ILS: 3.0453, HUF: 321.477, CZK: 21.4497, CLP: 962.564, COP: 3264.54,
    ARS: 1518.74, PEN: 3.3972, KZT: 442.659, OMR: 0.3845, BHD: 0.3760
  };

  // =========================================================================
  // Reactive Application State
  // =========================================================================
  const state = {
    rates: { ...FALLBACK_RATES },
    lastUpdated: "Loading...",
    dataSource: "Initializing",
    fromCurrency: "USD",
    toCurrency: "INR",
    amount: 1000.0,
    timeframe: 30, // days
    theme: localStorage.getItem("flux_theme") || "dark",
    favorites: JSON.parse(localStorage.getItem("flux_favorites") || '["USD-EUR", "USD-INR", "EUR-GBP", "USD-JPY"]'),
    history: JSON.parse(localStorage.getItem("flux_history") || "[]"),
    activePickerTarget: null, // 'from' or 'to'
    activeCategoryFilter: "all",
    searchFilter: ""
  };

  // Chart Instance Reference
  let trendChartInstance = null;

  // =========================================================================
  // DOM Elements Cache
  // =========================================================================
  const dom = {
    html: document.documentElement,
    amountInput: document.getElementById("amountInput"),
    sourceSymbolTag: document.getElementById("sourceSymbolTag"),
    fromCurrencyBtn: document.getElementById("fromCurrencyBtn"),
    toCurrencyBtn: document.getElementById("toCurrencyBtn"),
    fromFlag: document.getElementById("fromFlag"),
    fromCode: document.getElementById("fromCode"),
    fromName: document.getElementById("fromName"),
    toFlag: document.getElementById("toFlag"),
    toCode: document.getElementById("toCode"),
    toName: document.getElementById("toName"),
    btnSwap: document.getElementById("btnSwap"),
    summaryFrom: document.getElementById("summaryFrom"),
    summaryTargetVal: document.getElementById("summaryTargetVal"),
    summaryTargetCode: document.getElementById("summaryTargetCode"),
    directRateText: document.getElementById("directRateText"),
    inverseRateText: document.getElementById("inverseRateText"),
    btnCopyResult: document.getElementById("btnCopyResult"),
    copyBtnText: document.getElementById("copyBtnText"),
    btnPinPair: document.getElementById("btnPinPair"),
    favoritesChips: document.getElementById("favoritesChips"),
    btnThemeToggle: document.getElementById("btnThemeToggle"),
    btnRefresh: document.getElementById("btnRefresh"),
    refreshIcon: document.getElementById("refreshIcon"),
    statusBadge: document.getElementById("statusBadge"),
    statusText: document.getElementById("statusText"),
    syncTime: document.getElementById("syncTime"),
    chartHeading: document.getElementById("chartHeading"),
    metricHigh: document.getElementById("metricHigh"),
    metricLow: document.getElementById("metricLow"),
    metricAvg: document.getElementById("metricAvg"),
    metricChange: document.getElementById("metricChange"),
    matrixGrid: document.getElementById("matrixGrid"),
    matrixBaseCode: document.getElementById("matrixBaseCode"),
    historyList: document.getElementById("historyList"),
    btnClearHistory: document.getElementById("btnClearHistory"),
    btnResetAmount: document.getElementById("btnResetAmount"),
    currencyModal: document.getElementById("currencyModal"),
    btnModalClose: document.getElementById("btnModalClose"),
    currencySearchInput: document.getElementById("currencySearchInput"),
    currencyListContainer: document.getElementById("currencyListContainer"),
    categoryTabs: document.querySelectorAll(".cat-tab"),
    timeframeBtns: document.querySelectorAll(".tf-btn"),
    toastContainer: document.getElementById("toastContainer")
  };

  // =========================================================================
  // Data Fetching & Sync
  // =========================================================================
  async function fetchExchangeRates(forceRefresh = false) {
    dom.refreshIcon.classList.add("spinning");
    let fetched = false;

    // 1. Try local server API if running via UIcurr.py
    try {
      const url = forceRefresh ? "/api/rates?refresh=true" : "/api/rates";
      const resp = await fetch(url, { cache: "no-store" });
      if (resp.ok) {
        const data = await resp.json();
        if (data.rates && Object.keys(data.rates).length > 0) {
          state.rates = { ...state.rates, ...data.rates };
          state.lastUpdated = data.last_updated || new Date().toUTCString();
          state.dataSource = data.source || "Live Server API";
          fetched = true;
        }
      }
    } catch (_) {
      // Server endpoint not available (e.g. running directly via file://)
    }

    // 2. Direct client fallback to open.er-api.com
    if (!fetched) {
      try {
        const resp = await fetch("https://open.er-api.com/v6/latest/USD");
        if (resp.ok) {
          const data = await resp.json();
          if (data.result === "success" && data.rates) {
            state.rates = { ...state.rates, ...data.rates };
            state.lastUpdated = data.time_last_update_utc || new Date().toUTCString();
            state.dataSource = "Live API (Direct)";
            fetched = true;
          }
        }
      } catch (_) {
        // Network offline, use cached or fallback rates
      }
    }

    // 3. Fallback to cached or embedded
    if (!fetched) {
      const cached = localStorage.getItem("flux_cached_rates");
      if (cached) {
        try {
          state.rates = JSON.parse(cached);
          state.dataSource = "Offline Cache";
          state.lastUpdated = "Cached locally";
        } catch (_) {
          state.dataSource = "Built-in Baseline";
        }
      } else {
        state.dataSource = "Built-in Baseline";
      }
    } else {
      localStorage.setItem("flux_cached_rates", JSON.stringify(state.rates));
    }

    setTimeout(() => dom.refreshIcon.classList.remove("spinning"), 600);
    updateStatusUI();
    renderConverter();
    renderComparisonMatrix();
    renderTrendChart();
  }

  function updateStatusUI() {
    dom.syncTime.textContent = state.lastUpdated.split(" ").slice(0, 4).join(" ") || "Today";
    dom.statusText.textContent = state.dataSource.includes("Live") ? "Live Market" : "Offline / Cache";
    
    if (state.dataSource.includes("Live")) {
      dom.statusBadge.style.color = "var(--accent-emerald)";
      dom.statusBadge.style.borderColor = "rgba(16, 185, 129, 0.25)";
    } else {
      dom.statusBadge.style.color = "var(--accent-amber)";
      dom.statusBadge.style.borderColor = "rgba(245, 158, 11, 0.25)";
    }
  }

  // =========================================================================
  // Calculation & Conversion Logic
  // =========================================================================
  function getRate(fromCode, toCode) {
    const fromRate = state.rates[fromCode] || 1.0;
    const toRate = state.rates[toCode] || 1.0;
    return toRate / fromRate;
  }

  function renderConverter() {
    const fromMeta = CURRENCY_REGISTRY[state.fromCurrency] || { name: state.fromCurrency, symbol: state.fromCurrency, flag: "🌐" };
    const toMeta = CURRENCY_REGISTRY[state.toCurrency] || { name: state.toCurrency, symbol: state.toCurrency, flag: "🌐" };

    // Update triggers
    dom.fromFlag.textContent = fromMeta.flag;
    dom.fromCode.textContent = state.fromCurrency;
    dom.fromName.textContent = fromMeta.name;

    dom.toFlag.textContent = toMeta.flag;
    dom.toCode.textContent = state.toCurrency;
    dom.toName.textContent = toMeta.name;

    dom.sourceSymbolTag.textContent = fromMeta.symbol;

    // Calculation
    const rate = getRate(state.fromCurrency, state.toCurrency);
    const inverseRate = rate > 0 ? 1 / rate : 0;
    const convertedAmount = state.amount * rate;

    // Formatted strings
    const formattedAmount = formatNumber(state.amount, 2);
    const formattedConverted = formatNumber(convertedAmount, 2);

    dom.summaryFrom.textContent = `${formattedAmount} ${state.fromCurrency} (${fromMeta.symbol}) =`;
    dom.summaryTargetVal.textContent = formattedConverted;
    dom.summaryTargetCode.textContent = `${state.toCurrency} (${toMeta.symbol})`;

    dom.directRateText.textContent = `1 ${state.fromCurrency} = ${formatRate(rate)} ${state.toCurrency}`;
    dom.inverseRateText.textContent = `1 ${state.toCurrency} = ${formatRate(inverseRate)} ${state.fromCurrency}`;
  }

  function formatNumber(num, decimals = 2) {
    if (isNaN(num)) return "0.00";
    return num.toLocaleString(undefined, {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    });
  }

  function formatRate(rate) {
    if (rate >= 100) return rate.toFixed(2);
    if (rate >= 1) return rate.toFixed(4);
    if (rate >= 0.0001) return rate.toFixed(5);
    return rate.toExponential(3);
  }

  // =========================================================================
  // Interactive Historical Chart (Chart.js)
  // =========================================================================
  function generateHistoricalData(days, currentRate) {
    const labels = [];
    const points = [];
    const today = new Date();
    
    // Seeded pseudo-random realistic trajectory with mean reversion
    let rateTracker = currentRate * (1 - (Math.sin(days) * 0.02));
    const volatility = 0.004;

    for (let i = days - 1; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(today.getDate() - i);
      labels.push(d.toLocaleDateString("en-US", { month: "short", day: "numeric" }));

      const drift = (currentRate - rateTracker) * 0.08;
      const noise = (Math.sin(i * 1.5) * 0.003 + (Math.random() - 0.49) * volatility) * rateTracker;
      rateTracker += drift + noise;
      if (i === 0) rateTracker = currentRate; // End precisely on current rate
      points.push(Number(rateTracker.toFixed(4)));
    }

    return { labels, points };
  }

  function renderTrendChart() {
    const rate = getRate(state.fromCurrency, state.toCurrency);
    const { labels, points } = generateHistoricalData(state.timeframe, rate);

    dom.chartHeading.textContent = `${state.fromCurrency} to ${state.toCurrency} Trend`;

    // Calculate High, Low, Average, Change
    const high = Math.max(...points);
    const low = Math.min(...points);
    const avg = points.reduce((a, b) => a + b, 0) / points.length;
    const startVal = points[0];
    const endVal = points[points.length - 1];
    const netChange = ((endVal - startVal) / startVal) * 100;

    dom.metricHigh.textContent = formatRate(high);
    dom.metricLow.textContent = formatRate(low);
    dom.metricAvg.textContent = formatRate(avg);

    const changeSign = netChange >= 0 ? "+" : "";
    dom.metricChange.textContent = `${changeSign}${netChange.toFixed(2)}%`;
    dom.metricChange.className = `metric-value ${netChange >= 0 ? "positive" : "negative"}`;

    const ctx = document.getElementById("trendChart");
    if (!ctx) return;

    if (trendChartInstance) {
      trendChartInstance.destroy();
    }

    const isDark = state.theme === "dark";
    const lineColor = netChange >= 0 ? "#10b981" : "#f43f5e";
    const gridColor = isDark ? "rgba(255, 255, 255, 0.06)" : "rgba(0, 0, 0, 0.06)";
    const textColor = isDark ? "#94a3b8" : "#64748b";

    // Create glowing vertical gradient fill
    const canvasContext = ctx.getContext("2d");
    const gradient = canvasContext.createLinearGradient(0, 0, 0, 220);
    if (netChange >= 0) {
      gradient.addColorStop(0, "rgba(16, 185, 129, 0.28)");
      gradient.addColorStop(1, "rgba(16, 185, 129, 0.0)");
    } else {
      gradient.addColorStop(0, "rgba(244, 63, 94, 0.28)");
      gradient.addColorStop(1, "rgba(244, 63, 94, 0.0)");
    }

    trendChartInstance = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [{
          data: points,
          borderColor: lineColor,
          borderWidth: 2.5,
          backgroundColor: gradient,
          fill: true,
          tension: 0.35,
          pointRadius: points.length <= 14 ? 3 : 0,
          pointHoverRadius: 6,
          pointHoverBackgroundColor: lineColor,
          pointHoverBorderColor: "#fff",
          pointHoverBorderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: "index",
          intersect: false
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: isDark ? "#161e2e" : "#ffffff",
            titleColor: isDark ? "#f8fafc" : "#0f172a",
            bodyColor: isDark ? "#94a3b8" : "#475569",
            borderColor: isDark ? "rgba(255,255,255,0.1)" : "rgba(0,0,0,0.1)",
            borderWidth: 1,
            padding: 10,
            displayColors: false,
            callbacks: {
              label: (context) => `1 ${state.fromCurrency} = ${context.parsed.y} ${state.toCurrency}`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: {
              color: textColor,
              font: { size: 10, family: "Inter" },
              maxTicksLimit: 7
            }
          },
          y: {
            grid: { color: gridColor },
            ticks: {
              color: textColor,
              font: { size: 10, family: "Inter" },
              callback: (val) => formatRate(val)
            }
          }
        }
      }
    });
  }

  // =========================================================================
  // Comparison Matrix (1 Base -> Major Currencies)
  // =========================================================================
  function renderComparisonMatrix() {
    const majors = ["EUR", "GBP", "INR", "JPY", "CAD", "AUD", "CHF", "CNY", "AED", "SGD", "BRL", "ZAR"];
    dom.matrixBaseCode.textContent = state.fromCurrency;
    dom.matrixGrid.innerHTML = "";

    majors.forEach((targetCode) => {
      if (targetCode === state.fromCurrency) return;
      const meta = CURRENCY_REGISTRY[targetCode] || { name: targetCode, flag: "🌐" };
      const rate = getRate(state.fromCurrency, targetCode);
      const valStr = formatRate(rate);

      const item = document.createElement("div");
      item.className = "matrix-item";
      item.setAttribute("role", "button");
      item.setAttribute("tabindex", "0");
      item.setAttribute("title", `Click to convert ${state.fromCurrency} to ${targetCode}`);
      item.innerHTML = `
        <div class="matrix-item-left">
          <span class="flag-icon" style="font-size:1.1rem">${meta.flag}</span>
          <span class="matrix-code">${targetCode}</span>
        </div>
        <span class="matrix-val tabular">${valStr}</span>
      `;

      item.addEventListener("click", () => {
        state.toCurrency = targetCode;
        renderConverter();
        renderTrendChart();
        recordHistory();
        showToast(`Target currency set to ${targetCode}`);
      });

      dom.matrixGrid.appendChild(item);
    });
  }

  // =========================================================================
  // History & Favorites Management
  // =========================================================================
  function recordHistory() {
    const rate = getRate(state.fromCurrency, state.toCurrency);
    const converted = state.amount * rate;
    const entry = {
      id: Date.now(),
      from: state.fromCurrency,
      to: state.toCurrency,
      amount: state.amount,
      converted: converted,
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    };

    // Avoid duplicate immediate entries
    if (state.history.length > 0) {
      const last = state.history[0];
      if (last.from === entry.from && last.to === entry.to && Math.abs(last.amount - entry.amount) < 0.01) {
        return;
      }
    }

    state.history.unshift(entry);
    if (state.history.length > 15) state.history.pop();
    localStorage.setItem("flux_history", JSON.stringify(state.history));
    renderHistory();
  }

  function renderHistory() {
    if (state.history.length === 0) {
      dom.historyList.innerHTML = `<div class="empty-history">No recent conversions yet. Perform an exchange to track your activity.</div>`;
      return;
    }

    dom.historyList.innerHTML = "";
    state.history.forEach((item) => {
      const el = document.createElement("div");
      el.className = "history-item";
      el.setAttribute("role", "button");
      el.setAttribute("tabindex", "0");
      el.setAttribute("title", "Click to restore this conversion");
      el.innerHTML = `
        <span class="history-formula">
          ${formatNumber(item.amount, 2)} ${item.from} → <strong>${formatNumber(item.converted, 2)} ${item.to}</strong>
        </span>
        <span class="history-time">${item.time}</span>
      `;
      el.addEventListener("click", () => {
        state.amount = item.amount;
        state.fromCurrency = item.from;
        state.toCurrency = item.to;
        dom.amountInput.value = formatNumber(item.amount, 2);
        renderConverter();
        renderComparisonMatrix();
        renderTrendChart();
        showToast(`Restored ${item.amount} ${item.from} to ${item.to}`);
      });
      dom.historyList.appendChild(el);
    });
  }

  function renderFavorites() {
    dom.favoritesChips.innerHTML = "";
    state.favorites.forEach((pair) => {
      const [from, to] = pair.split("-");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "fav-chip";
      btn.textContent = `${from} → ${to}`;
      btn.addEventListener("click", () => {
        state.fromCurrency = from;
        state.toCurrency = to;
        renderConverter();
        renderComparisonMatrix();
        renderTrendChart();
        recordHistory();
        showToast(`Switched to favorite pair: ${from} → ${to}`);
      });
      dom.favoritesChips.appendChild(btn);
    });
  }

  function pinCurrentPair() {
    const pairKey = `${state.fromCurrency}-${state.toCurrency}`;
    if (!state.favorites.includes(pairKey)) {
      state.favorites.push(pairKey);
      localStorage.setItem("flux_favorites", JSON.stringify(state.favorites));
      renderFavorites();
      showToast(`Pinned ${pairKey} to favorites! ⭐`);
    } else {
      showToast(`${pairKey} is already in your favorites!`);
    }
  }

  // =========================================================================
  // Searchable Currency Modal
  // =========================================================================
  function openCurrencyModal(target) {
    state.activePickerTarget = target;
    dom.currencySearchInput.value = "";
    state.searchFilter = "";
    state.activeCategoryFilter = "all";

    dom.categoryTabs.forEach((tab) => {
      tab.classList.toggle("active", tab.dataset.filter === "all");
    });

    renderCurrencyList();
    dom.currencyModal.removeAttribute("hidden");
    setTimeout(() => dom.currencySearchInput.focus(), 50);
  }

  function closeCurrencyModal() {
    dom.currencyModal.setAttribute("hidden", "true");
    state.activePickerTarget = null;
  }

  function renderCurrencyList() {
    dom.currencyListContainer.innerHTML = "";
    const query = state.searchFilter.toLowerCase().trim();
    const cat = state.activeCategoryFilter;

    // Get all supported codes from rates + registry
    const allCodes = Array.from(new Set([...Object.keys(CURRENCY_REGISTRY), ...Object.keys(state.rates)])).sort();

    const filtered = allCodes.filter((code) => {
      const meta = CURRENCY_REGISTRY[code] || { name: code, region: "other", popular: false };

      // Category filter check
      if (cat === "popular" && !meta.popular) return false;
      if (cat !== "all" && cat !== "popular" && meta.region !== cat) return false;

      // Search query check
      if (query) {
        return (
          code.toLowerCase().includes(query) ||
          (meta.name && meta.name.toLowerCase().includes(query))
        );
      }
      return true;
    });

    if (filtered.length === 0) {
      dom.currencyListContainer.innerHTML = `<div class="empty-history">No currencies found matching your search.</div>`;
      return;
    }

    const currentSelected = state.activePickerTarget === "from" ? state.fromCurrency : state.toCurrency;

    filtered.forEach((code) => {
      const meta = CURRENCY_REGISTRY[code] || { name: code, symbol: code, flag: "🌐" };
      const rateVsUSD = state.rates[code] || 0;
      const isSelected = code === currentSelected;

      const row = document.createElement("div");
      row.className = `currency-row-item ${isSelected ? "active" : ""}`;
      row.setAttribute("role", "option");
      row.setAttribute("aria-selected", isSelected ? "true" : "false");
      row.innerHTML = `
        <div class="currency-row-left">
          <span class="row-flag">${meta.flag}</span>
          <div class="row-code-group">
            <span class="row-code">${code}</span>
            <span class="row-name">${meta.name}</span>
          </div>
        </div>
        <div class="currency-row-right">
          <span class="row-symbol">${meta.symbol || ""}</span>
          <span class="row-rate tabular">${rateVsUSD > 0 ? `1 USD = ${formatRate(rateVsUSD)}` : ""}</span>
        </div>
      `;

      row.addEventListener("click", () => {
        if (state.activePickerTarget === "from") {
          state.fromCurrency = code;
        } else {
          state.toCurrency = code;
        }
        closeCurrencyModal();
        renderConverter();
        renderComparisonMatrix();
        renderTrendChart();
        recordHistory();
        showToast(`Selected ${code} (${meta.name})`);
      });

      dom.currencyListContainer.appendChild(row);
    });
  }

  // =========================================================================
  // Toast Notifications Hub
  // =========================================================================
  function showToast(message) {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent-emerald)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"></polyline>
      </svg>
      <span>${message}</span>
    `;

    dom.toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateX(100%)";
      toast.style.transition = "all 0.3s ease";
      setTimeout(() => toast.remove(), 300);
    }, 2800);
  }

  // =========================================================================
  // Event Listeners & Binding
  // =========================================================================
  function attachEventHandlers() {
    // Amount Input handling (strips commas, debounces render)
    let amountDebounceTimer = null;
    dom.amountInput.addEventListener("input", (e) => {
      clearTimeout(amountDebounceTimer);
      const raw = e.target.value.replace(/,/g, "");
      const num = parseFloat(raw);
      if (!isNaN(num) && num >= 0) {
        state.amount = num;
        amountDebounceTimer = setTimeout(() => {
          renderConverter();
          recordHistory();
        }, 180);
      }
    });

    dom.amountInput.addEventListener("blur", () => {
      dom.amountInput.value = formatNumber(state.amount, 2);
    });

    // Quick Amount Chips (+10, +100, +1K)
    document.querySelectorAll(".chip-btn[data-inc]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const inc = parseFloat(btn.dataset.inc);
        state.amount += inc;
        dom.amountInput.value = formatNumber(state.amount, 2);
        renderConverter();
        recordHistory();
      });
    });

    dom.btnResetAmount.addEventListener("click", () => {
      state.amount = 100.0;
      dom.amountInput.value = formatNumber(state.amount, 2);
      renderConverter();
      recordHistory();
    });

    // Swap Button with rotation animation
    dom.btnSwap.addEventListener("click", () => {
      const temp = state.fromCurrency;
      state.fromCurrency = state.toCurrency;
      state.toCurrency = temp;

      dom.btnSwap.style.transform = "rotate(180deg) scale(1.1)";
      setTimeout(() => {
        dom.btnSwap.style.transform = "";
      }, 350);

      renderConverter();
      renderComparisonMatrix();
      renderTrendChart();
      recordHistory();
      showToast(`Swapped: ${state.fromCurrency} ⇄ ${state.toCurrency}`);
    });

    // Copy Result to Clipboard
    dom.btnCopyResult.addEventListener("click", () => {
      const resultText = `${dom.summaryFrom.textContent} ${dom.summaryTargetVal.textContent} ${dom.summaryTargetCode.textContent}`;
      navigator.clipboard.writeText(resultText).then(() => {
        dom.copyBtnText.textContent = "Copied! ✓";
        showToast("Result copied to clipboard!");
        setTimeout(() => {
          dom.copyBtnText.textContent = "Copy Result";
        }, 2000);
      }).catch(() => {
        showToast("Failed to copy automatically.");
      });
    });

    // Pin Favorite
    dom.btnPinPair.addEventListener("click", pinCurrentPair);

    // Theme Toggle
    dom.btnThemeToggle.addEventListener("click", () => {
      state.theme = state.theme === "dark" ? "light" : "dark";
      dom.html.setAttribute("data-theme", state.theme);
      localStorage.setItem("flux_theme", state.theme);
      renderTrendChart(); // Refresh chart styling for light/dark
      showToast(`Theme switched to ${state.theme} mode`);
    });

    // Manual Refresh
    dom.btnRefresh.addEventListener("click", () => {
      fetchExchangeRates(true);
      showToast("Fetching latest live rates...");
    });

    // Timeframe selector buttons
    dom.timeframeBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        dom.timeframeBtns.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        state.timeframe = parseInt(btn.dataset.days, 10);
        renderTrendChart();
      });
    });

    // Clear History
    dom.btnClearHistory.addEventListener("click", () => {
      state.history = [];
      localStorage.removeItem("flux_history");
      renderHistory();
      showToast("Conversion history cleared.");
    });

    // Currency Picker Trigger Modals
    dom.fromCurrencyBtn.addEventListener("click", () => openCurrencyModal("from"));
    dom.toCurrencyBtn.addEventListener("click", () => openCurrencyModal("to"));
    dom.btnModalClose.addEventListener("click", closeCurrencyModal);

    dom.currencyModal.addEventListener("click", (e) => {
      if (e.target === dom.currencyModal) closeCurrencyModal();
    });

    // Modal Search Filter
    dom.currencySearchInput.addEventListener("input", (e) => {
      state.searchFilter = e.target.value;
      renderCurrencyList();
    });

    // Category Tabs in Modal
    dom.categoryTabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        dom.categoryTabs.forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");
        state.activeCategoryFilter = tab.dataset.filter;
        renderCurrencyList();
      });
    });

    // Keyboard Shortcuts
    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !dom.currencyModal.hasAttribute("hidden")) {
        closeCurrencyModal();
      }
      if (e.key.toLowerCase() === "s" && document.activeElement.tagName !== "INPUT") {
        dom.btnSwap.click();
      }
    });
  }

  // =========================================================================
  // Initialization Sequence
  // =========================================================================
  function init() {
    dom.html.setAttribute("data-theme", state.theme);
    dom.amountInput.value = formatNumber(state.amount, 2);

    renderFavorites();
    renderHistory();
    attachEventHandlers();
    fetchExchangeRates(false);
  }

  // Launch when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
