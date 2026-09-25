"""
FluxConvert UI Server & Launcher
Launches a local, high-performance web server and opens the modern
interactive Currency Converter web application in the default browser.
"""

import http.server
import json
import os
import socket
import sys
import threading
import time
import urllib.parse
import webbrowser
from pathlib import Path
from typing import Optional, Tuple

# Enable ANSI colors on Windows
if os.name == "nt":
    os.system("")

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Import CurrencyEngine from curr.py in the same folder
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

try:
    from curr import CurrencyEngine, CURRENCY_INFO, Style, color
except ImportError:
    # Standalone fallback if curr.py is modified or missing
    class Style:
        RESET = "\033[0m"
        BOLD = "\033[1m"
        CYAN = "\033[96m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        WHITE = "\033[97m"
    def color(text, *styles):
        return f"{''.join(styles)}{text}{Style.RESET}"
    CurrencyEngine = None
    CURRENCY_INFO = {}

WEB_DIR = BASE_DIR / "web"


def find_available_port(start_port: int = 5000, max_attempts: int = 50) -> int:
    """Find an available TCP port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start_port


class CurrencyWebHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler serving static SPA assets and currency REST APIs."""

    engine: Optional[object] = None

    def log_message(self, format, *args):
        """Custom clean HTTP access log."""
        status = args[1] if len(args) > 1 else ""
        if status.startswith("2"):
            # Suppress noisy 200 logs for static assets
            return
        sys.stdout.write(f"  [HTTP] {args[0]} -> {status}\n")

    def send_cors_headers(self):
        """Send common CORS and caching headers."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # -------------------------------------------------------------
        # REST API Endpoints
        # -------------------------------------------------------------
        if path == "/api/rates":
            force_refresh = "refresh" in query and query["refresh"][0].lower() in ("true", "1")
            if self.engine:
                if force_refresh:
                    self.engine.load_rates(force_refresh=True)
                payload = {
                    "status": "success",
                    "rates": self.engine.rates,
                    "last_updated": self.engine.last_updated,
                    "source": self.engine.data_source,
                    "currencies_count": len(self.engine.rates),
                }
            else:
                payload = {"status": "error", "message": "Engine not initialized"}
            
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/api/convert":
            try:
                amount = float(query.get("amount", [1.0])[0])
                from_curr = query.get("from", ["USD"])[0].upper()
                to_curr = query.get("to", ["EUR"])[0].upper()

                if self.engine:
                    res = self.engine.convert(amount, from_curr, to_curr)
                    body = json.dumps({"status": "success", "result": res}).encode("utf-8")
                    self.send_response(200)
                else:
                    body = json.dumps({"status": "error", "message": "Engine unavailable"}).encode("utf-8")
                    self.send_response(500)
            except Exception as e:
                body = json.dumps({"status": "error", "message": str(e)}).encode("utf-8")
                self.send_response(400)

            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/api/health":
            body = json.dumps({"status": "ok", "app": "FluxConvert"}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
            return

        # -------------------------------------------------------------
        # Static Asset Serving
        # -------------------------------------------------------------
        file_map = {
            "/": ("index.html", "text/html; charset=utf-8"),
            "/index.html": ("index.html", "text/html; charset=utf-8"),
            "/style.css": ("style.css", "text/css; charset=utf-8"),
            "/app.js": ("app.js", "application/javascript; charset=utf-8"),
        }

        if path in file_map:
            filename, content_type = file_map[path]
            file_path = WEB_DIR / filename

            if file_path.exists():
                try:
                    with open(file_path, "rb") as f:
                        data = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", content_type)
                    self.send_header("Content-Length", str(len(data)))
                    self.send_header("Cache-Control", "no-cache")
                    self.end_headers()
                    self.wfile.write(data)
                    return
                except Exception as e:
                    self.send_error(500, f"Error reading asset: {e}")
                    return

        # 404 for unknown paths
        self.send_error(404, "Page Not Found")


def launch_server(port: int = 5000, auto_open: bool = True) -> None:
    """Initialize currency engine and start local web server."""
    actual_port = find_available_port(port)
    url = f"http://127.0.0.1:{actual_port}"

    # Initialize Engine
    engine = None
    if CurrencyEngine:
        engine = CurrencyEngine()
        engine.load_rates()

    CurrencyWebHandler.engine = engine

    server = http.server.ThreadingHTTPServer(("127.0.0.1", actual_port), CurrencyWebHandler)

    border = "=" * 66
    print(f"""
{color(border, Style.CYAN, Style.BOLD)}
{color("         FLUXCONVERT — GLOBAL CURRENCY CONVERTER WEB UI         ", Style.CYAN, Style.BOLD)}
{color(border, Style.CYAN, Style.BOLD)}
  * {color("Local Application URL", Style.BOLD)} : {color(url, Style.GREEN, Style.BOLD)}
  * {color("Live Exchange Rates", Style.BOLD)}   : {color(engine.data_source if engine else "Ready", Style.WHITE)}
  * {color("Currencies Loaded", Style.BOLD)}     : {color(str(len(engine.rates)) if engine else "160+", Style.YELLOW)}
  * {color("Browser Action", Style.BOLD)}        : Opening automatically in default browser...

  {color("Press Ctrl+C in this terminal window to stop the server.", Style.WHITE)}
{color(border, Style.CYAN, Style.BOLD)}
""")

    if auto_open:
        def open_browser():
            time.sleep(0.6)
            try:
                webbrowser.open(url)
            except Exception:
                pass
        threading.Thread(target=open_browser, daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{color('Server shutting down gracefully. Goodbye!', Style.GREEN)}\n")
        server.server_close()


if __name__ == "__main__":
    launch_server(port=5000, auto_open=True)
