
import pandas as pd
import random
import datetime
import os
from strategy_logger import log_strategy_result

def simulate_trade():
    # Dummy Trade-Daten
    coins = ["BTC", "ETH", "SOL", "XRP", "SUI"]
    coin = random.choice(coins)
    price = round(random.uniform(100, 50000), 2)
    reward = round(random.uniform(-0.1, 0.3), 4)
    action = random.choice(["Buy", "Sell"])

    trade = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "coin": coin,
        "price": price,
        "reward": reward,
        "action": action,
        "fibonacci": random.choice(["Support", "Resistance", "Neutral"]),
        "ma200": random.choice(["Above", "Below"]),
        "news": random.choice(["Bullish", "Bearish", "Neutral"]),
        "fear_greed": random.randint(0, 100)
    }

    strategie_combo = log_strategy_result(trade)
    trade["strategie_combo"] = strategie_combo

    return trade

def log_to_csv(trade, path="bot_log.csv"):
    df = pd.DataFrame([trade])
    if os.path.exists(path):
        df_old = pd.read_csv(path)
        df = pd.concat([df_old, df], ignore_index=True)
    df.to_csv(path, index=False)

if __name__ == "__main__":
    for _ in range(5):  # Simuliere 5 Trades pro Lauf
        t = simulate_trade()
        log_to_csv(t)
        print(f"🔁 Trade geloggt: {t['coin']} {t['action']} @ {t['price']} | Strategie: {t['strategie_combo']}")
