import time
import random
import requests
from config import NEWS_API_KEY, INITIAL_CAPITAL, MAX_HEBEL, MIN_TRADE_INTERVAL, AGGRESSIV_IN_DER_LERNPHASE

class TradingBot:
    def __init__(self, coins):
        self.capital = INITIAL_CAPITAL
        self.coins = coins
        self.trade_history = []
        self.min_trade_interval = MIN_TRADE_INTERVAL
        self.aggressiv = AGGRESSIV_IN_DER_LERNPHASE

    def run_strategy(self):
        for symbol in self.coins:
            price = self.fetch_price(symbol)
            signal = self.generate_signal(price, symbol)
            if signal:
                self.execute_trade(symbol, signal, price)

    def fetch_price(self, symbol):
        # Dummy-Methode, CoinGecko API kommt später rein
        return round(random.uniform(50, 50000), 2)

    def generate_signal(self, price, symbol):
        # Beispiel: kombinierte einfache Heuristik
        fib = price % 2 == 0
        rsi = random.choice(["Overbought", "Neutral", "Oversold"])
        ma = price > 10000
        sentiment = self.fetch_news_sentiment(symbol)
        signal = None

        if fib and rsi == "Oversold" and ma:
            signal = "Buy"
        elif rsi == "Overbought" and not ma:
            signal = "Sell"
        elif sentiment < -0.5:
            signal = "Sell"
        elif sentiment > 0.5:
            signal = "Buy"

        return signal

    def fetch_news_sentiment(self, symbol):
        try:
            url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}"
            res = requests.get(url).json()
            total = len(res.get("articles", []))
            score = random.uniform(-1, 1) if total > 0 else 0
            return round(score, 2)
        except Exception:
            return 0

    def execute_trade(self, symbol, action, price):
        hebel = random.randint(1, MAX_HEBEL)
        amount = 100 if self.aggressiv else 50
        reward = round(random.uniform(-1, 1) * hebel, 2)
        self.capital += reward
        self.trade_history.append({
            "symbol": symbol,
            "action": action,
            "hebel": hebel,
            "price": price,
            "reward": reward
        })
        print(f"💹 {symbol} | Aktion: {action} | Preis: {price}$ | Hebel: x{hebel} | Gewinn/Verlust: {reward} → Kapital: {self.capital:.2f}$")
