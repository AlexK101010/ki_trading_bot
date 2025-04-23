# config.py – zentrale Konfiguration des KI-Trading-Bots

# Bot-Grundeinstellungen
COINS = ["BTC", "ETH", "Sol", "XRP", "SUI"]
NEWS_API_KEY = "f06c6e3435824ecabb3107328164bb72"
CRYPTO_API_KEY = "A1r3tyuiop"

INITIAL_CAPITAL = 10000
MAX_HEBEL = 5
MIN_TRADE_INTERVAL = 10  # Sekunden
AGGRESSIV_IN_DER_LERNPHASE = True

# Dashboard-Schalter
ENABLE_DASHBOARD_CONTROLS = True
ENABLE_TRAINING_PAUSE = True
ENABLE_STRATEGY_RESET = True
ENABLE_TELEGRAM_ALERTS = True
ENABLE_DRAWDOWN_GRAPH = True
ENABLE_HEATMAP = True
ENABLE_KNOWLEDGE_TRACKING = True

# Log-Dateien
LOGFILE_TRADE = "bot_log.csv"
LOGFILE_PERFORMANCE = "performance_log.csv"
JSON_TOP_STRATEGIEN = "top_strategien.json"
JSON_MUTATIONEN = "mutationen_log.json"
TELEGRAM_LOGFILE = "telegram_log.json"
