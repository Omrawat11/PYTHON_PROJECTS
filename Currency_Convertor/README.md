# 💱 Global Currency Converter

A feature-rich, robust Python currency converter CLI that converts amounts between 165+ global currencies using live exchange rates, intelligent fallbacks, local caching, and an interactive shell.

---

## ✨ Features

- **Live Exchange Rates**: Fetches live rates without requiring any mandatory API key (powered by Open Exchange Rate API).
- **Multi-Tier Fallbacks**:
  1. High-speed local cache (12-hour validity)
  2. Primary live API (`open.er-api.com`)
  3. Secondary backup API (`api.exchangerate-api.com`)
  4. Optional Fixer.io support (via `FIXER_API_KEY` or `--fixer-key`)
  5. Built-in offline baseline rates (never crashes even if completely disconnected)
- **Flexible Modes**:
  - **Direct CLI Conversion**: e.g., `python curr.py 100 USD EUR`
  - **Interactive REPL Loop**: User-friendly shell with live commands.
- **Smart Currency Search**: Search by currency name, ISO code, or country (e.g. `search rupee`, `search japan`, `search euro`).
- **Typo Suggestions**: Automatically suggests correct currency codes if a typo is made (e.g., `USDD` -> `USD`).
- **Comprehensive Metadata**: Displays currency symbols (`$`, `€`, `£`, `₹`, `¥`), exchange rates, inverse rates, and last update timestamps.
- **Decimal & Comma Support**: Accepts formatted numbers like `1,250.50` or standard floats `99.95`.
- **Zero-Crash Design**: Full error handling for network timeouts, invalid inputs, and legacy Windows console encodings.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Direct CLI Conversion
```bash
# Convert 100 USD to INR
python curr.py 100 USD INR

# Convert 50 EUR to USD
python curr.py 50 EUR USD

# Search for a currency
python curr.py --search rupee

# View popular currencies snapshot
python curr.py --popular

# List all available currencies
python curr.py --list
```

### 3. Interactive Mode
Run without arguments to start the interactive shell:
```bash
python curr.py
```

Inside the interactive shell:
```text
Convert > 100 USD EUR
Convert > 5000 INR USD
Convert > search dollar
Convert > popular
Convert > list
Convert > refresh
Convert > help
Convert > q
```

---

## 🛠️ Command-Line Options

| Option | Shorthand | Description |
|---|---|---|
| `amount from to` | - | Perform immediate currency conversion |
| `--search <query>` | `-s` | Search currencies by keyword, name, or country |
| `--popular` | `-p` | Display exchange rate overview for major world currencies |
| `--list` | `-l` | List all 165+ supported currency codes |
| `--refresh` | `-r` | Force refresh rates from API and bypass local cache |
| `--fixer-key <key>` | - | Provide an optional Fixer.io API key |

---

## 📄 License
This project is open-source under the MIT License.
