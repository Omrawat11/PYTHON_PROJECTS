"""
Currency Converter
Converts amounts between global currencies using live exchange rates,
automatic fallbacks, offline caching, and an interactive CLI.
"""

import argparse
import difflib
import html
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import requests
except ImportError:
    requests = None

# Ensure Windows console uses UTF-8 without crashing on special currency symbols
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Enable ANSI colors on Windows terminals
if os.name == "nt":
    os.system("")

# ANSI styling constants
class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    BG_BLUE = "\033[44m"
    WHITE = "\033[97m"

def color(text: str, *styles: str) -> str:
    """Format text with ANSI style codes if terminal supports it."""
    if not sys.stdout.isatty():
        return text
    return f"{''.join(styles)}{text}{Style.RESET}"


CACHE_FILENAME = "rates_cache.json"
CACHE_DURATION_HOURS = 12

# Common currency symbols
CURRENCY_SYMBOLS: Dict[str, str] = {
    "USD": "$", "EUR": "€", "GBP": "£", "INR": "₹", "JPY": "¥",
    "CNY": "¥", "AUD": "A$", "CAD": "C$", "CHF": "CHF", "HKD": "HK$",
    "NZD": "NZ$", "SGD": "S$", "KRW": "₩", "RUB": "₽", "BRL": "R$",
    "ZAR": "R", "TRY": "₺", "MXN": "Mex$", "THB": "฿", "IDR": "Rp",
    "PHP": "₱", "MYR": "RM", "VND": "₫", "ILS": "₪", "PLN": "zł",
    "SEK": "kr", "NOK": "kr", "DKK": "kr", "AED": "AED", "SAR": "SAR",
    "KWD": "KD", "QAR": "QR", "OMR": "RO", "EGP": "E£", "NGN": "₦",
    "PKR": "Rs", "BDT": "৳", "LKR": "Rs", "NPR": "Rs", "BHD": "BD",
    "HUF": "Ft", "CZK": "Kč", "CLP": "CLP$", "COP": "COL$", "PEN": "S/."
}

# Embedded baseline rates (USD base) to ensure it works even completely offline
FALLBACK_RATES: Dict[str, float] = {
    "USD": 1.0, "EUR": 0.88, "GBP": 0.76, "INR": 96.02, "JPY": 158.69,
    "AUD": 1.43, "CAD": 1.41, "CHF": 0.83, "CNY": 6.72, "HKD": 7.84,
    "NZD": 1.77, "SGD": 1.28, "KRW": 1368.60, "BRL": 5.18, "MXN": 17.67,
    "AED": 3.67, "SAR": 3.75, "ZAR": 16.43, "TRY": 48.89, "RUB": 84.49,
    "THB": 33.45, "IDR": 17907.21, "MYR": 4.08, "PHP": 62.81, "VND": 25950.54,
    "PKR": 277.39, "BDT": 122.90, "KWD": 0.31, "QAR": 3.64, "EGP": 51.70,
    "NGN": 1327.93, "SEK": 9.92, "NOK": 9.50, "DKK": 6.57, "PLN": 3.85,
    "ILS": 3.05, "HUF": 321.48, "CZK": 21.45, "CLP": 962.56, "COP": 3264.54,
    "ARS": 1518.74, "PEN": 3.40, "KZT": 442.66, "OMR": 0.38, "BHD": 0.38
}

# Comprehensive currency metadata (Code -> Name, Countries)
RAW_CURRENCIES: List[str] = [
    "AED : Emirati Dirham,United Arab Emirates Dirham",
    "AFN : Afghan Afghani,Afghanistan Afghani",
    "ALL : Albanian Lek,Albania Lek",
    "AMD : Armenian Dram,Armenia Dram",
    "ANG : Dutch Guilder,Netherlands Antilles Guilder,Bonaire,Curaçao,Saba,Sint Eustatius,Sint Maarten",
    "AOA : Angolan Kwanza,Angola Kwanza",
    "ARS : Argentine Peso,Argentina Peso,Islas Malvinas",
    "AUD : Australian Dollar,Australia Dollar,Christmas Island,Cocos Islands,Norfolk Island,Kiribati,Nauru",
    "AWG : Aruban Guilder,Aruba Guilder",
    "AZN : Azerbaijan Manat,Azerbaijan Manat",
    "BAM : Bosnian Convertible Mark,Bosnia and Herzegovina Convertible Mark",
    "BBD : Barbadian Dollar,Barbados Dollar",
    "BDT : Bangladeshi Taka,Bangladesh Taka",
    "BGN : Bulgarian Lev,Bulgaria Lev",
    "BHD : Bahraini Dinar,Bahrain Dinar",
    "BIF : Burundian Franc,Burundi Franc",
    "BMD : Bermudian Dollar,Bermuda Dollar",
    "BND : Bruneian Dollar,Brunei Darussalam Dollar",
    "BOB : Bolivian Boliviano,Bolivia Boliviano",
    "BRL : Brazilian Real,Brazil Real",
    "BSD : Bahamian Dollar,Bahamas Dollar",
    "BTC : Bitcoin,BTC, Cryptocurrency",
    "BTN : Bhutanese Ngultrum,Bhutan Ngultrum",
    "BWP : Botswana Pula,Botswana Pula",
    "BYN : Belarusian Ruble,Belarus Ruble",
    "BZD : Belizean Dollar,Belize Dollar",
    "CAD : Canadian Dollar,Canada Dollar",
    "CDF : Congolese Franc,Congo Franc",
    "CHF : Swiss Franc,Switzerland Franc,Liechtenstein",
    "CLF : Chilean Unit of Account",
    "CLP : Chilean Peso,Chile Peso",
    "CNY : Chinese Yuan,China Yuan Renminbi",
    "COP : Colombian Peso,Colombia Peso",
    "CRC : Costa Rican Colon,Costa Rica Colon",
    "CUC : Cuban Convertible Peso,Cuba Convertible Peso",
    "CUP : Cuban Peso,Cuba Peso",
    "CVE : Cape Verdean Escudo,Cape Verde Escudo",
    "CZK : Czech Koruna,Czech Republic Koruna",
    "DJF : Djiboutian Franc,Djibouti Franc",
    "DKK : Danish Krone,Denmark Krone,Faroe Islands,Greenland",
    "DOP : Dominican Peso,Dominican Republic Peso",
    "DZD : Algerian Dinar,Algeria Dinar",
    "EGP : Egyptian Pound,Egypt Pound,Gaza Strip",
    "ERN : Eritrean Nakfa,Eritrea Nakfa",
    "ETB : Ethiopian Birr,Ethiopia Birr",
    "EUR : Euro,European Union,France,Germany,Italy,Spain,Netherlands,Austria,Belgium,Portugal,Greece",
    "FJD : Fijian Dollar,Fiji Dollar",
    "FKP : Falkland Island Pound,Falkland Islands Pound",
    "GBP : British Pound,United Kingdom Pound,England,Northern Ireland,Scotland,Wales",
    "GEL : Georgian Lari,Georgia Lari",
    "GGP : Guernsey Pound,Guernsey Pound",
    "GHS : Ghanaian Cedi,Ghana Cedi",
    "GIP : Gibraltar Pound,Gibraltar Pound",
    "GMD : Gambian Dalasi,Gambia Dalasi",
    "GNF : Guinean Franc,Guinea Franc",
    "GTQ : Guatemalan Quetzal,Guatemala Quetzal",
    "GYD : Guyanese Dollar,Guyana Dollar",
    "HKD : Hong Kong Dollar,Hong Kong Dollar",
    "HNL : Honduran Lempira,Honduras Lempira",
    "HRK : Croatian Kuna,Croatia Kuna",
    "HTG : Haitian Gourde,Haiti Gourde",
    "HUF : Hungarian Forint,Hungary Forint",
    "IDR : Indonesian Rupiah,Indonesia Rupiah",
    "ILS : Israeli Shekel,Israel Shekel,Palestinian Territories",
    "IMP : Isle of Man Pound,Isle of Man Pound",
    "INR : Indian Rupee,India Rupee,Bhutan,Nepal",
    "IQD : Iraqi Dinar,Iraq Dinar",
    "IRR : Iranian Rial,Iran Rial",
    "ISK : Icelandic Krona,Iceland Krona",
    "JEP : Jersey Pound,Jersey Pound",
    "JMD : Jamaican Dollar,Jamaica Dollar",
    "JOD : Jordanian Dinar,Jordan Dinar",
    "JPY : Japanese Yen,Japan Yen",
    "KES : Kenyan Shilling,Kenya Shilling",
    "KGS : Kyrgyzstani Som,Kyrgyzstan Som",
    "KHR : Cambodian Riel,Cambodia Riel",
    "KMF : Comorian Franc,Comoros Franc",
    "KRW : South Korean Won,Korea Won",
    "KWD : Kuwaiti Dinar,Kuwait Dinar",
    "KYD : Caymanian Dollar,Cayman Islands Dollar",
    "KZT : Kazakhstani Tenge,Kazakhstan Tenge",
    "LAK : Lao Kip,Laos Kip",
    "LBP : Lebanese Pound,Lebanon Pound",
    "LKR : Sri Lankan Rupee,Sri Lanka Rupee",
    "LRD : Liberian Dollar,Liberia Dollar",
    "LSL : Basotho Loti,Lesotho Loti",
    "LYD : Libyan Dinar,Libya Dinar",
    "MAD : Moroccan Dirham,Morocco Dirham",
    "MDL : Moldovan Leu,Moldova Leu",
    "MGA : Malagasy Ariary,Madagascar Ariary",
    "MKD : Macedonian Denar,Macedonia Denar",
    "MMK : Burmese Kyat,Myanmar Kyat",
    "MNT : Mongolian Tughrik,Mongolia Tughrik",
    "MOP : Macau Pataca,Macau Pataca",
    "MRU : Mauritanian Ouguiya,Mauritania Ouguiya",
    "MUR : Mauritian Rupee,Mauritius Rupee",
    "MVR : Maldivian Rufiyaa,Maldives Rufiyaa",
    "MWK : Malawian Kwacha,Malawi Kwacha",
    "MXN : Mexican Peso,Mexico Peso",
    "MYR : Malaysian Ringgit,Malaysia Ringgit",
    "MZN : Mozambican Metical,Mozambique Metical",
    "NAD : Namibian Dollar,Namibia Dollar",
    "NGN : Nigerian Naira,Nigeria Naira",
    "NIO : Nicaraguan Cordoba,Nicaragua Cordoba",
    "NOK : Norwegian Krone,Norway Krone",
    "NPR : Nepalese Rupee,Nepal Rupee",
    "NZD : New Zealand Dollar,New Zealand Dollar,Cook Islands",
    "OMR : Omani Rial,Oman Rial",
    "PAB : Panamanian Balboa,Panama Balboa",
    "PEN : Peruvian Sol,Peru Sol",
    "PGK : Papua New Guinean Kina,Papua New Guinea Kina",
    "PHP : Philippine Peso,Philippines Peso",
    "PKR : Pakistani Rupee,Pakistan Rupee",
    "PLN : Polish Zloty,Poland Zloty",
    "PYG : Paraguayan Guarani,Paraguay Guarani",
    "QAR : Qatari Riyal,Qatar Riyal",
    "RON : Romanian Leu,Romania Leu",
    "RSD : Serbian Dinar,Serbia Dinar",
    "RUB : Russian Ruble,Russia Ruble",
    "RWF : Rwandan Franc,Rwanda Franc",
    "SAR : Saudi Arabian Riyal,Saudi Arabia Riyal",
    "SBD : Solomon Islander Dollar,Solomon Islands Dollar",
    "SCR : Seychellois Rupee,Seychelles Rupee",
    "SDG : Sudanese Pound,Sudan Pound",
    "SEK : Swedish Krona,Sweden Krona",
    "SGD : Singapore Dollar,Singapore Dollar",
    "SHP : Saint Helenian Pound,Saint Helena Pound",
    "SLE : Sierra Leonean Leone,Sierra Leone Leone",
    "SOS : Somali Shilling,Somalia Shilling",
    "SRD : Surinamese Dollar,Suriname Dollar",
    "STN : Sao Tomean Dobra,São Tomé and Príncipe Dobra",
    "SYP : Syrian Pound,Syria Pound",
    "SZL : Swazi Lilangeni,Eswatini Lilangeni",
    "THB : Thai Baht,Thailand Baht",
    "TJS : Tajikistani Somoni,Tajikistan Somoni",
    "TMT : Turkmenistani Manat,Turkmenistan Manat",
    "TND : Tunisian Dinar,Tunisia Dinar",
    "TOP : Tongan Pa'anga,Tonga Pa'anga",
    "TRY : Turkish Lira,Turkey Lira",
    "TTD : Trinidadian Dollar,Trinidad and Tobago Dollar",
    "TWD : Taiwan New Dollar,Taiwan New Dollar",
    "TZS : Tanzanian Shilling,Tanzania Shilling",
    "UAH : Ukrainian Hryvnia,Ukraine Hryvnia",
    "UGX : Ugandan Shilling,Uganda Shilling",
    "USD : US Dollar,United States Dollar,America",
    "UYU : Uruguayan Peso,Uruguay Peso",
    "UZS : Uzbekistani Som,Uzbekistan Som",
    "VES : Venezuelan Bolivar,Venezuela Bolivar",
    "VND : Vietnamese Dong,Vietnam Dong",
    "VUV : Ni-Vanuatu Vatu,Vanuatu Vatu",
    "WST : Samoan Tala,Samoa Tala",
    "XAF : Central African CFA Franc,Cameroon,Chad,Congo,Gabon",
    "XCD : East Caribbean Dollar,Antigua,Dominica,Grenada,Saint Lucia",
    "XDR : IMF Special Drawing Rights",
    "XOF : West African CFA Franc,Benin,Ivory Coast,Senegal,Togo",
    "XPF : CFP Franc,French Polynesia,New Caledonia",
    "YER : Yemeni Rial,Yemen Rial",
    "ZAR : South African Rand,South Africa Rand",
    "ZMW : Zambian Kwacha,Zambia Kwacha",
    "ZWL : Zimbabwean Dollar,Zimbabwe Dollar",
]

# For backwards compatibility
currencies = RAW_CURRENCIES

def parse_currency_metadata() -> Dict[str, Dict[str, str]]:
    """Parse raw currency strings into a searchable dictionary."""
    data = {}
    for entry in RAW_CURRENCIES:
        if " : " in entry:
            code, details = entry.split(" : ", 1)
            code = code.strip().upper()
            details = html.unescape(details.strip())
            parts = [p.strip() for p in details.split(",") if p.strip()]
            name = parts[0] if parts else code
            countries = ", ".join(parts[1:]) if len(parts) > 1 else ""
            symbol = CURRENCY_SYMBOLS.get(code, "")
            data[code] = {
                "name": name,
                "countries": countries,
                "symbol": symbol,
                "raw": details,
            }
    return data

CURRENCY_INFO = parse_currency_metadata()


class CurrencyEngine:
    """Manages rate fetching, caching, and currency conversion logic."""

    def __init__(self, cache_path: Optional[Path] = None):
        if cache_path is None:
            self.cache_path = Path(__file__).resolve().parent / CACHE_FILENAME
        else:
            self.cache_path = cache_path
        self.rates: Dict[str, float] = {}
        self.last_updated: str = "Unknown"
        self.data_source: str = "Uninitialized"

    def _fetch_from_open_er(self) -> Optional[Dict[str, float]]:
        """Primary free provider (Open Exchange Rate API - USD base, no key required)."""
        if not requests:
            return None
        try:
            resp = requests.get("https://open.er-api.com/v6/latest/USD", timeout=6)
            if resp.status_code == 200:
                payload = resp.json()
                if payload.get("result") == "success" and "rates" in payload:
                    self.last_updated = payload.get("time_last_update_utc", datetime.now(timezone.utc).strftime("%c UTC"))
                    self.data_source = "Live API (open.er-api.com)"
                    return payload["rates"]
        except Exception:
            pass
        return None

    def _fetch_from_exchangerate_api(self) -> Optional[Dict[str, float]]:
        """Secondary free provider."""
        if not requests:
            return None
        try:
            resp = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=6)
            if resp.status_code == 200:
                payload = resp.json()
                if "rates" in payload:
                    self.last_updated = payload.get("date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
                    self.data_source = "Live API (exchangerate-api.com)"
                    return payload["rates"]
        except Exception:
            pass
        return None

    def _fetch_from_fixer(self, api_key: str) -> Optional[Dict[str, float]]:
        """Optional Fixer.io provider if user has a valid API key."""
        if not requests or not api_key:
            return None
        try:
            resp = requests.get(f"http://data.fixer.io/api/latest?access_key={api_key}", timeout=6)
            if resp.status_code == 200:
                payload = resp.json()
                if payload.get("success") and "rates" in payload:
                    # Fixer free tier uses EUR base, convert to USD base
                    rates = payload["rates"]
                    if "USD" in rates and rates["USD"] > 0:
                        usd_rate = rates["USD"]
                        rates_usd = {k: v / usd_rate for k, v in rates.items()}
                        self.last_updated = payload.get("date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
                        self.data_source = "Live API (fixer.io)"
                        return rates_usd
        except Exception:
            pass
        return None

    def _load_cache(self) -> Optional[Tuple[Dict[str, float], str]]:
        """Load cached rates from disk if fresh."""
        try:
            if self.cache_path.exists():
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)
                cached_time = cache_data.get("timestamp", 0)
                # Check age
                if time.time() - cached_time < CACHE_DURATION_HOURS * 3600:
                    return cache_data.get("rates", {}), cache_data.get("last_updated", "Cached")
        except Exception:
            pass
        return None

    def _save_cache(self, rates: Dict[str, float]) -> None:
        """Save rates to disk cache."""
        try:
            cache_payload = {
                "timestamp": time.time(),
                "last_updated": self.last_updated,
                "rates": rates
            }
            with open(self.cache_path, "w", encoding="utf-8") as f:
                json.dump(cache_payload, f, indent=2)
        except Exception:
            pass

    def load_rates(self, force_refresh: bool = False, fixer_key: Optional[str] = None) -> bool:
        """
        Load exchange rates with graceful multi-tier fallback:
        1. Cache (if not force_refresh)
        2. Fixer.io (if user supplied key)
        3. Open.er-api (free, zero-key)
        4. Exchangerate-api (backup free)
        5. Cache (even if older than 12h)
        6. Embedded fallback rates
        """
        if not force_refresh:
            cached = self._load_cache()
            if cached and cached[0]:
                self.rates, self.last_updated = cached
                self.data_source = "Local Cache (12h fresh)"
                return True

        # Try user-provided Fixer key if present
        key = fixer_key or os.getenv("FIXER_API_KEY")
        if key:
            rates = self._fetch_from_fixer(key)
            if rates:
                self.rates = rates
                self._save_cache(rates)
                return True

        # Try Primary Free API
        rates = self._fetch_from_open_er()
        if rates:
            self.rates = rates
            self._save_cache(rates)
            return True

        # Try Secondary Free API
        rates = self._fetch_from_exchangerate_api()
        if rates:
            self.rates = rates
            self._save_cache(rates)
            return True

        # Fallback to expired cache if available
        try:
            if self.cache_path.exists():
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)
                if "rates" in cache_data and cache_data["rates"]:
                    self.rates = cache_data["rates"]
                    self.last_updated = cache_data.get("last_updated", "Older Cache")
                    self.data_source = "Local Cache (offline mode)"
                    return True
        except Exception:
            pass

        # Final fallback: Embedded rates
        self.rates = FALLBACK_RATES.copy()
        self.last_updated = "Built-in Baseline"
        self.data_source = "Offline Baseline Data"
        return True

    def validate_currency(self, code: str) -> Tuple[bool, Optional[str]]:
        """Validate if currency code exists; if not, suggest closest match."""
        code_upper = code.upper()
        if code_upper in self.rates:
            return True, code_upper

        # Suggest closest match
        all_codes = list(self.rates.keys())
        matches = difflib.get_close_matches(code_upper, all_codes, n=1, cutoff=0.6)
        suggestion = matches[0] if matches else None
        return False, suggestion

    def convert(self, amount: float, from_curr: str, to_curr: str) -> Dict[str, object]:
        """Convert amount between two currencies."""
        from_code = from_curr.upper()
        to_code = to_curr.upper()

        if from_code not in self.rates:
            raise KeyError(f"Currency code '{from_code}' is not supported.")
        if to_code not in self.rates:
            raise KeyError(f"Currency code '{to_code}' is not supported.")

        from_rate = self.rates[from_code]
        to_rate = self.rates[to_code]

        # Since rates are against USD base:
        # 1 USD = from_rate [FROM] => 1 [FROM] = 1 / from_rate USD
        # 1 [FROM] = to_rate / from_rate [TO]
        exchange_rate = to_rate / from_rate
        converted_amount = amount * exchange_rate
        inverse_rate = 1 / exchange_rate if exchange_rate > 0 else 0.0

        from_meta = CURRENCY_INFO.get(from_code, {})
        to_meta = CURRENCY_INFO.get(to_code, {})

        return {
            "amount": amount,
            "from_code": from_code,
            "from_name": from_meta.get("name", from_code),
            "from_symbol": from_meta.get("symbol", ""),
            "from_countries": from_meta.get("countries", ""),
            "to_code": to_code,
            "to_name": to_meta.get("name", to_code),
            "to_symbol": to_meta.get("symbol", ""),
            "to_countries": to_meta.get("countries", ""),
            "converted_amount": converted_amount,
            "rate": exchange_rate,
            "inverse_rate": inverse_rate,
            "data_source": self.data_source,
            "last_updated": self.last_updated,
        }


def format_conversion_result(res: Dict[str, object]) -> str:
    """Format conversion result into an attractive, clear presentation."""
    amount_str = f"{res['amount']:,.2f}"
    converted_str = f"{res['converted_amount']:,.2f}"
    
    from_sym = f" ({res['from_symbol']})" if res['from_symbol'] else ""
    to_sym = f" ({res['to_symbol']})" if res['to_symbol'] else ""

    rate = res['rate']
    inv_rate = res['inverse_rate']
    rate_str = f"{rate:,.4f}" if rate >= 0.0001 else f"{rate:.6f}"
    inv_rate_str = f"{inv_rate:,.4f}" if inv_rate >= 0.0001 else f"{inv_rate:.6f}"

    lines = [
        color("=" * 62, Style.CYAN),
        f"  {color(amount_str, Style.BOLD, Style.GREEN)} {color(res['from_code'], Style.BOLD)}{from_sym}  =  "
        f"{color(converted_str, Style.BOLD, Style.YELLOW)} {color(res['to_code'], Style.BOLD)}{to_sym}",
        color("-" * 62, Style.DIM),
        f"  {color('Exchange Rate:', Style.BOLD)} 1 {res['from_code']} = {rate_str} {res['to_code']}",
        f"  {color('Inverse Rate :', Style.BOLD)} 1 {res['to_code']} = {inv_rate_str} {res['from_code']}",
        f"  {color('Currencies   :', Style.BOLD)} {res['from_name']} -> {res['to_name']}",
        f"  {color('Source & Date:', Style.DIM)} {res['data_source']} | {res['last_updated']}",
        color("=" * 62, Style.CYAN),
    ]
    return "\n".join(lines)


def display_banner(engine: CurrencyEngine) -> None:
    """Print the startup header banner."""
    border = "=" * 64
    banner = f"""
{color(border, Style.CYAN, Style.BOLD)}
{color("                   GLOBAL CURRENCY CONVERTER                    ", Style.CYAN, Style.BOLD)}
{color(border, Style.CYAN, Style.BOLD)}
  * Rates Source: {color(engine.data_source, Style.GREEN)}
  * Last Update : {color(engine.last_updated, Style.WHITE)}
  * Currencies  : {color(str(len(engine.rates)), Style.YELLOW)} supported
    """
    print(banner.strip())


def display_help() -> None:
    """Print usage instructions and command cheatsheet."""
    print(f"""
{color("Available Commands & Syntax:", Style.BOLD, Style.YELLOW)}
  {color("<amount> <from> <to>", Style.CYAN)}    Convert currency (e.g. {color("100 USD EUR", Style.GREEN)} or {color("50.5 inr usd", Style.GREEN)})
  {color("rate <from> <to>", Style.CYAN)}        Check unit rate (e.g. {color("rate EUR GBP", Style.GREEN)})
  {color("search <query>", Style.CYAN)}          Search by currency code, country, or name
  {color("popular", Style.CYAN)}                 View snapshot of top global currencies
  {color("list", Style.CYAN)} or {color("show", Style.CYAN)}            List all available currency codes
  {color("refresh", Style.CYAN)}                 Force fetch fresh live rates from API
  {color("help", Style.CYAN)}                    Show this help menu
  {color("quit", Style.CYAN)} or {color("q", Style.CYAN)}               Exit application
""")


def search_currencies(engine: CurrencyEngine, query: str) -> None:
    """Search currencies by keyword across code, name, and country list."""
    q = query.strip().lower()
    if not q:
        print(color("Please provide a search term. Example: search euro", Style.YELLOW))
        return

    matches = []
    for code, info in CURRENCY_INFO.items():
        if (q in code.lower() or 
            q in info["name"].lower() or 
            q in info["countries"].lower()):
            has_rate = code in engine.rates
            matches.append((code, info["name"], info["symbol"], info["countries"], has_rate))

    # Also search codes in engine rates that might not be in CURRENCY_INFO
    for code in engine.rates:
        if q in code.lower() and not any(m[0] == code for m in matches):
            matches.append((code, code, CURRENCY_SYMBOLS.get(code, ""), "", True))

    if not matches:
        print(color(f"No currencies found matching '{query}'.", Style.YELLOW))
        return

    print(f"\n{color(f'Found {len(matches)} matching currencies:', Style.BOLD, Style.GREEN)}")
    print(f"  {'CODE':<6} {'SYMBOL':<8} {'NAME':<28} {'COUNTRIES'}")
    print("  " + "-" * 75)
    for code, name, sym, countries, has_rate in matches[:25]:
        sym_str = sym if sym else "-"
        country_preview = (countries[:35] + "...") if len(countries) > 35 else countries
        rate_indicator = "" if has_rate else color(" (no live rate)", Style.DIM)
        code_colored = color(f"{code:<6}", Style.BOLD, Style.CYAN)
        print(f"  {code_colored} {sym_str:<8} {name:<28} {country_preview}{rate_indicator}")
    
    if len(matches) > 25:
        print(color(f"\n  ... and {len(matches) - 25} more. Refine your search query.", Style.DIM))
    print()


def show_popular_rates(engine: CurrencyEngine) -> None:
    """Display a matrix of popular exchange rates."""
    majors = ["USD", "EUR", "GBP", "INR", "JPY", "CAD", "AUD", "AED", "CHF", "CNY"]
    print(f"\n{color('Popular Exchange Rates Overview (Relative to USD):', Style.BOLD, Style.CYAN)}")
    print(f"  {'CODE':<6} {'NAME':<22} {'1 USD =':<14} {'1 UNIT IN USD'}")
    print("  " + "-" * 58)
    for code in majors:
        if code in engine.rates:
            rate = engine.rates[code]
            info = CURRENCY_INFO.get(code, {})
            name = info.get("name", code)
            inv = 1 / rate if rate > 0 else 0.0
            code_colored = color(f"{code:<6}", Style.BOLD)
            print(f"  {code_colored} {name:<22} {rate:>10,.4f}     ${inv:>8,.4f}")
    print()


def list_all_currencies(engine: CurrencyEngine) -> None:
    """Display all available currencies cleanly in columns."""
    all_codes = sorted(list(engine.rates.keys()))
    print(f"\n{color(f'All {len(all_codes)} Available Currency Codes:', Style.BOLD, Style.GREEN)}")
    
    # 4 columns display
    cols = 4
    for i in range(0, len(all_codes), cols):
        chunk = all_codes[i:i + cols]
        row_str = "   ".join(f"{color(f'{code:<4}', Style.BOLD, Style.CYAN)} {CURRENCY_INFO.get(code, {}).get('name', '')[:14]:<14}" for code in chunk)
        print(f"  {row_str}")
    print(color("\nTip: Use 'search <term>' to find country or currency details.\n", Style.DIM))


def parse_and_convert(engine: CurrencyEngine, query: str) -> None:
    """Parse user input string and perform currency conversion."""
    # Clean input
    tokens = query.strip().replace(",", "").split()
    
    # Remove filler words like 'to', 'in', 'convert'
    tokens = [t for t in tokens if t.lower() not in ("to", "in", "convert")]

    # Handle 'rate USD EUR' syntax
    if len(tokens) == 3 and tokens[0].lower() == "rate":
        qty = 1.0
        from_c = tokens[1]
        to_c = tokens[2]
    elif len(tokens) == 2:
        # e.g. 'USD EUR' -> assume 1 unit
        qty = 1.0
        from_c = tokens[0]
        to_c = tokens[1]
    elif len(tokens) >= 3:
        try:
            qty = float(tokens[0])
        except ValueError:
            print(color(f"Error: '{tokens[0]}' is not a valid number. Example: 100 USD EUR", Style.RED))
            return
        from_c = tokens[1]
        to_c = tokens[2]
    else:
        print(color("Invalid format. Please use: <amount> <from_currency> <to_currency>", Style.YELLOW))
        print(color("Example: 100 USD EUR   or   50 inr usd", Style.DIM))
        return

    if qty < 0:
        print(color("Error: Currency amount cannot be negative.", Style.RED))
        return

    # Validate currencies and give helpful typo suggestions
    valid_from, suggest_from = engine.validate_currency(from_c)
    if not valid_from:
        msg = f"Error: Unknown currency code '{from_c.upper()}'."
        if suggest_from:
            msg += f" Did you mean '{suggest_from}'?"
        print(color(msg, Style.RED))
        print(color("Tip: Type 'search <country/name>' or 'list' to see valid codes.", Style.DIM))
        return

    valid_to, suggest_to = engine.validate_currency(to_c)
    if not valid_to:
        msg = f"Error: Unknown currency code '{to_c.upper()}'."
        if suggest_to:
            msg += f" Did you mean '{suggest_to}'?"
        print(color(msg, Style.RED))
        print(color("Tip: Type 'search <country/name>' or 'list' to see valid codes.", Style.DIM))
        return

    # Execute conversion
    try:
        res = engine.convert(qty, from_c, to_c)
        print("\n" + format_conversion_result(res) + "\n")
    except Exception as e:
        print(color(f"Conversion error: {e}", Style.RED))


def interactive_loop(engine: CurrencyEngine) -> None:
    """Main interactive REPL loop."""
    display_banner(engine)
    display_help()

    while True:
        try:
            prompt_text = f"{color('Convert', Style.CYAN, Style.BOLD)} > "
            user_input = input(prompt_text).strip()
            
            if not user_input:
                continue

            cmd = user_input.lower()

            if cmd in ("q", "quit", "exit"):
                print(color("\nThank you for using Global Currency Converter. Goodbye! 👋\n", Style.GREEN))
                break
            elif cmd in ("help", "?"):
                display_help()
            elif cmd in ("list", "show"):
                list_all_currencies(engine)
            elif cmd == "popular":
                show_popular_rates(engine)
            elif cmd == "refresh":
                print(color("Refreshing exchange rates from API...", Style.YELLOW))
                engine.load_rates(force_refresh=True)
                print(color(f"Rates updated! Source: {engine.data_source}", Style.GREEN))
            elif cmd.startswith("search ") or cmd.startswith("find "):
                _, search_term = user_input.split(maxsplit=1)
                search_currencies(engine, search_term)
            else:
                parse_and_convert(engine, user_input)

        except (KeyboardInterrupt, EOFError):
            print(color("\n\nOperation cancelled. Exiting. 👋\n", Style.GREEN))
            break
        except Exception as err:
            print(color(f"Unexpected error: {err}. Please try again.", Style.RED))


def main() -> None:
    """CLI entry point supporting both arguments and interactive mode."""
    parser = argparse.ArgumentParser(
        description="Convert currency amounts using live exchange rates and robust fallbacks.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  curr.py 100 USD EUR
  curr.py 5000 INR USD
  curr.py --search rupee
  curr.py --popular
  curr.py --list
  curr.py               (starts interactive mode)
"""
    )
    parser.add_argument("amount", nargs="?", type=float, help="Amount of currency to convert")
    parser.add_argument("from_currency", nargs="?", type=str, help="Source currency code (e.g. USD)")
    parser.add_argument("to_currency", nargs="?", type=str, help="Target currency code (e.g. EUR)")
    parser.add_argument("--search", "-s", type=str, help="Search for currencies by name or country")
    parser.add_argument("--list", "-l", action="store_true", help="List all supported currency codes")
    parser.add_argument("--popular", "-p", action="store_true", help="Show overview of popular currency rates")
    parser.add_argument("--refresh", "-r", action="store_true", help="Force fresh download of exchange rates")
    parser.add_argument("--fixer-key", type=str, help="Optional Fixer.io API key")

    args = parser.parse_args()

    engine = CurrencyEngine()
    engine.load_rates(force_refresh=args.refresh, fixer_key=args.fixer_key)

    # CLI option flags
    if args.search:
        search_currencies(engine, args.search)
        return
    if args.list:
        list_all_currencies(engine)
        return
    if args.popular:
        show_popular_rates(engine)
        return

    # Direct conversion arguments passed
    if args.amount is not None and args.from_currency and args.to_currency:
        parse_and_convert(engine, f"{args.amount} {args.from_currency} {args.to_currency}")
        return

    # If partial arguments passed, warn and start interactive
    if args.amount is not None or args.from_currency or args.to_currency:
        print(color("Incomplete conversion arguments. Starting interactive mode...", Style.YELLOW))

    # Default to interactive mode
    interactive_loop(engine)



# =====================================================================
# Backwards Compatibility Interface
# =====================================================================
def function1():
    """Legacy entry point preserved from original curr.py."""
    engine = CurrencyEngine()
    engine.load_rates()
    interactive_loop(engine)


if __name__ == "__main__":
    main()
