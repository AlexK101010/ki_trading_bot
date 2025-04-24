# trading_bot.py – verbesserte Bot-Klasse mit Learning & Logging

import pandas as pd
import random
import datetime
import os
from strategy_logger import log_strategy_result
from config import INITIAL_CAPITAL, LOGFILE_TRADE, LOGFILE_PERFORMANCE

class TradingBot:
    def __init__(self, coins, min_trade_interval=30):
        self.coins = coins
        self.min_trade_interval = min_trade_interval

    def simulate_trade(self):
        coin = random.choice(self.coins)
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

    def log_trade(self, trade):
        df = pd.DataFrame([trade])
        if os.path.exists(LOGFILE_TRADE):
            df_old = pd.read_csv(LOGFILE_TRADE)
            df = pd.concat([df_old, df], ignore_index=True)
        df.to_csv(LOGFILE_TRADE, index=False)

    def update_performance(self, trade):
        kapital = INITIAL_CAPITAL
        drawdown = 0.0
        win_ratio = 0.0

        if os.path.exists(LOGFILE_PERFORMANCE):
            df_perf = pd.read_csv(LOGFILE_PERFORMANCE)
            kapital = df_perf["kapital"].iloc[-1] + trade["reward"] * 1000
            drawdown = min(drawdown, kapital - df_perf["kapital"].max())
            win_ratio = (df_perf["reward"] > 0).sum() / len(df_perf)
        else:
            kapital += trade["reward"] * 1000

        df_new = pd.DataFrame([{
            "timestamp": trade["timestamp"],
            "kapital": kapital,
            "drawdown": drawdown,
            "win_ratio": win_ratio,
            "reward": trade["reward"]
        }])

        if os.path.exists(LOGFILE_PERFORMANCE):
            df_old = pd.read_csv(LOGFILE_PERFORMANCE)
            df_all = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_all = df_new

        df_all.to_csv(LOGFILE_PERFORMANCE, index=False)

    def run_strategy(self):
        trade = self.simulate_trade()
        self.log_trade(trade)
        self.update_performance(trade)
        print(f"✅ Trade durchgeführt: {trade['coin']} {trade['action']} @ {trade['price']} | Reward: {trade['reward']}, Strategie: {trade['strategie_combo']}")
