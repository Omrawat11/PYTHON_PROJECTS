# 💱 FluxConvert — Modern Global Currency Converter & Web UI

A feature-rich, high-performance currency conversion suite featuring:
1. **Interactive Modern Web Application (`UIcurr.py`)**: Glassmorphism Neo-Fintech UI with interactive Chart.js historical charts, live market ticker, searchable currency modals with flags, dark/light mode, and offline resilience.
2. **Terminal CLI & REPL Tool (`curr.py`)**: Fast CLI utility with live multi-tier API fallbacks, caching, decimal conversions, and typo suggestions.

---

## ✨ Features

- **🎨 Modern Web UI**:
  - **Glassmorphic Neo-Fintech Theme**: Frosted glass cards, ambient gradient glows, and refined borders.
  - **Interactive Historical Chart**: Powered by Chart.js with timeframe switches (`7D`, `1M`, `3M`, `1Y`), period high/low/average stats, and gradient fills.
  - **Live Market Ticker**: Real-time ribbon with popular world currencies and change percentages.
  - **Global Comparison Matrix**: Live multi-currency conversion table across 12 major global currencies.
  - **Animated Quick Actions**: Interactive 360° swap button (`⇄`), quick increment chips (`+10`, `+100`, `+1K`), and clipboard copy.
  - **Searchable Currency Dialog**: Fast search across 165+ currencies with country flag emojis, ISO codes, and region filter tabs (Americas, Europe, Asia, Africa).
  - **Theme Switcher**: Smooth toggle between Dark Mode and Light Mode with persistent state.
  - **Favorites & History**: Pin preferred pairs and review conversion logs.

- **⚡ Robust Backend & Rate Engine**:
  - **Zero-Key Live Rates**: Fetches live rates directly from Open Exchange Rates API.
  - **Multi-Tier Fallbacks**:
    1. Local cache (12-hour validity window)
    2. Primary live API (`open.er-api.com`)
    3. Secondary live API (`api.exchangerate-api.com`)
    4. Optional Fixer.io support (`--fixer-key` or `FIXER_API_KEY`)
    5. Built-in offline baseline rates (guaranteed zero crashes)
  - **Universal Compatibility**: Uses Python standard library (`http.server`, `urllib`, `webbrowser`) so the Web UI launches with **zero external heavy server frameworks required**.

---

## 🚀 How to Run

### Option A: Launch Interactive Web Application (Recommended)

From the project root or inside `Currency_Convertor`:

```bash
# From workspace root:
python Currency_Convertor/UIcurr.py

# Or from inside Currency_Convertor directory:
cd Currency_Convertor
python UIcurr.py
```

*The application starts a local server and automatically opens `http://127.0.0.1:5000/` in your default web browser.*

---

### Option B: Terminal CLI & REPL Mode

```bash
# Interactive terminal shell
python Currency_Convertor/curr.py

# Instant single-line conversion
python Currency_Convertor/curr.py 100 USD EUR
python Currency_Convertor/curr.py 5000 INR USD

# Search currencies by name or country
python Currency_Convertor/curr.py --search rupee

# Overview of popular currencies
python Currency_Convertor/curr.py --popular

# List all available currencies
python Currency_Convertor/curr.py --list
```

---

## 📁 Project Structure

```text
Currency_Convertor/
├── UIcurr.py           # Web UI server launcher & REST API endpoints
├── curr.py             # Advanced CLI converter & rate engine
├── requirements.txt    # Python dependencies (requests)
├── README.md           # Documentation & usage guide
└── web/
    ├── index.html      # Responsive HTML5 SPA layout
    ├── style.css       # Vanilla CSS glassmorphism & neo-fintech styles
    └── app.js          # Reactive frontend client & Chart.js logic
```

---

## 📄 License
This project is open-source under the MIT License.
