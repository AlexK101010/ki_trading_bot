# main.py – Startpunkt des KI-Trading-Bots
import time
from trading_bot import TradingBot
from config import COINS, MIN_TRADE_INTERVAL

if __name__ == "__main__":
    bot = TradingBot(coins=COINS, min_trade_interval=MIN_TRADE_INTERVAL)

    print("🤖 KI-Trading-Bot läuft...")

    try:
        while True:
            bot.run_strategy()
            time.sleep(bot.min_trade_interval)
    except KeyboardInterrupt:
        print("🛑 Bot wurde manuell gestoppt.")
